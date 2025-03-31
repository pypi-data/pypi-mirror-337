import torch
import torch.nn as nn
from einops import rearrange, repeat


class RMSNorm(nn.Module):
    """
    https://arxiv.org/abs/1910.07467

    """

    def __init__(self,
                 dim: int = 512,
                 eps: float = 1e-6
                 ):
        super().__init__()
        self.dim = dim
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor):
        return nn.functional.rms_norm(x, (self.dim, ), self.weight, self.eps)


def precompute_rope_emb(dim: int = 16, seq_len: int = 512 * 8, theta: float = 10000.0):
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2, dtype = torch.float32) / dim))
    t = torch.arange(seq_len)
    freqs = torch.outer(t, freqs)
    rope_emb = torch.polar(torch.ones_like(freqs), freqs)
    return rope_emb


def apply_rope_emb(x: torch.Tensor, rope_emb: torch.Tensor):
    dtype = x.dtype
    x = torch.view_as_complex(x.float().view(*x.shape[:-1], -1, 2))
    rope_emb = rope_emb.view(1, x.shape[1], 1, x.shape[-1])
    y = torch.view_as_real(x * rope_emb).flatten(3)
    return y.to(dtype)


class MLA(nn.Module):
    """
    https://arxiv.org/abs/2412.19437

    """

    def __init__(self,
                 dim: int = 512,
                 n_head: int = 8,
                 q_lora_rank: int = 0,
                 kv_lora_rank: int = 128,
                 qk_nope_head_dim: int = 32,
                 qk_rope_head_dim: int = 16,
                 v_head_dim: int = 32,
                 max_batch_size: int = 32,
                 max_seq_len: int = 512 * 8
                 ):
        super().__init__()
        self.dim = dim
        self.n_head = n_head
        self.q_lora_rank = q_lora_rank
        self.kv_lora_rank = kv_lora_rank
        self.qk_nope_head_dim = qk_nope_head_dim
        self.qk_rope_head_dim = qk_rope_head_dim
        self.qk_head_dim = qk_nope_head_dim + qk_rope_head_dim
        self.v_head_dim = v_head_dim
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len

        if self.q_lora_rank == 0:
            self.to_q = nn.Linear(self.dim, self.n_head * self.qk_head_dim, bias = False)
        else:
            self.to_q = nn.Sequential(
                nn.Linear(self.dim, self.q_lora_rank, bias = False),
                RMSNorm(self.q_lora_rank),
                nn.Linear(self.q_lora_rank, self.n_head * self.qk_head_dim, bias = False)
            )
        self.to_kv_a = nn.Linear(self.dim, qk_rope_head_dim + kv_lora_rank, bias = False)
        self.kv_norm = RMSNorm(self.kv_lora_rank)
        self.to_kv_b = nn.Linear(self.kv_lora_rank, self.n_head * (self.qk_nope_head_dim + self.v_head_dim),
                                 bias = False)
        self.to_out = nn.Linear(self.n_head * self.v_head_dim, self.dim, bias = False)

        self.register_buffer('k_cache',
                             torch.zeros(self.max_batch_size, self.max_seq_len, self.n_head, self.qk_head_dim),
                             persistent = False
                             )
        self.register_buffer('v_cache',
                             torch.zeros(self.max_batch_size, self.max_seq_len, self.n_head, self.v_head_dim),
                             persistent = False
                             )

    def forward(self,
                x: torch.Tensor,
                start_pos: int,
                rope_emb: torch.Tensor,
                mask: torch.Tensor = None,
                use_cache: bool = False
                ):
        # x:[b, n, d]
        b, n, _ = x.shape
        end_pos = start_pos + n
        # q
        q = self.to_q(x)
        q = rearrange(q, 'b n (h d) -> b n h d', h = self.n_head)
        q_nope, q_rope = q.split((self.qk_nope_head_dim, self.qk_rope_head_dim), dim = -1)
        q_rope = apply_rope_emb(q_rope, rope_emb)
        # kv
        kv = self.to_kv_a(x)
        k_rope, kv = kv.split((self.qk_rope_head_dim, self.kv_lora_rank), dim = -1)
        k_rope = apply_rope_emb(k_rope.unsqueeze(2), rope_emb)
        # attn
        q = torch.cat((q_nope, q_rope), dim = -1)
        kv = self.to_kv_b(self.kv_norm(kv))
        kv = rearrange(kv, 'b n (h d) -> b n h d', h = self.n_head)
        k_nope, v = kv.split((self.qk_nope_head_dim, self.v_head_dim), dim = -1)
        k = torch.cat((k_nope, k_rope.expand(-1, -1, self.n_head, -1)), dim = -1)
        if use_cache:
            self.k_cache[:b, start_pos:end_pos] = k
            self.v_cache[:b, start_pos:end_pos] = v
            k = self.k_cache[:b, :end_pos]
            v = self.v_cache[:b, :end_pos]
        q, k, v = map(lambda t: rearrange(t, 'b n h d -> b h n d'), (q, k, v))
        attn = torch.matmul(q, k.transpose(-2, -1)) * (self.qk_head_dim ** -0.5)
        # mask
        if mask is not None:
            attn += mask
        attn = torch.softmax(attn, dim = -1)
        # out
        out = torch.matmul(attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out = self.to_out(out)
        return out


class GQA(nn.Module):
    """
    https://arxiv.org/abs/2305.13245

    """
    
    def __init__(self,
                 dim: int = 512,
                 n_head: int = 8,
                 n_kv_head: int = 2,
                 dropout: float = 0.0,
                 max_batch_size: int = 32,
                 max_seq_len: int = 512 * 8
                 ):
        super().__init__()
        self.dim = dim
        self.n_head = n_head
        self.head_dim = self.dim // self.n_head
        self.n_kv_head = n_kv_head
        self.dropout = dropout
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len

        self.to_q = nn.Linear(self.dim, self.n_head * self.head_dim, bias = False)
        self.to_kv = nn.Linear(self.dim, 2 * self.n_kv_head * self.head_dim, bias = False)
        self.to_out = nn.Linear(self.n_head * self.head_dim, self.dim, bias=False)
        self.dropout = nn.Dropout(self.dropout)

        self.register_buffer('k_cache',
                             torch.zeros(self.max_batch_size, self.max_seq_len, self.n_head, self.head_dim),
                             persistent=False
                             )
        self.register_buffer('v_cache',
                             torch.zeros(self.max_batch_size, self.max_seq_len, self.n_head, self.head_dim),
                             persistent=False
                             )

    def forward(self,
                x: torch.Tensor,
                start_pos: int,
                rope_emb: torch.Tensor,
                mask: torch.Tensor = None,
                use_cache: bool = False
                ):
        # x:[b, n, d]
        b, n, _ = x.shape
        end_pos = start_pos + n
        # q, k, v
        q = self.to_q(x)
        k, v = self.to_kv(x).chunk(2, dim = -1)
        q = rearrange(q, 'b n (h d) -> b n h d', h = self.n_head)
        k, v = map(lambda t: rearrange(t, 'b n (h d) -> b n h d', h = self.n_kv_head), (k, v))
        q, k = map(lambda t: apply_rope_emb(t, rope_emb), (q, k))
        if use_cache:
            self.k_cache[:b, start_pos:end_pos] = k
            self.v_cache[:b, start_pos:end_pos] = v
            k = self.k_cache[:b, :end_pos]
            v = self.v_cache[:b, :end_pos]
        k, v = map(lambda t: repeat(t, 'b n h d -> b n (r h) d', r = self.n_head // self.n_kv_head), (k, v))
        q, k, v = map(lambda t: rearrange(t, 'b n h d -> b h n d'), (q, k, v))
        # attn
        attn = torch.matmul(q, k.transpose(-2, -1)) * (self.head_dim ** -0.5)
        # mask
        if mask is not None:
            attn += mask
        attn = torch.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        # out
        out = torch.matmul(attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out = self.to_out(out)
        return out


class MLP(nn.Module):

    def __init__(self,
                 dim: int = 512,
                 inter_dim: int = 1344
                 ):
        super().__init__()
        self.dim = dim
        self.inter_dim = inter_dim

        self.linear1 = nn.Linear(self.dim, self.inter_dim, bias = False)
        self.linear2 = nn.Linear(self.inter_dim, self.dim, bias = False)
        self.linear3 = nn.Linear(self.dim, self.inter_dim, bias = False)
        self.silu = nn.SiLU()

    def forward(self, x: torch.Tensor):
        return self.linear2(self.silu(self.linear1(x)) * self.linear3(x))


class Block(nn.Module):

    def __init__(self,
                 # MLA
                 dim: int = 512,
                 inter_dim: int = 1344,
                 n_head: int = 8,
                 q_lora_rank: int = 0,
                 kv_lora_rank: int = 128,
                 qk_nope_head_dim: int = 32,
                 qk_rope_head_dim: int = 16,
                 v_head_dim: int = 32,
                 # GQA
                 n_kv_head: int = 2,
                 dropout: float = 0.0,
                 # common
                 max_batch_size: int = 32,
                 max_seq_len: int = 512 * 8,
                 attn_name = 'mla',
                 mlp_name = 'mlp'
                 ):
        super().__init__()

        if attn_name == 'MLA' or attn_name == 'mla':
            self.attn = MLA(dim = dim, n_head = n_head, q_lora_rank = q_lora_rank, kv_lora_rank = kv_lora_rank,
                            qk_nope_head_dim = qk_nope_head_dim, qk_rope_head_dim = qk_rope_head_dim,
                            v_head_dim = v_head_dim, max_batch_size = max_batch_size, max_seq_len = max_seq_len)
        elif attn_name == 'GQA' or attn_name ==  'gqa':
            self.attn = GQA(dim = dim, n_head = n_head, n_kv_head = n_kv_head, dropout = dropout,
                            max_batch_size = max_batch_size, max_seq_len = max_seq_len)
        else:
            raise ValueError('attn_name must be MLA or GQA')

        if mlp_name == 'mlp':
            self.mlp = MLP(dim = dim, inter_dim = inter_dim)
        else:
            raise ValueError('mlp_name must be mlp')

        self.attn_norm = RMSNorm(dim)
        self.mlp_norm = RMSNorm(dim)

    def forward(self,
                x: torch.Tensor,
                start_pos: int,
                rope_emb: torch.Tensor,
                mask: torch.Tensor = None,
                use_cache: bool = False
                ):
        x = x + self.attn(self.attn_norm(x), start_pos, rope_emb, mask = mask, use_cache = use_cache)
        x = x + self.mlp(self.mlp_norm(x))
        return x


class Transformer(nn.Module):

    def __init__(self,
                 # embedding
                 vocab_size: int = 6400,
                 # MLA
                 dim: int = 512,
                 inter_dim: int = 1344,
                 n_head: int = 8,
                 q_lora_rank: int = 0,
                 kv_lora_rank: int = 128,
                 qk_nope_head_dim: int = 32,
                 qk_rope_head_dim: int = 16,
                 v_head_dim: int = 32,
                 # GQA
                 n_kv_head: int = 2,
                 dropout: float = 0.0,
                 # Transformer
                 n_layer: int = 8,
                 # common
                 max_batch_size: int = 32,
                 max_seq_len: int = 512 * 8,
                 attn_name='mla',
                 mlp_name='mlp'
                 ):
        super().__init__()

        self.token_embedding = nn.Embedding(vocab_size, dim)

        self.transformer = nn.ModuleList([
            Block(dim=dim, inter_dim=inter_dim, n_head=n_head, q_lora_rank=q_lora_rank,
                  kv_lora_rank=kv_lora_rank, qk_nope_head_dim=qk_nope_head_dim, qk_rope_head_dim=qk_rope_head_dim,
                  v_head_dim=v_head_dim, n_kv_head=n_kv_head, dropout=dropout, max_batch_size=max_batch_size,
                  max_seq_len=max_seq_len, attn_name=attn_name, mlp_name=mlp_name)
            for _ in range(n_layer)
        ])

        self.out_norm = RMSNorm(dim)
        self.to_out = nn.Linear(dim, vocab_size, bias = False)

        self.register_buffer('rope_emb',
                             precompute_rope_emb(dim = qk_rope_head_dim, seq_len = max_seq_len) if attn_name == 'mla'
                             else precompute_rope_emb(dim = dim // n_head, seq_len = max_seq_len),
                             persistent = False
                             )

    def forward(self,
                x: torch.Tensor,
                start_pos: int,
                mask: torch.Tensor = None,
                use_cache: bool = False
                ):
        # x:[b, n]
        b, n = x.shape
        end_pos = start_pos + n
        # embedding
        x = self.token_embedding(x)
        rope_emb = self.rope_emb[start_pos: end_pos]
        # transformer
        for layer in self.transformer:
            x = layer(x, start_pos, rope_emb, mask = mask, use_cache = use_cache)
        out = self.to_out(self.out_norm(x))
        return out


if __name__ == '__main__':
    data = torch.randint(0, 6400, (2, 512))

    mask = torch.triu(torch.full((512, 512), float('-inf')), 1)

    model = Transformer(attn_name = 'mla')
    total_param = 0
    for param in model.parameters():
        if param.requires_grad:
            total_param += param.numel()
    print(total_param)
    model(data, 0, mask = mask)

    model = Transformer(attn_name='gqa')
    total_param = 0
    for param in model.parameters():
        if param.requires_grad:
            total_param += param.numel()
    print(total_param)
    model(data, 0, mask = mask)
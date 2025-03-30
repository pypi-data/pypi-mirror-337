import torch
import torch.nn as nn


class MultiSelfAttension(nn.Module):
    def __init__(self, d_model, num_heads, masked=False, device=None):
        super().__init__()
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        assert d_model % num_heads == 0
        self.masked = masked
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_k = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_v = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_o = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.softmax = nn.Softmax(dim=-1).to(self.device)

    def forward(self, x):
        x = x.to(self.device)
        batch_size, seq_len, d_model = x.shape
        Q = self.W_q(x).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        scores = (Q @ K.transpose(-2, -1)) / (self.d_k ** 0.5)
        if self.masked:
            mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0).to(self.device)
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attention = self.softmax(scores)
        output = (attention @ V).transpose(1, 2).reshape(batch_size, seq_len, d_model)
        return self.W_o(output)
import torch
import torch.nn as nn


class MultiCrossAttention(nn.Module):
    def __init__(self, d_model, num_heads, device=None):
        super().__init__()
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_k = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_v = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.W_o = nn.Linear(d_model, d_model, bias=False).to(self.device)
        self.softmax = nn.Softmax(dim=-1).to(self.device)

    def forward(self, x, encoder_output):
        x = x.to(self.device)
        encoder_output = encoder_output.to(self.device)
        batch_size, seq_len, d_model = x.shape
        Q = self.W_q(x).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(encoder_output).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(encoder_output).reshape(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        scores = (Q @ K.transpose(-2, -1)) / (self.d_k ** .5)
        attention = self.softmax(scores)
        output = (attention @ V).transpose(1, 2).reshape(batch_size, seq_len, d_model)
        out = self.W_o(output)
        return out
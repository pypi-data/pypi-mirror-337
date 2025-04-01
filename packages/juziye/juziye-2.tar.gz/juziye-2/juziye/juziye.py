import torch
from torch import nn
import math

class ModelConfig:
    def __init__(self,
                 hidden_size=512,  
                 num_attention_heads=8,  
                 num_hidden_layers=2,  
                 intermediate_size=1024,  
                 hidden_dropout_prob=0.1,  
                 add_norm_dropout_prob=0.1, 
                 attention_probs_dropout_prob=0.1):
        """
        存储模型的超参数配置    
        """
        # 把传入的 hidden_size 参数赋值给类的 hidden_size 变量，这样我们就能在类的其他地方使用这个参数了
        self.hidden_size = hidden_size
        self.num_attention_heads = num_attention_heads
        self.num_hidden_layers = num_hidden_layers
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.add_norm_dropout_prob = add_norm_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob


class MultiHeadAttention(nn.Module):
    # config 是 ModelConfig 类的实例，我们从 config 里面获取超参数。
    def __init__(self, config):
        super().__init__()
        # 检查 hidden_size 是否可以被 num_attention_heads 整除，这是多头注意力机制的要求
        if config.hidden_size % config.num_attention_heads != 0:
            raise ValueError("hidden_size必须是num_attention_heads的整数倍")

        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = config.hidden_size // config.num_attention_heads # 每个注意力头的维度
        self.all_head_size = self.num_attention_heads * self.attention_head_size # 所有注意力头拼接后的总维度，理论上应该等于 config.hidden_size，用于后续的计算

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)

        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)

    def transpose_for_scores(self, x):
        """
        调整形状：使用 view() 把 hidden_size 拆分成 (num_heads, head_dim)，然后 permute() 交换维度。
        把张量的形状变换为 (batch_size, num_heads, seq_length, head_dim)

        1.假设输入 x 的形状是：
            (batch_size, seq_length, hidden_size)

        2.使用 view() 将 hidden_size 拆分成 num_heads 个 head_dim：
            (batch_size, seq_length, num_heads, head_dim)

        3.这种形状不方便计算 QK^T，因为矩阵相乘通常希望最后两个维度表示“行 × 列”。
          为了计算方便，我们交换维度：
            (batch_size, num_heads, seq_length, head_dim)

        4.这样：num_heads 变成第二个维度，让所有头并行计算，seq_length 和 head_dim 保持原来的结构，方便矩阵运算。
        """
        # 在 Transformer 的多头注意力机制里，我们需要把 hidden_size 拆成 (num_heads, head_dim)
        # x.size()[:-1] 取 size() 的前 n-1 维，去掉最后一维（hidden_size），只保留 (batch_size, seq_length)
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        # 使用 view() 将 hidden_size 拆分成 num_heads 个 head_dim
        x = x.view(*new_x_shape)
        # permute 交换张量的维度，这样做的目的是：让 num_heads 维度提前，使得每个头可以并行计算 QK^T 。
        # 方便后续的矩阵运算（计算注意力分数）。      
        return x.permute(0, 2, 1, 3)

    def forward(self, query, key, value, attention_mask=None):
        # 计算q、k、v向量并调整形状，用于多头注意力机制
        query_layer = self.transpose_for_scores(self.query(query))
        key_layer = self.transpose_for_scores(self.key(key))
        value_layer = self.transpose_for_scores(self.value(value))
        """
            计算注意力分数：QK^T
            用 matmul() 计算注意力分数，并通过 softmax() 归一化
            query_layer、key_layer 的形状都是 (batch_size, num_heads, seq_length, head_dim)
            key_layer.transpose(-1, -2) 变成 (batch_size, num_heads, head_dim, seq_length)
            计算 matmul(Q, K^T) 后，得到 (batch_size, num_heads, seq_length, seq_length)
        """
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
        """
            进行缩放：
            除以 sqrt(d_k) 进行缩放，避免 QK^T 值过大导致 softmax 结果太极端（梯度消失或爆炸）。
        """
        attention_scores = attention_scores / math.sqrt(self.attention_head_size)

        if attention_mask is not None:
            attention_scores = attention_scores + attention_mask

        attention_probs = nn.Softmax(dim=-1)(attention_scores)
        attention_probs = self.dropout(attention_probs)

        context_layer = torch.matmul(attention_probs, value_layer)
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)

        return context_layer.view(*new_context_layer_shape)
    
class AddNorm(nn.Module):
    """ 残差连接 + LayerNorm """
    def __init__(self, config, eps=1e-12):
        super().__init__()
        self.layer_norm = nn.LayerNorm(config.hidden_size, eps=eps)
        self.dropout = nn.Dropout(config.add_norm_dropout_prob)

    def forward(self, x, residual):
        # 确保 residual 和 x 维度一致
        if x.size() != residual.size():
            raise ValueError(f"Input x and residual must have the same shape: {x.size()} vs {residual.size()}")
        return self.layer_norm(self.dropout(x + residual))

"""
    FeedForward 层用来增强 Transformer 的表示能力，避免单纯的注意力机制过于线性化
"""
class FeedForward(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense1 = nn.Linear(config.hidden_size, config.intermediate_size)
        self.activation = nn.ReLU()
        self.dense2 = nn.Linear(config.intermediate_size, config.hidden_size)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, x):
        x = self.dense1(x)
        x = self.activation(x)
        x = self.dense2(x)
        x = self.dropout(x)
        return x
    
class SelfAttentionBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = MultiHeadAttention(config)
        self.add_norm1 = AddNorm(config.hidden_size)  # 用于 Self-Attention
        self.feed_forward = FeedForward(config)
        self.add_norm2 = AddNorm(config.hidden_size)  # 用于 FeedForward

    def forward(self, x, attention_mask=None):
        # 在 Self-Attention 里，query、key、value 都是 x
        residual = x
        x = self.attention(x, x, x, attention_mask)
        x = self.add_norm1(x, residual)
        
        residual = x
        x = self.feed_forward(x)
        x = self.add_norm2(x, residual)  # 残差 + 归一化
        return x

class CrossAttentionBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = MultiHeadAttention(config)
        self.add_norm1 = AddNorm(config.hidden_size)  # Cross-Attention 后的残差 + 归一化
        self.feed_forward = FeedForward(config)
        self.add_norm2 = AddNorm(config.hidden_size)  # FeedForward 后的残差 + 归一化

    def forward(self, modal_1, modal_2, attention_mask=None):
        residual = modal_1
        modal_1 = self.attention(modal_1, modal_2, modal_2, attention_mask)
        modal_1 = self.add_norm1(modal_1, residual)  # 残差 + 归一化

        residual = modal_1
        modal_1 = self.feed_forward(modal_1)
        modal_1 = self.add_norm2(modal_1, residual)  # 残差 + 归一化
        return modal_1
    



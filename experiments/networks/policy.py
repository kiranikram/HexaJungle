mode = Enum('Player', 'SENDER RECVER')

def relaxedembedding(x, weight, *args):
    if isinstance(x, torch.LongTensor) or (torch.cuda.is_available() and isinstance(x, torch.cuda.LongTensor)):
        return F.embedding(x, weight, *args)
    else:
        return torch.matmul(x, weight)


class RelaxedEmbedding(nn.Embedding):
    def forward(self, x):
        if isinstance(x, torch.LongTensor) or (torch.cuda.is_available() and isinstance(x, torch.cuda.LongTensor)):
            return F.embedding(x, self.weight, self.padding_idx, self.max_norm, self.norm_type, self.scale_grad_by_freq, self.sparse)
        else:
            return torch.matmul(x, self.weight)

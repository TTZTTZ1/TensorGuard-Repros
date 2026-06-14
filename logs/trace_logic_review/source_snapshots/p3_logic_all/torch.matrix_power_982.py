
m = torch.tensor([[0.1, 0.2], [0.0, 10.0]])
matrix = torch.linalg.matrix_power(m, 5)
matrix = (torch.matmul(matrix, matrix) + m)
matrix = (torch.matmul(matrix.transpose(0, 1), matrix.transpose(0, 1)) + m)
matrix = (torch.matmul(matrix.transpose(0, 1).inverse(), matrix.transpose(0, 1)) - m)
matrix = (matrix / torch.norm(matrix, p=2, dim=1).expand_as(matrix))
n = 2
matrix = torch.matmul(matrix, matrix.transpose(0, 1))
matrix = (matrix + ((torch.eye(n, n, dtype=matrix.dtype) * n) * torch.eye(n, n, dtype=matrix.dtype)))
matrix = torch.tril(matrix, (- 1))
result = torch.matrix_power(matrix, n)
torch.allclose(matrix, result)

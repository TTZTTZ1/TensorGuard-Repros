
input_tensor = torch.tensor([[0, 0, 0, 1, 1], [1, 0, 0, 3, 4], [3, 0, 0, 2, 4], [2, 0, 0, 5, 4], [4, 0, 2, 0, 1], [2, 5, 1, 5, 5], [0, 4, 2, 3, 0]], dtype=torch.float32)
k = 2
dim = 1
topk_result = torch.topk(input_tensor, k, dim=dim, largest=True)
topk_result = list(topk_result)
for result in topk_result:
    print(result)

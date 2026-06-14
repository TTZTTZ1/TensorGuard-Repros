import sys
import torch
import torch.nn.functional as F

print("torch:", torch.__version__)
print("cuda:", torch.version.cuda)

device = sys.argv[1] if len(sys.argv) > 1 else "cpu"
print("device:", device)

torch.manual_seed(420)

FloatTensor = torch.cuda.FloatTensor if device.startswith("cuda") else torch.FloatTensor

x = torch.randn(100, 3, 128, 128, device=device)
x = torch.relu(x)
x = torch.clamp(x, min=0.0, max=1.0)
x = torch.reshape(x, (-1, 4, 4, 4)).type(FloatTensor)

kernel_size = (2, 2, 2)
output_size = (1, 1, 1)

random_samples = torch.rand(100, 3, 128, 128, device=device)
random_samples = torch.relu(random_samples)
random_samples = torch.clamp(random_samples, min=0.0, max=1.0)
random_samples = torch.reshape(random_samples, (-1, 4, 4, 4)).type(FloatTensor)

print("x.shape:", tuple(x.shape))
print("random_samples.shape:", tuple(random_samples.shape))

# This follows the generated call shape:
# fractional_max_pool3d(x, output_size, fractional_stride, random_samples, return_indices)
y = F.fractional_max_pool3d(x, kernel_size, output_size, random_samples, False)

if device.startswith("cuda"):
    torch.cuda.synchronize()

print("ok")
print("y.shape:", tuple(y.shape))

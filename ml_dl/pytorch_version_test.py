import torch

# torch 버전 확인
print("Pytorch 버전:", torch.__version__)

# CUDA 사용 가능 여부 확인
print("CUDA 사용 가능 여부:", torch.cuda.is_available())

# 사용 가능한 GPU 개수 확인
print("사용 가능한 GPU 개수:", torch.cuda.device_count())

# 현재 사용 중인 디바이스 ID
print("현재 디바이스 ID:", torch.cuda.current_device())

# 현재 디바이스 이름
print("현재 디바이스 이름:", torch.cuda.get_device_name(torch.cuda.current_device()))

# 텐서를 GPU에 할당해보기
x = torch.tensor([1.0, 2.0, 3.0]).to('cuda')
print("GPU에 할당된 텐서:", x)
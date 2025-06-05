import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import streamlit as st
from PIL import Image
import numpy as np
import os

# CNN 모델 정의 (test.py와 동일한 구조)
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# CIFAR-10 클래스 이름
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']

# 모델 로드 함수
@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load('cifar10_cnn_0605.pth', map_location=device))
    model.eval()
    return model, device

# 이미지 전처리 함수
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    return transform(image).unsqueeze(0)

# Streamlit 앱 UI
st.title("CIFAR-10 이미지 분류기")
st.write("이미지를 업로드하거나 샘플 이미지를 선택하여 CIFAR-10 클래스로 분류합니다.")

model, device = load_model()

# 샘플 이미지 선택
sample_dir = "test_sample"
sample_images = [f for f in os.listdir(sample_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
sample_choice = st.selectbox("샘플 이미지 선택 (test_sample 폴더)", [None] + sample_images)

# 이미지 업로드
uploaded_file = st.file_uploader("또는 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

image = None
if sample_choice and sample_choice != 'None':
    image = Image.open(os.path.join(sample_dir, sample_choice))
    st.image(image, caption=f'샘플 이미지: {sample_choice}', use_container_width=True)
elif uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 이미지', use_container_width=True)

if image is not None:
    if st.button('분류하기'):
        input_tensor = preprocess_image(image).to(device)
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
        st.write(f"예측 결과: {classes[predicted_class]}")
        probs = probabilities[0].cpu().numpy()
        st.bar_chart(dict(zip(classes, probs)))

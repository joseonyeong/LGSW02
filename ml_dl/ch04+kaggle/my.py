# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import joblib
import time

train = pd.read_csv('train.xls')

features = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
target = 'Calories'

# 전처리
train['Sex'] = train['Sex'].map({'male':0, 'female':1})

x = train[features]
y = train[target]
# target 설정
# 독립변수 : 신체정보 + 운동특성
# 종속변수 : 칼로리 소모량

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state = 42,
    stratify = y
)



# 사용할 모델 정의
models = {
    'RandomForest': RandomForestClassifier(random_state=42),  # 랜덤 포레스트 분류기
    'SVM': SVC(random_state=42, probability=True),  # 서포트 벡터 머신
    'LogisticRegression': (random_state=42)  # 로지스틱 회귀
}

# 각 모델별 하이퍼파라미터 후보군 정의
param_grid = {
    'RandomForest': [
        {'n_estimators': 100, 'max_depth': None},  # 트리 100개, 깊이 제한 없음
        {'n_estimators': 200, 'max_depth': 5}      # 트리 200개, 최대 깊이 5
    ],
    'SVM': [
        {'C': 1.0, 'kernel': 'rbf'},    # RBF 커널, C=1.0
        {'C': 0.5, 'kernel': 'linear'}  # 선형 커널, C=0.5
    ],
    'LogisticRegression': [
        {'C': 1.0, 'max_iter': 1000},  # 기본 설정
        {'C': 0.1, 'max_iter': 1000}   # 더 강한 정규화
    ]
}

# 객체 검증을 통한 최적 모델 선택
best_score = 0 # 최고 성능 점수
best_model_name = None # 최고 성능 모델 이름
best_model = None # 최고 성능 모델 객체

# 각 모델과 하이퍼파라미터 조합에 대해 교차검증 수행
for model_name, model in models.items():
    print(f"\n--- Testing {model_name} ---")
    for params in param_grid[model_name]:
        model.set_params(**params)  # 하이퍼파라미터 설정
        cv_scores = cross_val_score(model, x_train, y_train, cv=5, scoring='accuracy')  # 5-fold 교차검증
        mean_cv = np.mean(cv_scores)  # 평균 교차검증 점수
        print(f"Params: {params}, CV Accuracy: {mean_cv:.4f}")
        
        # 최고 성능 모델 업데이트
        if mean_cv > best_score:
            best_score = mean_cv
            best_model_name = model_name
            best_model = model.set_params(**params)

# 최종 선택된 모델로 테스트셋 평가
best_model.fit(x_train, y_train)  # 최적 모델 학습
y_pred = best_model.predict(x_test)  # 테스트셋 예측
test_acc = accuracy_score(y_test, y_pred)  # 테스트셋 정확도 계산

# 최종 결과 출력
print(f"\nBest Model: {best_model_name}")
print(f"Best CV Score: {best_score:.4f}")
print(f"Test Set Accuracy: {test_acc:.4f}")
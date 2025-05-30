# 필요한 라이브러리 임포트
import pandas as pd  # 데이터 처리를 위한 pandas
import numpy as np   # 수치 계산을 위한 numpy
from sklearn.ensemble import RandomForestClassifier  # 랜덤 포레스트 분류기
from sklearn.svm import SVC  # 서포트 벡터 머신
from sklearn.linear_model import LogisticRegression  # 로지스틱 회귀
from sklearn.model_selection import train_test_split, cross_val_score  # 데이터 분할 및 교차 검증
from sklearn.metrics import accuracy_score  # 정확도 평가 지표
import joblib  # 모델 저장을 위한 joblib
import json  # 전처리 정보 저장을 위한 json

# Titanic 데이터셋 로드
data = pd.read_csv('train.csv')

# 모델링에 사용할 특성(features)과 타겟(target) 변수 선택
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']  # 승객 등급, 성별, 나이, 동반자 수, 요금, 탑승 항구
target = 'Survived'  # 생존 여부 (0: 사망, 1: 생존)

# 범주형 변수를 수치형으로 변환
data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})  # 성별: 남성=0, 여성=1
data['Embarked'] = data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})  # 탑승 항구: C=0, Q=1, S=2

# 데이터를 훈련셋과 테스트셋으로 분할 (비율: 75:25)
X = data[features]  # 특성 데이터
y = data[target]    # 타겟 데이터
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

# 훈련셋에서 결측치를 채울 대표값 계산
age_mean = X_train['Age'].mean()  # 나이의 평균값
fare_mean = X_train['Fare'].mean()  # 요금의 평균값
pclass_mode = X_train['Pclass'].mode()[0]  # 승객 등급의 최빈값
embarked_mode = X_train['Embarked'].mode()[0]  # 탑승 항구의 최빈값

# 훈련셋의 결측치 처리
X_train['Age'] = X_train['Age'].fillna(age_mean)  # 나이 결측치를 평균값으로 대체
X_train['Fare'] = X_train['Fare'].fillna(fare_mean)  # 요금 결측치를 평균값으로 대체
X_train['Pclass'] = X_train['Pclass'].fillna(pclass_mode)  # 승객 등급 결측치를 최빈값으로 대체
X_train['SibSp'] = X_train['SibSp'].fillna(0)  # 동반자 수 결측치를 0으로 대체
X_train['Parch'] = X_train['Parch'].fillna(0)  # 부모/자식 수 결측치를 0으로 대체
X_train['Embarked'] = X_train['Embarked'].fillna(embarked_mode)  # 탑승 항구 결측치를 최빈값으로 대체

# 테스트셋의 결측치 처리 (훈련셋에서 계산한 대표값 사용)
X_test['Age'] = X_test['Age'].fillna(age_mean)
X_test['Fare'] = X_test['Fare'].fillna(fare_mean)
X_test['Pclass'] = X_test['Pclass'].fillna(pclass_mode)
X_test['SibSp'] = X_test['SibSp'].fillna(0)
X_test['Parch'] = X_test['Parch'].fillna(0)
X_test['Embarked'] = X_test['Embarked'].fillna(embarked_mode)

# 사용할 모델 정의
models = {
    'RandomForest': RandomForestClassifier(random_state=42),  # 랜덤 포레스트 분류기
    'SVM': SVC(random_state=42, probability=True),  # 서포트 벡터 머신
    'LogisticRegression': LogisticRegression(random_state=42)  # 로지스틱 회귀
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

# 교차검증을 통한 최적 모델 선택
best_score = 0  # 최고 성능 점수
best_model_name = None  # 최고 성능 모델 이름
best_model = None  # 최고 성능 모델 객체

# 각 모델과 하이퍼파라미터 조합에 대해 교차검증 수행
for model_name, model in models.items():
    print(f"\n--- Testing {model_name} ---")
    for params in param_grid[model_name]:
        model.set_params(**params)  # 하이퍼파라미터 설정
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')  # 5-fold 교차검증
        mean_cv = np.mean(cv_scores)  # 평균 교차검증 점수
        print(f"Params: {params}, CV Accuracy: {mean_cv:.4f}")
        
        # 최고 성능 모델 업데이트
        if mean_cv > best_score:
            best_score = mean_cv
            best_model_name = model_name
            best_model = model.set_params(**params)

# 최종 선택된 모델로 테스트셋 평가
best_model.fit(X_train, y_train)  # 최적 모델 학습
y_pred = best_model.predict(X_test)  # 테스트셋 예측
test_acc = accuracy_score(y_test, y_pred)  # 테스트셋 정확도 계산

# 전처리 정보 저장
preprocessing_info = {
    'age_mean': float(age_mean),
    'fare_mean': float(fare_mean),
    'pclass_mode': int(pclass_mode),
    'embarked_mode': int(embarked_mode),
    'features': features,
    'sex_mapping': {'male': 0, 'female': 1},
    'embarked_mapping': {'C': 0, 'Q': 1, 'S': 2}
}

# 모델과 전처리 정보 저장
joblib.dump(best_model, 'titanic_model.joblib')
with open('preprocessing_info.json', 'w') as f:
    json.dump(preprocessing_info, f)

# 최종 결과 출력
print(f"\nBest Model: {best_model_name}")
print(f"Best CV Score: {best_score:.4f}")
print(f"Test Set Accuracy: {test_acc:.4f}")
print("\nModel and preprocessing information have been saved.")

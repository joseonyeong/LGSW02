# train 데이터 기반

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

# 데이터 로드
data = pd.read_csv('train.csv')

# 특성과 타겟 분리
X = data.drop(['id', 'Calories'], axis=1)
y = data['Calories']

# 학습/테스트 데이터 분할 (데이터 누수 방지)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 수치형 특성과 범주형 특성 분리
numeric_features = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
categorical_features = ['Sex']

# 수치형 특성 스케일링 (학습 데이터로만 fit)
scaler = StandardScaler()
X_train_numeric = scaler.fit_transform(X_train[numeric_features])
X_test_numeric = scaler.transform(X_test[numeric_features])

# 범주형 특성 원-핫 인코딩 (학습 데이터로만 fit)
encoder = OneHotEncoder(sparse_output=False)
X_train_categorical = encoder.fit_transform(X_train[categorical_features])
X_test_categorical = encoder.transform(X_test[categorical_features])

# 특성 결합
X_train_processed = np.hstack([X_train_numeric, X_train_categorical])
X_test_processed = np.hstack([X_test_numeric, X_test_categorical])

# 사용할 모델 정의
models = {
    'DecisionTree': DecisionTreeRegressor(random_state=42),
    'RandomForest': RandomForestRegressor(random_state=42),
    'LinearRegression': LinearRegression(),
    'SVR': SVR()
}

# 각 모델별 하이퍼파라미터 후보군 정의
param_grid = {
    'DecisionTree': [
        {'max_depth': 5},
        {'max_depth': 10}
    ],
    'RandomForest': [
        {'n_estimators': 100},
        {'n_estimators': 200}
    ],
    'LinearRegression': [
        {}
    ],
    'SVR': [
        {'kernel': 'linear'},
        {'kernel': 'rbf'}
    ]
}

# 최고 성능 모델 추적을 위한 변수 초기화
best_score = float('-inf')
best_model_name = None
best_model = None
best_params = None

# 모델 학습 및 평가
for model_name, model in models.items():
    print(f"\n--- Testing {model_name} ---")
    for params in param_grid[model_name]:
        # 모델 파라미터 설정
        model.set_params(**params)
        
        # 학습 시간 측정
        start_time = time.time()
        
        # 교차 검증 수행
        cv_scores = cross_val_score(model, X_train_processed, y_train, cv=5, scoring='r2')
        mean_cv = np.mean(cv_scores)
        
        # 모델 학습
        model.fit(X_train_processed, y_train)
        training_time = time.time() - start_time
        
        print(f"Parameters: {params}")
        print(f"Training Time: {training_time:.2f} seconds")
        print(f"Cross-validation R2 Score: {mean_cv:.4f}")
        
        # 최고 성능 모델 업데이트
        if mean_cv > best_score:
            best_score = mean_cv
            best_model_name = model_name
            best_model = model
            best_params = params

# 최고 성능 모델 저장
model_info = {
    'model': best_model,
    'scaler': scaler,
    'encoder': encoder
}
# joblib.dump(model_info, 'model.pkl')
joblib.dump(model_info, 'model.joblib')

# 최종 결과 출력
print("\n=== 최종 결과 ===")
print(f"Best Model: {best_model_name}")
print(f"Best Parameters: {best_params}")
print(f"Best CV Score: {best_score:.4f}")
print("Best model has been saved to 'model.pkl'")

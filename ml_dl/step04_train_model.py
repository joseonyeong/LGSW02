# train_pipeline.py
import pandas as pd
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. 데이터 로드
tips = sns.load_dataset("tips")

# 2. 특성과 타겟 지정 (tip으로 size 분류)
features = ['total_bill', 'sex', 'smoker', 'day', 'time', 'tip']
target = 'size'
X = tips[features]
y = tips[target].astype(str)  # 다중분류 위해 str로 처리

# 3. 전처리 파이프라인 구성
numeric_features = ['total_bill', 'tip']
categorical_features = ['sex', 'smoker', 'day', 'time']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# 4. 전체 파이프라인 구성 (분류 모델)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# 5. 학습 및 평가
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
pipeline.fit(X_train, y_train)
preds = pipeline.predict(X_test)
acc = accuracy_score(y_test, preds)

# 6. MLflow 로깅
mlflow.set_experiment("Tips_Size_Classification")

with mlflow.start_run() as run:
    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(pipeline, "pipeline_model")
    print(f"분류 모델 저장 완료 - run_id: {run.info.run_id}")
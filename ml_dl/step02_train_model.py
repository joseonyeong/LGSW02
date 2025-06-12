# train_pipeline.py
import pandas as pd
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 데이터 로드
tips = sns.load_dataset("tips")
X = tips[["total_bill"]]
y = tips["tip"]

# 학습/검증 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 파이프라인 구성
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression())
])

# MLflow 실험 설정
mlflow.set_experiment("Tips_Pipeline_Experiment2")

with mlflow.start_run() as run:
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    # 로그 기록
    mlflow.log_param("model_type", "StandardScaler+LinearRegression")
    mlflow.log_metric("mse", mse)

    # 전체 파이프라인 저장
    mlflow.sklearn.log_model(pipe, artifact_path="pipeline_model")

    print(f"✅ 파이프라인 저장 완료 (run_id: {run.info.run_id})")
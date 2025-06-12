import mlflow.sklearn
import pandas as pd
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

tips = sns.load_dataset('tips')
# print(tips.head(2))
x = tips[['size']]
y = tips['tip']

x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=42)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

mlflow.set_experiment('Tips_Pipeline_Experiment3')
with mlflow.start_run() as run:
    pipe.fit(x_train, y_train)
    preds = pipe.predict(x_test)
    mse = mean_squared_error(y_test, preds)

    mlflow.log_param('model_type', 'StandardScaler+LinearRegression')
    mlflow.log_metric('mse', mse)

    mlflow.sklearn.log_model(pipe, artifact_path='pipeline_model')
    print(f"✅ 파이프라인 저장 완료 (run_id: {run.info.run_id})")
import mlflow.sklearn
import pandas as pd
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

mlflow.set_tracking_uri('http://127.0.0.1:5000/')

tips = sns.load_dataset('tips')
x = tips[['total_bill']]
y = tips['tip']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 모델 생성
mlflow.set_experiment('Tips-Regression-Exp')
with mlflow.start_run():
    model = LinearRegression()
    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    mse = mean_squared_error(y_test, preds)

    # 해당 모델 mlflow에 추가
    mlflow.log_param('model_type', 'LinearRegresstion')
    mlflow.log_metric('mse', mse)

    # 모델 저장
    mlflow.sklearn.log_model(model, name='model')
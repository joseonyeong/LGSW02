import mlflow.sklearn
import mlflow.sklearn
import streamlit as st
import pandas as pd
from mlflow.tracking import MlflowClient

st.title('MLFlow-Streamlit 2')

client = MlflowClient()
experiment = client.get_experiment_by_name('Tips_Pipeline_Experiment2')

# runid 가져오기
runs = client.search_runs(experiment_ids=[experiment.experiment_id],
                          order_by=['start_time desc'])                 # 최신 모델만 추출 (여러 모델 존재 시)
# print(experiment.experiment_id)
latest_run_id = runs[0].info.run_id
print(runs)
print('------------------------------------------------------------')
print(latest_run_id)


model_uri = f"runs:/{latest_run_id}/pipeline_model"
model = mlflow.sklearn.load_model(model_uri)

st.write(model)
# Streamlit 입력 UI
bill = st.number_input("Total Bill ($)", min_value=0.0, step=1.0)

if st.button("예측하기"):
    input_df = pd.DataFrame([[bill]], columns=["total_bill"])
    pred = model.predict(input_df)[0]
    st.success(f"예상 팁 금액은 💵 ${pred:.2f} 입니다.")
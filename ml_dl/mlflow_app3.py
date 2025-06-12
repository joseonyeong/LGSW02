import mlflow.sklearn
import mlflow.sklearn
import mlflow.sklearn
import streamlit as st
import pandas as pd
from mlflow.tracking import MlflowClient

st.title('MLFlow-Streamlit 3')

client = MlflowClient()
experiment = client.get_experiment_by_name('Tips_Pipeline_Experiment3')


runs = client.search_runs(experiment_ids=[experiment.experiment_id],
                          order_by=['start_time desc']) 
latest_run_id = runs[0].info.run_id

model_uri = f"runs:/{latest_run_id}/pipeline_model"
model = mlflow.sklearn.load_model(model_uri)
# st.write(model)
size = st.number_input("size", min_value=0.0, step=1.0)

if st.button("예측하기"):
    input_df = pd.DataFrame([[size]], columns=["size"])
    pred = model.predict(input_df)[0]
    st.success(f"예상 크기는 ${pred:.2f} 입니다.")
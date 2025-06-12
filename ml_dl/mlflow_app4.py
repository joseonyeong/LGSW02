import streamlit as st
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient
import streamlit.components.v1 as components

st.set_page_config(page_title="Size 예측 + MLflow 대시보드", layout="wide")
st.title("📊 Size 예측기 + MLflow UI")

st.subheader("예측 입력")

# 모델 로드
client = MlflowClient()
experiment = client.get_experiment_by_name("Tips_Size_Classification")
runs = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time desc"])
latest_run_id = runs[0].info.run_id
model_uri = f"runs:/{latest_run_id}/pipeline_model"
model = mlflow.sklearn.load_model(model_uri)

# 입력 폼
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        total_bill = st.number_input("Total Bill ($)", min_value=0.0, value=20.0)
        sex = st.selectbox("성별", options=["Male", "Female"])
        day = st.selectbox("요일", options=["Thur", "Fri", "Sat", "Sun"])
    with col2:
        smoker = st.selectbox("흡연 여부", options=["Yes", "No"])
        time = st.selectbox("식사 시간", options=["Lunch", "Dinner"])
        tip = st.number_input("Tip ($)", min_value=0.0, value=3.0)

    submitted = st.form_submit_button("예측하기")

if submitted:
    input_df = pd.DataFrame([{
        "total_bill": total_bill,
        "sex": sex,
        "smoker": smoker,
        "day": day,
        "time": time,
        "tip": tip
    }])
    prediction = model.predict(input_df)[0]
    st.success(f"예측된 인원 수는 **{prediction}명** 입니다.")


st.subheader("MLFlow 실험 대시보드 추가")
components.html(
    """
    <iframe src="http://localhost:5000" width="100%" height="800"></iframe>
    """, 
    height=800
)
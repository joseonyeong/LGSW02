import mlflow.sklearn
import streamlit as st
import mlflow.sklearn
import pandas as pd

st.title('MLFLOW')

mlflow.set_tracking_uri('http://127.0.0.1:5000/')

run_id = 'b6c9a8784b624c5fa45a6d5a4e3a741e'     # mlflow Source run ID
model_uri = f"runs:/{run_id}/model"             # model 은 step01_train_model.py에서 지정한 model 저장 이름
model = mlflow.sklearn.load_model(model_uri)
st.write(model)

# UI
st.title("Tips 예측 앱")
st.write("Total Bill 금액에 따라 팁을 예측합니다.")

bill = st.number_input("Total Bill ($)", min_value=0.0, step=1.0)

if st.button("예측하기"):
    input_df = pd.DataFrame([[bill]], columns=["total_bill"])
    pred = model.predict(input_df)[0]
    st.success(f"예상 팁 금액은 ${pred:.2f} 입니다.")
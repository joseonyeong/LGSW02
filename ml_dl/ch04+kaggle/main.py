import pandas as pd
import numpy as np
import joblib
import json
import streamlit as st

st.title('칼로리 연관성')

# 모델 불러오기 전처리 정보 불러오기

# 모델을 불러와서 세션에 저장한다.
@st.cache_resource
def load_model():
    model = joblib.load('model.pkl')
    with open('preprocessing_info.json', 'r') as f:
        preprocessing_info = json.load(f)
    return model, preprocessing_info

model, preprocessing_info = load_model()

# 입력값 없으면 평균으로 대체한다. -> 없어도 되는 코드임 (반드시 입력을 한다 가정했을 때)
def preprocess_input(data):
    # 입력 데이터를 DataFrame으로 변환
    df = pd.DataFrame([data])
    
    # 성별 변환
    df['Sex'] = df['Sex'].map(preprocessing_info['sex_mapping'])
    
    # 탑승 항구 변환
    df['Embarked'] = df['Embarked'].map(preprocessing_info['embarked_mapping'])
    
    # 결측치 처리
    df['Age'] = df['Age'].fillna(preprocessing_info['age_mean'])
    df['Fare'] = df['Fare'].fillna(preprocessing_info['fare_mean'])
    df['Pclass'] = df['Pclass'].fillna(preprocessing_info['pclass_mode'])
    df['SibSp'] = df['SibSp'].fillna(0)
    df['Parch'] = df['Parch'].fillna(0)
    df['Embarked'] = df['Embarked'].fillna(preprocessing_info['embarked_mode'])
    
    # 필요한 특성만 선택
    return df[preprocessing_info['features']]

# 입력 폼 생성
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        pclass = st.selectbox("승객 등급", [1, 2, 3], help="1: 1등석, 2: 2등석, 3: 3등석")
        sex = st.selectbox("성별", ["male", "female"])
        age = st.number_input("나이", min_value=0, max_value=100, value=30)
        sibsp = st.number_input("동반 형제/자매 수", min_value=0, max_value=10, value=0)
    
    with col2:
        parch = st.number_input("동반 부모/자식 수", min_value=0, max_value=10, value=0)
        fare = st.number_input("요금", min_value=0.0, max_value=500.0, value=50.0)
        embarked = st.selectbox("탑승 항구", ["C", "Q", "S"], 
                              help="C: Cherbourg, Q: Queenstown, S: Southampton")
    
    submitted = st.form_submit_button("생존 여부 예측하기")

if submitted:
    # 입력 데이터 준비
    input_data = {
        "Pclass": pclass,
        "Sex": sex,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
        "Embarked": embarked
    }
    
    # 전처리
    processed_data = preprocess_input(input_data)
    
    # 예측
    # 퍼센트로 (확률, 0-1) 
    prediction = model.predict(processed_data)[0]           # 범주 예측
    probability = model.predict_proba(processed_data)[0]    # predict_proba 확률
    
    # 결과 표시
    st.markdown("---")
    st.subheader("예측 결과")
    
    if prediction == 1:
        st.success("생존 가능성이 높습니다! 🎉")
    else:
        st.error("생존 가능성이 낮습니다. 😢")
    
    # 생존 확률 표시
    st.metric("생존 확률", f"{probability[1]*100:.1f}%")

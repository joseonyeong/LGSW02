import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

## 페이지 설정
st.set_page_config(
    page_title='Titanic Survival Prediction',
    layout='wide'
)

st.title("Titanic Main page, Dashboard")

## 데이터 불러오기
@st.cache_data  # 데이터 불러올 땐 무조건 있어야 함
def load_data():
    train = pd.read_csv('train.csv')
    # 추가로 이곳에서 데이터 처리 (불필요한 컬럼 제거 등)을 할 수 있음
    # 추가로 local에서가 아닌 sql에서 수집하는 방법 작성 
    return train

train = load_data()
# st.dataframe(train) # 확인용

## 탭 생성
tab1, tab2, tab3 = st.tabs(['EDA', 'Statistics', 'Prediction'])

# EDA 탭
with tab1:
    st.header("Exploratory Data Analysis")
    
    # 데이터 미리보기
    st.subheader("Data Preview")
    st.dataframe(train.head())
    
    # 생존자 분포
    st.subheader("Survival Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=train, x='Survived')
    plt.title("Survival Count")
    st.pyplot(fig)
    
    # 성별별 생존율
    st.subheader("Survival Rate by Gender")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=train, x='Sex', y='Survived')
    plt.title("Survival Rate by Gender")
    st.pyplot(fig)
    
    # 객실 등급별 생존율
    st.subheader("Survival Rate by Passenger Class")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=train, x='Pclass', y='Survived')
    plt.title("Survival Rate by Passenger Class")
    st.pyplot(fig)

# Statistics 탭
with tab2:
    st.header("Statistical Analysis")
    
    # 기본 통계량
    st.subheader("Basic Statistics")
    st.dataframe(train.describe())
    
    # 상관관계 분석
    st.subheader("Correlation Analysis")
    numeric_cols = train.select_dtypes(include=['int64', 'float64']).columns
    corr = train[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    # 결측치 분석
    st.subheader("Missing Values Analysis")
    missing_data = pd.DataFrame({
        'Missing Values': train.isnull().sum(),
        'Percentage': (train.isnull().sum() / len(train)) * 100
    })
    st.dataframe(missing_data)

with tab3:
    st.header('예측')    

    @st.cache_resource # 세션과 관련 있는 데코레이터
    def load_model():
        return joblib.load('titanic_stacking_model.pkl')
    
    model = load_model()
    # st.write(model)

    ## 입력 폼
    st.subheader('고객 정보 입력')
    
    # col1, col2 = st.columns(2)

    # # 입력값 기준점은 train.csv 파일 기준에 작성
    # with col1:
    #     pclass = st.selectbox('Passenger Class', [1,2,3])
    # with col2:
    #     fare = st.number_input('Fare', min_value=0.0, max_value=500.0, value=50.0)
    
    # if st.button('Predict Survival'):
    #     input_data = pd.DataFrame({
    #         'Pclass': [pclass],
    #         'Fare': [fare]
    #     })
    #     st.dataframe(input_data)
    #     model.predict(input_data)
    col1, col2 = st.columns(2)
    
    with col1:
        pclass = st.selectbox("Passenger Class", [1, 2, 3])
        sex = st.selectbox("Sex", ["male", "female"])
        age = st.number_input("Age", min_value=0, max_value=100, value=30)
        
    with col2:
        sibsp = st.number_input("Number of Siblings/Spouses", min_value=0, max_value=10, value=0)
        parch = st.number_input("Number of Parents/Children", min_value=0, max_value=10, value=0)
        fare = st.number_input("Fare", min_value=0.0, max_value=500.0, value=50.0)
        embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"])
    
    # 예측 버튼
    if st.button("Predict Survival"):
        # 입력 데이터 준비
        input_data = pd.DataFrame({
            'Pclass': [pclass],
            'Sex': [sex],
            'Age': [age],
            'SibSp': [sibsp],
            'Parch': [parch],
            'Fare': [fare],
            'Embarked': [embarked]
        })
        
        # 예측
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        # 결과 표시
        st.subheader("Prediction Result")
        if prediction == 1:
            st.success(f"Survival Probability: {probability:.2%}")
            st.write("The passenger is predicted to survive.")
        else:
            st.error(f"Survival Probability: {probability:.2%}")
            st.write("The passenger is predicted to not survive.")

    
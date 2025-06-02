import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, StackingClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, roc_auc_score
import xgboost as xgb
import lightgbm as lgb
import joblib
import os
from datetime import datetime

# 1. 데이터 로드
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# 2. 주요 변수 선택 (예시)
main_features = [
    'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked'
]

# 3. 피처/타겟 분리
X = train[main_features]
y = train['Survived']
X_test = test[main_features]

# 4. 훈련/검증 분리
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. 전처리 파이프라인 (결측치 처리 포함)
numeric_feats = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_feats = X_train.select_dtypes(include=['object']).columns.tolist()

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_feats),
    ('cat', categorical_transformer, categorical_feats)
])

# 6. Base 모델 정의
base_estimators = [
    ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
    ('xgb', xgb.XGBClassifier(n_estimators=100, max_depth=3, tree_method='hist', random_state=42, use_label_encoder=False, eval_metric='logloss')),
    ('lgb', lgb.LGBMClassifier(n_estimators=100, max_depth=3, random_state=42))
]

# 7. Stacking 앙상블 (파이프라인 포함)
stacking = StackingClassifier(
    estimators=[(name, Pipeline([('pre', preprocessor), (name, model)])) for name, model in base_estimators],
    final_estimator=GradientBoostingClassifier(n_estimators=100, random_state=42),
    cv=5,
    n_jobs=-1,
    passthrough=False
)

# 8. 학습
stacking.fit(X_train, y_train)

# 9. 검증 예측 및 평가
val_preds = stacking.predict(X_val)
val_probs = stacking.predict_proba(X_val)[:, 1]

print("검증 정확도:", accuracy_score(y_val, val_preds))
print(classification_report(y_val, val_preds))

# 10. ROC Curve (fig, ax)
fpr, tpr, _ = roc_curve(y_val, val_probs)
auc = roc_auc_score(y_val, val_probs)

fig, ax = plt.subplots(figsize=(6, 5))
ax.plot(fpr, tpr, label=f'Stacking (AUC={auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', label='Random')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve - Titanic Survival (Stacking)')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()

# 11. Test 데이터 예측 및 제출 파일 생성
test_preds = stacking.predict(X_test)
submission = pd.DataFrame({
    'PassengerId': test['PassengerId'],
    'Survived': test_preds
})

# 12. 모델 내보내기
model_path = "titanic_stacking_model.pkl"
os.makedirs("models", exist_ok=True)
with open(model_path, "wb") as f:
    joblib.dump(stacking, f)

print(f"모델이 {model_path}에 저장되었습니다.")



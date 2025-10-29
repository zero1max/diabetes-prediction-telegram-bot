import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib


# 1. Ma'lumotni yuklash
df = pd.read_csv("diabetes.csv")  # shu fayl loyihang papkasida bo‘lishi kerak

# 2. X va y
X = df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
        'BMI', 'DiabetesPedigreeFunction', 'Age']]
y = df['Outcome']

# 3. Train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Skalalash
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 5. Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# 6. Saqlash
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model va scaler fayllar saqlandi!")

def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age):
    new_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    new_data_scaled = scaler.transform(new_data)
    
    prediction = model.predict(new_data_scaled)
    probability = model.predict_proba(new_data_scaled)[0][1]
    
    result = "Diabet bor" if prediction[0] == 1 else "Diabet yo‘q"
    return result, round(probability, 3)
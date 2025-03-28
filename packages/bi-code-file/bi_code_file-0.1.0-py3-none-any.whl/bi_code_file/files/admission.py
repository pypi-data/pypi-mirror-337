import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data = pd.read_csv("./dataset/admission.csv")

features = data[['gre', 'gpa', 'rank']]
target = data['admit']

X_train, X_test, y_train, y_test = train_test_split(features, target, 
                                                   test_size=0.3, 
                                                   random_state=1)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.1f}")

new_student = pd.DataFrame({'gre': [260], 'gpa': [2.67], 'rank': [1]})
prediction = model.predict(new_student)

print("\nNew Student Details:")
print(new_student)
print(f"\nAdmission Forecast: {prediction[0]}")

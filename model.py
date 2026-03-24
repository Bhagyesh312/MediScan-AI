import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.calibration import CalibratedClassifierCV
import joblib
import warnings

warnings.filterwarnings("ignore")

df = pd.read_excel("dataset.xlsx")

le = LabelEncoder()
df['prognosis'] = le.fit_transform(df['prognosis'])

X = df.drop('prognosis', axis=1)
y = df['prognosis']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Found {len(le.classes_)} diseases. Example classes: {le.classes_[:8]}")
print("Class distribution (disease:count) sample:", list(df['prognosis'].value_counts().items())[:8])

rf_params = {
    'n_estimators': [100, 150],
    'max_depth': [8, 10, None],
    'min_samples_split': [2, 4]
}
rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=3, n_jobs=-1)
rf_grid.fit(X_train, y_train)
print("Best params for RandomForestClassifier ->", rf_grid.best_params_)
rf_best = rf_grid.best_estimator_

gb_params = {
    'n_estimators': [100, 150],
    'max_depth': [3]
}
gb_grid = GridSearchCV(GradientBoostingClassifier(random_state=42), gb_params, cv=3, n_jobs=-1)
gb_grid.fit(X_train, y_train)
print("Best params for GradientBoostingClassifier ->", gb_grid.best_params_)
gb_best = gb_grid.best_estimator_

et_params = {
    'n_estimators': [100, 150],
    'max_depth': [None, 10]
}
et_grid = GridSearchCV(ExtraTreesClassifier(random_state=42), et_params, cv=3, n_jobs=-1)
et_grid.fit(X_train, y_train)
print("Best params for ExtraTreesClassifier ->", et_grid.best_params_)
et_best = et_grid.best_estimator_

voting = VotingClassifier(
    estimators=[('rf', rf_best), ('gb', gb_best), ('et', et_best)],
    voting='soft'
)
voting.fit(X_train, y_train)
print("Voting ensemble trained successfully.")

calibrated = CalibratedClassifierCV(estimator=voting, method='isotonic', cv=3)
calibrated.fit(X_train, y_train)

y_pred = calibrated.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nFinal Model Accuracy: {acc * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

joblib.dump(calibrated, 'disease_model.pkl')
joblib.dump(le, 'label_encoder.pkl')

print("\n✅ Model and label encoder saved successfully!")

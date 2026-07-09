import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# dataset load
df = pd.read_csv('core/ml/Crop_recommendation.csv')

# features
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]

# target
y = df['label']

# Random Forest Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# train
model.fit(X, y)

# save model
pickle.dump(model, open('core/ml/model.pkl', 'wb'))

print("Random Forest model trained successfully!")
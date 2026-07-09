import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Dataset load
df = pd.read_csv("core/ml/crop_production.csv")

# Missing values hatao
df = df.dropna()

# Yield calculate karo
df['Yield'] = df['Production'] / df['Area']

# Area 0 wale rows hatao
df = df[df['Area'] > 0]

# Label Encoding
state_encoder = LabelEncoder()
district_encoder = LabelEncoder()
season_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df['State_Name'] = state_encoder.fit_transform(df['State_Name'])
df['District_Name'] = district_encoder.fit_transform(df['District_Name'])
df['Season'] = season_encoder.fit_transform(df['Season'])
df['Crop'] = crop_encoder.fit_transform(df['Crop'])

# Features
X = df[['State_Name',
        'District_Name',
        'Season',
        'Crop',
        'Area']]

# Target
y = df['Yield']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("core/ml/yield_model.pkl", "wb"))

# Encoders bhi save karo
pickle.dump(state_encoder, open("core/ml/state_encoder.pkl", "wb"))
pickle.dump(district_encoder, open("core/ml/district_encoder.pkl", "wb"))
pickle.dump(season_encoder, open("core/ml/season_encoder.pkl", "wb"))
pickle.dump(crop_encoder, open("core/ml/crop_encoder.pkl", "wb"))

print("Yield model trained successfully!")
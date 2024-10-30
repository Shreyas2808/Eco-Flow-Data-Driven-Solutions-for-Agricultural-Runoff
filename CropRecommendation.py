import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib  # To save and load the model

# Step 1: Load the dataset
df = pd.read_csv('final_commercial_crops_karnataka.csv', encoding='latin-1')

# Step 2: Prepare the data for training
X = pd.get_dummies(df[['Family', 'Fertilizer Used', 'Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']], drop_first=True)
y = df['Crop Name']

# Optional: Scale numerical features
scaler = StandardScaler()
X[['Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']] = scaler.fit_transform(X[['Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']])

# Step 3: Train the model and save it
model = RandomForestClassifier(random_state=42)
model.fit(X, y)
joblib.dump(model, 'crop_model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for consistent preprocessing

# Step 4: Define the prediction function
def recommend_crop(family, fertilizer, nitrogen, phosphorus, potassium):
    # Load the trained model and scaler
    model = joblib.load('crop_model.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Family': [family],
        'Fertilizer Used': [fertilizer],
        'Nitrogen (N) (%)': [nitrogen],
        'Phosphorus (P) (%)': [phosphorus],
        'Potassium (K) (%)': [potassium]
    })
    input_data = pd.get_dummies(input_data, drop_first=True)
    input_data = input_data.reindex(columns=X.columns, fill_value=0)

    # Scale the data
    input_data[['Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']] = scaler.transform(input_data[['Nitrogen (N) (%)', 'Phosphorus (P) (%)', 'Potassium (K) (%)']])

    # Predict and return the recommended crop
    recommended_crop = model.predict(input_data)
    return recommended_crop[0]

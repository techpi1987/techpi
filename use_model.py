import pickle
import numpy as np

# Load the saved model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the saved scaler
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Example: Make a prediction with new data
# Replace this with your actual data
new_data = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example iris flower measurements

# Preprocess the new data using the saved scaler
new_data_scaled = scaler.transform(new_data)

# Make prediction
prediction = model.predict(new_data_scaled)

print("Prediction:", prediction)
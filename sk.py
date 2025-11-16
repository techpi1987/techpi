from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np
import pickle

# Load sample dataset (iris dataset)
print("Loading dataset...")
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train the model
print("Training model...")
model = SVC(kernel='linear')
model.fit(X_train_scaled, y_train)

# Save the model to a file
print("Saving model to file...")
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Save the scaler too (important for preprocessing new data)
print("Saving scaler to file...")
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("\nFiles saved successfully!")

# Example of loading and using the saved model
print("\nTesting saved model...")
# Load the model
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Load the scaler
with open('scaler.pkl', 'rb') as file:
    loaded_scaler = pickle.load(file)

# Test the loaded model
# Preprocess the test data using loaded scaler
X_test_scaled = loaded_scaler.transform(X_test)

# Make predictions using loaded model
predictions = loaded_model.predict(X_test_scaled)

# Calculate accuracy
accuracy = (predictions == y_test).mean()
print(f"\nLoaded Model Accuracy: {accuracy * 100:.2f}%")

# Show sample predictions
print("\nSample Predictions:")
print("Actual vs Predicted")
print("-" * 20)
for actual, predicted in zip(y_test[:5], predictions[:5]):
    print(f"Actual: {iris.target_names[actual]}")
    print(f"Predicted: {iris.target_names[predicted]}\n")
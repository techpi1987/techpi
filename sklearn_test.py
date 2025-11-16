from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np

# Load sample dataset (iris dataset)
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train the model
model = SVC(kernel='linear')
model.fit(X_train_scaled, y_train)

# Make predictions
predictions = model.predict(X_test_scaled)

# Calculate accuracy
accuracy = (predictions == y_test).mean()
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Print sample predictions
print("\nSample Predictions:")
print("Actual vs Predicted")
print("-" * 20)
for actual, predicted in zip(y_test[:5], predictions[:5]):
    print(f"Actual: {iris.target_names[actual]}")
    print(f"Predicted: {iris.target_names[predicted]}\n")
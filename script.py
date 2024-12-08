import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Step 1: Load and preprocess the data
data = pd.read_csv("Data.csv")

# Handle missing values
data.fillna(0, inplace=True)

# One-hot encode categorical columns
categorical_cols = ["Town", "Type", "Sale/Rent"]
encoder = OneHotEncoder(sparse=False)
encoded_features = encoder.fit_transform(data[categorical_cols])

# Standardize numeric columns
numeric_cols = ["Amount of Rooms", "Surface Area", "Floor/Floors"]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[numeric_cols])

# Combine processed features
X = np.hstack((encoded_features, scaled_features))

# Target variable
y = data["Price"].str.replace("€", "").str.replace(",", "").astype(float)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Build the neural network
model = Sequential([
    Dense(128, input_dim=X_train.shape[1], activation='relu'),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')  # Regression output
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Step 3: Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Step 4: Evaluate the model
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error on test set: {mae}")

# Save the model
model.save("property_price_predictor.h5")

# Make predictions
def predict_price(input_data):
    # Preprocess input data (encode, scale)
    encoded_input = encoder.transform([input_data[:3]])
    scaled_input = scaler.transform([input_data[3:]])
    final_input = np.hstack((encoded_input, scaled_input))
    
    # Predict price
    predicted_price = model.predict(final_input)
    return predicted_price[0][0]

# Example usage
example_data = ["Tallinn", "Apartment", "For Sale", 3, 75.0, 5]
predicted_price = predict_price(example_data)
print(f"Predicted price: €{predicted_price:.2f}")

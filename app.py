from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input from form
    year = int(request.form['year'])
    km_driven = int(request.form['km_driven'])
    fuel_type = request.form['fuel_type']  # 'Petrol', 'Diesel', etc.

    # Convert fuel type to numeric (simple encoding)
    if fuel_type.lower() == 'petrol':
        fuel = 0
    elif fuel_type.lower() == 'diesel':
        fuel = 1
    else:
        fuel = 2

    # Predict
    input_features = np.array([[year, km_driven, fuel]])
    prediction = model.predict(input_features)[0]

    return render_template('index.html', prediction_text=f"Estimated Price: ₹{round(prediction, 2)}")

if __name__ == "_main_":
    app.run(debug=True)
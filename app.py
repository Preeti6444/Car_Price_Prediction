from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    year = int(request.form['year'])
    kms_driven = int(request.form['kms_driven'])
    fuel_type = request.form['fuel_type']
    transmission = request.form['transmission']
    owner = request.form['owner']
    car_type = request.form['type']
    company = request.form['company']

    fuel_map = {'petrol': 0, 'diesel': 1, 'cng': 2, 'lpg': 3, 'electric': 4}
    transmission_map = {'manual': 0, 'automatic': 1}
    owner_map = {'first': 0, 'second': 1, 'third': 2, 'fourth & above': 3}
    type_map = {'hatchback': 0, 'sedan': 1, 'suv': 2, 'muv': 3, 'convertible': 4}
    company_map = {'maruti': 0, 'hyundai': 1, 'honda': 2, 'toyota': 3, 'ford': 4, 'bmw': 5, 'audi': 6}

    fuel = fuel_map.get(fuel_type.lower(), 0)
    transmission = transmission_map.get(transmission.lower(), 0)
    owner = owner_map.get(owner.lower(), 0)
    car_type = type_map.get(car_type.lower(), 0)
    company = company_map.get(company.lower(), 0)

    input_features = np.array([[year, kms_driven, fuel, transmission, owner, car_type, company]])
    print("input_features.shape =", input_features.shape)

    prediction = round(model.predict(input_features)[0],2)
    return render_template('index.html', prediction_text=f"Estimated Price: ₹{prediction} Lakhs")

if __name__ == "__main__":
    app.run(debug=True)
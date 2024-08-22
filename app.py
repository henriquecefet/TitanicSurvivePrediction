from flask import Flask, request, jsonify, send_from_directory, render_template, make_response, session, redirect, url_for
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
import pandas as pd
import joblib
import traceback
import mysql.connector
from mysql.connector import Error
app = Flask(__name__, static_folder='static')


@app.route('/')
def login_page():
    return render_template('generalmodel.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load the model
        pipeline = joblib.load('modelo_titanic.pkl')

        # Carregar os LabelEncoders
        label_encoders = {
            'Embarked': joblib.load('label_encoder_Embarked.pkl'),
            'Sex': joblib.load('label_encoder_Sex.pkl'),
        }

        # Define as colunas numéricas e categóricas
        categorical_columns = ['Sex', 'Embarked']
        numerical_columns = ['Pclass', 'Age', 'Fare']
        # Get the JSON data from the request
        data = request.json
        
        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data, index=[0])
        
        # Apply label encoding to categorical columns
        for name, le in label_encoders.items():
            try:
                df[name] = le.transform(df[name])
            except ValueError as e:
                return jsonify({'error': f"Unknown category in column '{name}': {str(e)}"}), 400
        
        # Convert all non-categorical columns to float
        for column in numerical_columns:
            df[column] = df[column].astype(float)
        
        # Print column types for debugging
        for column in df.columns:
            print(f"Column '{column}' has type: {type(df[column].iloc[0])}")
        
        # Select features for prediction
        X = df[numerical_columns + categorical_columns]
        
        # Print the transformed DataFrame for debugging
        print(X)
        
        y_pred = pipeline.predict(X)
        print("-----------------------------------------------------------")
        print(y_pred.tolist())
        # Return the predictions as JSON
        return jsonify({'prediction': y_pred.tolist()[0]})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        full_error_message = f"{error_message}\nTraceback:\n{traceback_str}"
        print(full_error_message)
        return jsonify(error=full_error_message), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)

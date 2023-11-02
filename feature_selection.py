
!pip install scikit-learn

import streamlit as st
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.title("Feature Selection for Predicting Requests")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure 'requests' is in the DataFrame
    if 'requests' not in df.columns:
        st.error("The 'requests' column is not found in the uploaded file.")
    else:
        # Prepare data
        X = df.drop(columns=['requests'])
        y = df['requests']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Linear Regression model
        model = LinearRegression()

        # Recursive Feature Elimination
        rfe = RFE(model, n_features_to_select=1)
        fit = rfe.fit(X_train, y_train)

        # Display results
        st.header("Feature Ranking")
        ranked_features = pd.DataFrame({'Feature': X.columns, 'Ranking': fit.ranking_})
        st.write(ranked_features.sort_values(by='Ranking'))

        # Train model with all features
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        st.header("Model Performance (All Features)")
        st.write("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
        st.write("R-squared:", r2_score(y_test, y_pred))

        # Train model with selected features
        selected_features = X.columns[fit.support_].tolist()
        model.fit(X_train[selected_features], y_train)
        y_pred = model.predict(X_test[selected_features])
        st.header("Model Performance (Selected Features)")
        st.write("Selected Features:", selected_features)
        st.write("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
        st.write("R-squared:", r2_score(y_test, y_pred))

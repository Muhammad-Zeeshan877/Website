import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

# Create Firestore database instance
db = firestore.client()

# Streamlit App UI
st.title("MTTF Failure Predictor")
st.subheader("Real-time Failure Predictions")

# Function to save data to Firebase
def save_data(mttf, status):
    doc_ref = db.collection("predictions").document("latest")
    doc_ref.set({"MTTF": mttf, "Status": status})
    st.success("Prediction saved to Firebase!")

# Function to retrieve data from Firebase
def get_data():
    doc_ref = db.collection("predictions").document("latest")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Input form for MTTF Prediction
mttf_value = st.number_input("Enter Predicted MTTF Value:", min_value=1, step=1)
status_value = st.text_input("Enter Status (Running/Failed):")

if st.button("Save Prediction"):
    save_data(mttf_value, status_value)

# Display latest prediction
st.subheader("Latest Prediction from Firebase:")
data = get_data()
if data:
    st.write(f"**MTTF:** {data['MTTF']} hours")
    st.write(f"**Status:** {data['Status']}")
else:
    st.warning("No prediction data available.")

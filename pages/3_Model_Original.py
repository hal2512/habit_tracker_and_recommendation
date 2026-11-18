import streamlit as st
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Model A: Original", page_icon="🧠")

st.title("🧠 Model A: The 'Weak' Guardian")
st.markdown("This model was trained on **only 90 days** of data.")

try:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model = joblib.load(os.path.join(base_dir, 'models', 'guardian_original.joblib'))
    features = joblib.load(os.path.join(base_dir, 'models', 'guardian_original_features.joblib'))
except:
    st.error("Model A not found. Run `train_guardian.py`.")
    st.stop()

st.subheader("Model Architecture")
st.code("Pipeline(StandardScaler + IsolationForest(n_estimators=100))", language="python")

st.warning("""
**Limitation:** Because this model has seen very few examples of 'Burnout', it might over-react 
or miss subtle signs. It hasn't learned the full complexity of student life.
""")
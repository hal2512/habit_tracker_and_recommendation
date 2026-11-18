import streamlit as st
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Model B: Augmented", page_icon="🚀")

st.title("🚀 Model B: The 'Smart' Guardian")
st.markdown("This model was trained on **1000+ days** of comprehensive data.")

try:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model = joblib.load(os.path.join(base_dir, 'models', 'guardian_augmented.joblib'))
except:
    st.error("Model B not found. Run `train_guardian.py`.")
    st.stop()

st.subheader("Why this model is better")
st.success("""
**Robustness:** With 3 years of data, this model understands that one bad night of sleep 
isn't always an emergency. It detects *patterns* rather than just single events.
""")

st.metric("Training Samples", "1000+")
st.metric("Contamination Factor", "0.05 (5%)")
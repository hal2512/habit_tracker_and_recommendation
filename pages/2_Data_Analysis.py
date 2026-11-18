import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Data Analysis", page_icon="📊")

st.title("📊 Data Analysis: Real vs. Augmented")
st.markdown("Comparing the **Original (Small)** dataset with the **Augmented (Big)** dataset.")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df_orig = pd.read_csv(os.path.join(base_dir, 'data', 'original_data.csv'))
    df_aug = pd.read_csv(os.path.join(base_dir, 'data', 'augmented_data.csv'))
    return df_orig, df_aug

try:
    df_orig, df_aug = load_data()
except FileNotFoundError:
    st.error("Data not found. Please run `generate_data.py` first.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.info(f"**Original Data**\n\nRows: {len(df_orig)}\n\nSimulates 3 months of manual logging.")
with col2:
    st.success(f"**Augmented Data**\n\nRows: {len(df_aug)}\n\nSimulates 3 years of synthetic history.")

st.divider()

st.subheader("📉 Distribution Comparison: Sleep Hours")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(df_orig['sleep_hours'], bins=15, kde=True, ax=ax[0], color='blue')
ax[0].set_title("Original (Small Data)")

sns.histplot(df_aug['sleep_hours'], bins=15, kde=True, ax=ax[1], color='green')
ax[1].set_title("Augmented (Big Data)")

st.pyplot(fig)

st.caption("Notice how the Augmented data provides a smoother 'bell curve', allowing the AI to learn better boundaries.")
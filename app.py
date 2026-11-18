import streamlit as st
import pandas as pd
import joblib
import os
from recommender import BurnoutRecommender

st.set_page_config(
    page_title="Habit Tracker with AI",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def load_brain():
    try:
        model = joblib.load('models/guardian_augmented.joblib')
        features = joblib.load('models/guardian_augmented_features.joblib')
        return model, features
    except FileNotFoundError:
        return None, None


model, feature_names = load_brain()
recommender = BurnoutRecommender()

st.sidebar.header("📝 Log Daily Habits")


def user_input_features():
    sleep = st.sidebar.slider("Sleep (Hours)", 0.0, 12.0, 7.0, 0.5)
    study = st.sidebar.slider("Study/Productivity (Hours)", 0.0, 16.0, 4.0, 0.5)
    social = st.sidebar.slider("Social Time (Hours)", 0.0, 10.0, 2.0, 0.5)
    screen = st.sidebar.slider("Screen Time (Hours)", 0.0, 16.0, 3.0, 0.5)
    water = st.sidebar.slider("Water (Glasses)", 0, 15, 5, 1)
    exercise = st.sidebar.slider("Exercise (Minutes)", 0, 120, 30, 5)
    skipped_meals = st.sidebar.selectbox("Skipped Meals", [0, 1, 2, 3])

    data = {
        'sleep_hours': sleep,
        'study_hours': study,
        'social_hours': social,
        'screen_hours': screen,
        'water_glasses': water,
        'exercise_minutes': exercise,
        'skipped_meals': skipped_meals
    }
    return pd.DataFrame([data])


input_df = user_input_features()

st.title("📊 Habit Tracker with AI Insights")
st.markdown("### Track your routine. Detect anomalies. Optimize performance.")
st.markdown(
    "This system uses **AI Anomaly Detection** to analyze your daily logs. It flags unusual patterns (like burnout risks or irregular sleep) and provides smart recommendations.")

st.divider()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🔍 Daily Insight")

    if st.button("Analyze My Day", type="primary"):
        if model:
            prediction = model.predict(input_df)[0]

            if prediction == 1:
                st.success("## ✅ Status: On Track")
                st.metric("Pattern Stability", "Normal", delta="Stable")
                st.info("Your habits today align with your healthy baseline. Keep it up!")
                is_risk = False
            else:
                st.warning("## ⚠️ Insight: Irregular Pattern")
                st.metric("Pattern Stability", "Deviation Detected", delta="- Alert", delta_color="inverse")
                st.write(
                    "**Analysis:** Your habits today deviate significantly from your goal baseline. This often indicates stress or potential burnout.")
                is_risk = True

            with col2:
                st.subheader("💡 AI Recommendations")
                current_stats = input_df.iloc[0].to_dict()
                advice_list = recommender.get_recommendations(current_stats, is_risk)

                for tip in advice_list:
                    st.chat_message("assistant").write(tip)

        else:
            st.error("Model not found! Did you run `train_guardian.py`?")

# --- Footer ---
st.markdown("---")
st.caption("AI Model: Isolation Forest (Unsupervised Learning) | Features: Sleep, Study, Social, Health Metrics")
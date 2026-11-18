import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs('data', exist_ok=True)


def generate_student_data(days, seed=42):
    np.random.seed(seed)
    data = []
    start_date = datetime.today() - timedelta(days=days)

    print(f"Generating data for {days} days...")

    for i in range(days):
        current_date = start_date + timedelta(days=i)

        # 5% chance of a "Burnout/Crisis" day (Anomaly)
        is_burnout = np.random.random() < 0.05

        if is_burnout:
            sleep = np.random.normal(4.0, 0.5)  # Sleep deprivation
            study = np.random.normal(10.5, 1.0)  # Cramming
            social = np.random.normal(0.2, 0.1)  # Isolation
            screen = np.random.normal(6.0, 1.0)  # Doomscrolling
            water = np.random.normal(2.0, 1.0)  # Dehydration
            exercise = 0  # No movement
            skipped_meals = np.random.choice([2, 3])  # Skipping meals

            label = -1  # Anomaly tag
        else:
            # 🟢 HEALTHY/NORMAL PATTERN (The Baseline)
            sleep = np.random.normal(7.5, 0.8)
            study = np.random.normal(4.5, 1.5)
            social = np.random.normal(2.0, 0.8)
            screen = np.random.normal(3.0, 0.8)
            water = np.random.normal(7.0, 1.5)
            exercise = np.random.normal(30.0, 15.0)
            skipped_meals = np.random.choice([0, 1], p=[0.8, 0.2])

            label = 1  # Normal tag

        # Clean up data (no negative numbers)
        sleep = max(0, round(sleep, 1))
        study = max(0, round(study, 1))
        social = max(0, round(social, 1))
        screen = max(0, round(screen, 1))
        water = max(0, int(round(water)))
        exercise = max(0, int(round(exercise)))

        data.append([current_date.date(), sleep, study, social, screen, water, exercise, skipped_meals, label])

    cols = ['date', 'sleep_hours', 'study_hours', 'social_hours', 'screen_hours', 'water_glasses', 'exercise_minutes',
            'skipped_meals', 'true_label']
    df = pd.DataFrame(data, columns=cols)
    return df


if __name__ == "__main__":
    #  Generate "Original" Data (Small - 90 days, simulating manual entry)
    df_orig = generate_student_data(days=90, seed=42)
    df_orig.to_csv('data/original_data.csv', index=False)
    print(f" Created 'data/original_data.csv' ({len(df_orig)} rows)")

    #  Generate "Augmented" Data (Large - 1000 days, simulating AI synthetic data)
    df_aug = generate_student_data(days=1000, seed=999)
    df_aug.to_csv('data/augmented_data.csv', index=False)
    print(f" Created 'data/augmented_data.csv' ({len(df_aug)} rows)")

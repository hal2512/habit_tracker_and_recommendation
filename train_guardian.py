import pandas as pd
import joblib
import os
from preprocessing import create_guardian_pipeline  # Importing your custom module

# Create models directory
os.makedirs('models', exist_ok=True)


def train_and_save(data_path, model_name):
    print(f"\n Starting training for: {model_name}")

    # 1. Load Data
    try:
        df = pd.read_csv(data_path)
        print(f"   ...Loaded data from {data_path} ({len(df)} rows)")
    except FileNotFoundError:
        print(f" Error: File {data_path} not found.")
        return

    # 2. Select Features
    features = [
        'sleep_hours', 'study_hours', 'social_hours',
        'screen_hours', 'water_glasses', 'exercise_minutes',
        'skipped_meals'
    ]
    X = df[features]

    # 3. Get the Pipeline (Using the imported logic)
    print("   ...Initializing Pipeline (Scaler + IsolationForest)")
    pipeline = create_guardian_pipeline(contamination=0.05)

    # 4. Train
    print("   ...Fitting model to data")
    pipeline.fit(X)

    # 5. Save
    joblib.dump(pipeline, f'models/{model_name}.joblib')
    joblib.dump(features, f'models/{model_name}_features.joblib')
    print(f" Saved to models/{model_name}.joblib")


if __name__ == "__main__":
    # Train Model A: Original (Small Data)
    train_and_save('data/original_data.csv', 'guardian_original')

    # Train Model B: Augmented (Big Data)
    train_and_save('data/augmented_data.csv', 'guardian_augmented')

    print("\n All models trained successfully using Modular Architecture!")
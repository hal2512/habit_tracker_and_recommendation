from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def create_guardian_pipeline(contamination=0.05):
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', IsolationForest(n_estimators=100,
                                  contamination=contamination,
                                  random_state=42))
    ])

    return pipeline
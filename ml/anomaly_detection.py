import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    """
    Unsupervised anomaly detection using Isolation Forest
    """

    features = df[["amount"]].copy()

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(features)

    
    anomalies = df[df["anomaly"] == -1]

    return anomalies[["transaction_id"]]

import pandas as pd

def detect_duplicate_payments(df):
    duplicates = df[df.duplicated(
        subset=["vendor", "amount", "date"],
        keep=False
    )]
    return duplicates

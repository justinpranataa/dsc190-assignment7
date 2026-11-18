"""Add duration_minutes and weekday columns."""

import sys
from pathlib import Path

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()
    return df


def main(in_path: str, out_path: str) -> None:
    df = pd.read_csv(in_path)
    result = add_features(df)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_path, index=False)
    print(f"features: {len(result)} rows -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

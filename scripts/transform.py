"""Add a date column (YYYY-MM-DD) taken from the timestamp."""

import sys
from pathlib import Path

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")
    return df


def main(in_path: str, out_path: str) -> None:
    df = pd.read_csv(in_path)
    result = transform(df)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_path, index=False)
    print(f"transform: {len(result)} rows -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

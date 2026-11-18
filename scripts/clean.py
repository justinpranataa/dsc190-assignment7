"""Clean the raw events file.

Drops rows with missing fields, an invalid event_type, or a non-positive
duration_seconds, and normalizes timestamp to ISO 8601 (YYYY-MM-DDTHH:MM:SS).
duration_seconds is written as a whole number.
"""

import sys
from pathlib import Path

import pandas as pd

# Event types seen in the provided data. Case variants and typos (VIEW,
# PURCHASE!, klick, log_in, buy, test, unknown) are treated as invalid.
VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

COLUMNS = ["user_id", "timestamp", "event_type", "duration_seconds"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Keep only the expected columns, in order.
    df = df[COLUMNS]

    # Drop rows with any missing field (empty strings count as missing).
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(subset=COLUMNS)

    # Drop rows with an invalid event_type.
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Drop rows whose duration is not a positive number.
    duration = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[duration.notna() & (duration > 0)].copy()
    df["duration_seconds"] = duration[df.index].round().astype("int64")

    # Normalize timestamps to ISO 8601. Rows whose timestamp cannot be parsed
    # are dropped, since they cannot be given a date later in the pipeline.
    parsed = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")
    df = df[parsed.notna()].copy()
    df["timestamp"] = parsed[df.index].dt.strftime("%Y-%m-%dT%H:%M:%S")

    return df.reset_index(drop=True)


def main(in_path: str, out_path: str) -> None:
    raw = pd.read_csv(in_path, dtype=str, keep_default_na=True)
    cleaned = clean(raw)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(out_path, index=False)
    print(f"clean: {len(raw)} rows in, {len(cleaned)} rows out -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

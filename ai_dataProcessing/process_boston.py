#!/usr/bin/env python3

import argparse
import csv
import re
from pathlib import Path
from typing import List


COLUMNS = [
    "CRIM",
    "ZN",
    "INDUS",
    "CHAS",
    "NOX",
    "RM",
    "AGE",
    "DIS",
    "RAD",
    "TAX",
    "PTRATIO",
    "B",
    "LSTAT",
    "MEDV",
]

NUMBER_RE = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _find_first_data_line_index(lines: List[str]) -> int:
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Heuristic: a data line starts with a number and contains multiple numeric tokens.
        if re.match(r"^[-+]?\d", stripped) and len(NUMBER_RE.findall(stripped)) >= 3:
            return idx
    raise ValueError("Could not locate start of numeric data block in input file.")


def parse_boston_txt(text: str) -> List[List[float]]:
    lines = text.splitlines()
    start_idx = _find_first_data_line_index(lines)

    data_text = "\n".join(lines[start_idx:])
    tokens = NUMBER_RE.findall(data_text)
    values = [float(t) for t in tokens]

    n_cols = len(COLUMNS)
    if len(values) % n_cols != 0:
        raise ValueError(
            f"Parsed {len(values)} numeric values, which is not divisible by {n_cols}. "
            "Input format may be unexpected."
        )

    rows = [values[i : i + n_cols] for i in range(0, len(values), n_cols)]
    return rows


def write_csv(rows: List[List[float]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert raw boston.txt to CSV.")
    parser.add_argument(
        "--input",
        default=str(Path("raw_data") / "boston.txt"),
        help="Path to raw boston.txt (default: raw_data/boston.txt)",
    )
    parser.add_argument(
        "--output",
        default=str(Path("data") / "boston.csv"),
        help="Path to output CSV (default: data/boston.csv)",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    text = in_path.read_text(encoding="utf-8", errors="replace")
    rows = parse_boston_txt(text)
    write_csv(rows, out_path)

    print(f"Wrote {len(rows)} rows x {len(COLUMNS)} cols to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

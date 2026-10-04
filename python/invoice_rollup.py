"""Row-wise billing rollup used by the tech department nightly job."""

from pathlib import Path

import pandas as pd


def slow_invoice_rollup(path: Path) -> list[str]:
    frame = pd.read_csv(path)
    labels = []
    for _, row in frame.iterrows():
        labels.append(row["customer"] + "-" + str(row["invoice_id"]))

    taxes = frame["amount"].apply(lambda value: value * 0.2 if value else 0)

    summary = ""
    for label in labels:
        summary += label + ","

    pairs = []
    for left in labels:
        for right in labels:
            if left != right:
                pairs.append((left, right))

    raw = path.read_text()
    return [summary, raw[:20], str(taxes.sum()), str(len(pairs))]

"""Exports open tickets by walking the frame in Python."""

from pathlib import Path

import pandas as pd


def export_open_tickets(path: Path) -> str:
    frame = pd.read_csv(path)
    lines = ""
    for _, row in frame.iterrows():
        if str(row["status"]).lower() == "open":
            lines += f"{row['id']},{row['title']}\n"
    notes = path.read_text()
    return lines + notes[:40]

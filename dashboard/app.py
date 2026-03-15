from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_LOG = DATA_DIR / "log.xml"

app = Flask(__name__, template_folder="templates", static_folder="static")


def _parse_log(xml_path: Path) -> list[dict]:
    if not xml_path.exists():
        return []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    entries: list[dict] = []
    for entry in root.findall("entry"):
        timestamp = (entry.findtext("timestamp") or "").strip()
        level = (entry.findtext("level") or "").strip().upper()
        source = (entry.findtext("source") or "").strip()
        message = (entry.findtext("message") or "").strip()

        parsed_time = None
        if timestamp:
            try:
                parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                parsed_time = None

        entries.append(
            {
                "timestamp": timestamp,
                "parsed_time": parsed_time,
                "level": level,
                "source": source,
                "message": message,
            }
        )

    entries.sort(
        key=lambda row: row["parsed_time"] or datetime.min, reverse=True
    )
    return entries


def _stats(entries: list[dict]) -> dict:
    counts = {"INFO": 0, "WARN": 0, "ERROR": 0, "DEBUG": 0}
    for row in entries:
        if row["level"] in counts:
            counts[row["level"]] += 1
        else:
            counts.setdefault("OTHER", 0)
            counts["OTHER"] += 1

    latest = entries[0]["timestamp"] if entries else None
    return {
        "total": len(entries),
        "counts": counts,
        "latest": latest,
    }


@app.route("/")
def index():
    log_path = request.args.get("log")
    if log_path:
        xml_path = Path(log_path).expanduser()
        if not xml_path.is_absolute():
            xml_path = (DATA_DIR / xml_path).resolve()
    else:
        xml_path = DEFAULT_LOG

    entries = _parse_log(xml_path)
    stats = _stats(entries)

    return render_template(
        "index.html",
        entries=entries,
        stats=stats,
        log_path=str(xml_path),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

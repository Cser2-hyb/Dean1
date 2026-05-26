from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from models.equipment import Equipment

STORAGE_DIR = Path(__file__).resolve().parent
EQUIPMENT_FILE = STORAGE_DIR / "equipment.csv"
EQUIPMENT_HEADERS = ["equipment_id", "power_rating", "name", "hourly_rate", "status"]


def ensure_equipment_file() -> None:
    """Ensure the equipment CSV file exists with the correct header."""
    if not EQUIPMENT_FILE.exists():
        EQUIPMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with EQUIPMENT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=EQUIPMENT_HEADERS)
            writer.writeheader()


def load_equipment() -> List[Equipment]:
    """Load equipment records from the CSV file."""
    ensure_equipment_file()
    equipment = []
    with EQUIPMENT_FILE.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row or not row.get("equipment_id"):
                continue
            equipment.append(Equipment.from_dict(row))
    return equipment


def save_equipment(items: List[Equipment]) -> None:
    """Write equipment records back to the CSV file."""
    ensure_equipment_file()
    with EQUIPMENT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=EQUIPMENT_HEADERS)
        writer.writeheader()
        for item in items:
            writer.writerow(item.to_dict())

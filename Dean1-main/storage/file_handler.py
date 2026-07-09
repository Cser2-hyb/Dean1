from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from models.equipment import Equipment
from models.rental import Rental

STORAGE_DIR = Path(__file__).resolve().parent
EQUIPMENT_FILE = STORAGE_DIR / "equipment.csv"
RENTAL_FILE = STORAGE_DIR / "rentals.csv"
RENTAL_HISTORY_TXT = STORAGE_DIR / "rental_history.txt"
MAINTENANCE_LOG_TXT = STORAGE_DIR / "maintenance_log.txt"

EQUIPMENT_HEADERS = ["equipment_id", "power_rating", "name", "hourly_rate", "status"]
RENTAL_HEADERS = ["rental_id", "client_name", "equipment_ids", "start_time", "expected_return", "actual_return", "status"]

def ensure_equipment_file() -> None:
    """Ensure the equipment CSV file exists with the correct header."""
    if not EQUIPMENT_FILE.exists():
        EQUIPMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with EQUIPMENT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=EQUIPMENT_HEADERS)
            writer.writeheader()

def ensure_storage_files() -> None:
    ensure_equipment_file()
    if not RENTAL_FILE.exists():
        with RENTAL_FILE.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=RENTAL_HEADERS)
            writer.writeheader()
    if not RENTAL_HISTORY_TXT.exists():
        RENTAL_HISTORY_TXT.touch()
    if not MAINTENANCE_LOG_TXT.exists():
        MAINTENANCE_LOG_TXT.touch()

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

def load_rentals() -> List[Dict[str, Any]]:
    ensure_storage_files()
    records = []
    with RENTAL_FILE.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row or not row.get("rental_id"):
                continue
            records.append(row)
    return records

def save_rentals(rentals: List[Rental]) -> None:
    ensure_storage_files()
    with RENTAL_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=RENTAL_HEADERS)
        writer.writeheader()
        for r in rentals:
            writer.writerow(r.to_dict())

def read_log_file(filepath: Path) -> str:
    if not filepath.exists():
        return "(File not found)"
    with filepath.open("r", encoding="utf-8") as f:
        return f.read()

def append_rental_history(rental: Rental, all_equipment: List[Equipment], rental_fee: float, late_penalty: float) -> None:
    ensure_storage_files()
    with RENTAL_HISTORY_TXT.open("a", encoding="utf-8") as f:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now_str}] Rental returned: {rental.rental_id} by {rental.client_name}\n")
        f.write(f"  Fee: {rental_fee}, Late Penalty: {late_penalty}, Total: {rental_fee + late_penalty}\n")
        f.write("-" * 40 + "\n")

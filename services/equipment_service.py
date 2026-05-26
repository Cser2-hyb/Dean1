from __future__ import annotations

from typing import Dict, List, Optional

from models.equipment import Equipment
from storage.file_handler import load_equipment, save_equipment


class EquipmentService:
    """Service layer for working with Equipment records."""

    def __init__(self) -> None:
        self._equipment: Dict[str, Equipment] = {
            item.equipment_id: item for item in load_equipment()
        }

    def list_all(self) -> List[Equipment]:
        return list(self._equipment.values())

    def get(self, equipment_id: str) -> Optional[Equipment]:
        return self._equipment.get(equipment_id.strip())

    def add(self, equipment: Equipment) -> None:
        key = equipment.equipment_id
        if key in self._equipment:
            raise ValueError(f"Equipment with ID {key} already exists")
        self._equipment[key] = equipment
        save_equipment(self.list_all())

    def update(self, equipment_id: str, **changes) -> Equipment:
        existing = self.get(equipment_id)
        if existing is None:
            raise KeyError(f"Equipment with ID {equipment_id} does not exist")

        if "name" in changes:
            existing.name = changes["name"]
        if "power_rating" in changes:
            existing.power_rating = changes["power_rating"]
        if "hourly_rate" in changes:
            existing.hourly_rate = changes["hourly_rate"]
        if "status" in changes:
            existing.status = changes["status"]

        save_equipment(self.list_all())
        return existing

    def find_by_status(self, status: str) -> List[Equipment]:
        status = status.strip()
        return [item for item in self._equipment.values() if item.status == status]

    def save(self) -> None:
        save_equipment(self.list_all())

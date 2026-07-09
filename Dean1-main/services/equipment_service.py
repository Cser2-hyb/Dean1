from __future__ import annotations

from typing import Dict, List, Optional
from models.equipment import Equipment
from storage.file_handler import load_equipment, save_equipment

class EquipmentService:
    """Service layer for working with Equipment records."""

    def __init__(self) -> None:
        self._equipment: List[Equipment] = []

    def load_from_records(self, records: List[Equipment]) -> None:
        self._equipment = records

    def get_all(self) -> List[Equipment]:
        return self._equipment

    def get_summary(self) -> dict:
        total = len(self._equipment)
        available = sum(1 for eq in self._equipment if eq.status == "Available")
        rented = sum(1 for eq in self._equipment if eq.status == "Rented")
        return {"total": total, "available": available, "rented": rented}

    def add_equipment(self, equipment_id: str, name: str, power_rating: float, hourly_rate: float) -> Equipment:
        if self.find_by_id(equipment_id):
            raise ValueError(f"Equipment with ID {equipment_id} already exists")
        eq = Equipment(equipment_id, power_rating, name, hourly_rate)
        self._equipment.append(eq)
        return eq

    def find_by_id(self, equipment_id: str) -> Optional[Equipment]:
        equipment_id = equipment_id.strip()
        for eq in self._equipment:
            if eq.equipment_id == equipment_id:
                return eq
        return None

    def find_by_status(self, status: str) -> List[Equipment]:
        status = status.strip()
        return [eq for eq in self._equipment if eq.status == status]

    def update_equipment(self, equipment_id: str, name: Optional[str] = None, power_rating: Optional[float] = None, hourly_rate: Optional[float] = None) -> Equipment:
        eq = self.find_by_id(equipment_id)
        if not eq:
            raise ValueError(f"Equipment with ID {equipment_id} does not exist")
        
        if name is not None:
            eq.name = name
        if power_rating is not None:
            eq.power_rating = power_rating
        if hourly_rate is not None:
            eq.hourly_rate = hourly_rate
        return eq

    def update_status(self, equipment_id: str, status: str) -> None:
        eq = self.find_by_id(equipment_id)
        if eq:
            eq.status = status

    def group_by_status(self) -> dict:
        groups = {}
        for eq in self._equipment:
            groups.setdefault(eq.status, []).append(eq)
        return groups

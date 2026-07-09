# equipment_ID power_rating : (W), name, hourly_rate : (VND) status
import math
from typing import ClassVar, Set, Dict, Any

class Equipment:
    ALLOWED_STATUSES: ClassVar[Set[str]] = {
        "Available",
        "Rented",
        "Maintenance",
        "Unavailable",
    }

    def __init__(
        self,
        equipment_id: str,
        power_rating: float,
        name: str,
        hourly_rate: float,
        status: str = "Available",
    ) -> None:
        self.equipment_id = equipment_id
        self.power_rating = power_rating
        self.name = name
        self.hourly_rate = hourly_rate
        self.status = status

    # equipment_id
    @property
    def equipment_id(self) -> str:
        return self._equipment_id

    @equipment_id.setter
    def equipment_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("equipment_id must be a string")
        value = value.strip()
        if not value:
            raise ValueError("equipment_id cannot be empty")
        self._equipment_id = value

    # name
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("name cannot be empty")
        self._name = value

    # power_rating (in Watts)
    @property
    def power_rating(self) -> float:
        return self._power_rating

    @power_rating.setter
    def power_rating(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("power_rating must be a number")
        if not math.isfinite(value):
            raise ValueError("power_rating must be a finite number")
        if value < 0:
            raise ValueError("power_rating cannot be negative")
        self._power_rating = float(value)

    # hourly_rate
    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("hourly_rate must be a number")
        if not math.isfinite(value):
            raise ValueError("hourly_rate must be a finite number")
        if value < 0:
            raise ValueError("hourly_rate cannot be negative")
        self._hourly_rate = float(value)

    # status
    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("status must be a string")
        value = value.strip()
        if value not in self.ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {sorted(self.ALLOWED_STATUSES)}")
        self._status = value

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict suitable for CSV/JSON storage."""
        return {
            "equipment_id": self.equipment_id,
            "name": self.name,
            "power_rating": self.power_rating,
            "hourly_rate": self.hourly_rate,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Equipment":
        """Create an Equipment from a dict (tolerant of missing/None keys)."""
        def parse_str(val: Any, default: str = "") -> str:
            if val is None:
                return default
            return str(val).strip()

        def parse_number(val: Any) -> float:
            if val is None:
                return 0.0
            if isinstance(val, bool):
                raise TypeError("numeric fields must be numbers or numeric strings")
            if isinstance(val, str):
                val = val.strip().replace(",", "")
                if not val:
                    return 0.0
            try:
                return float(val)
            except (TypeError, ValueError):
                raise TypeError("numeric fields must be numbers or numeric strings")

        eq_id = parse_str(data.get("equipment_id"), "")
        if not eq_id:
            raise ValueError("from_dict requires a non-empty 'equipment_id'")

        status = parse_str(data.get("status"), "Available")
        if not status:
            status = "Available"

        name = parse_str(data.get("name"), "Unnamed")
        if not name:
            name = "Unnamed"

        return cls(
            equipment_id=eq_id,
            power_rating=parse_number(data.get("power_rating", 0)),
            name=name,
            hourly_rate=parse_number(data.get("hourly_rate", 0)),
            status=status,
        )

    def __repr__(self) -> str:
        return (
            f"Equipment(equipment_id={self.equipment_id!r}, name={self.name!r}, "
            f"power_rating={self.power_rating!r}, hourly_rate={self.hourly_rate!r}, "
            f"status={self.status!r})"
        )
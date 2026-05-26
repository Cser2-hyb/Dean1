# equipment_ID power_rating : (W), name, hourly_rate : (VND) status
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

    # power_rating (in Watts)
    @property
    def power_rating(self) -> float:
        return self._power_rating

    @power_rating.setter
    def power_rating(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("power_rating must be a number")
        if value < 0:
            raise ValueError("power_rating cannot be negative")
        self._power_rating = float(value)

    # hourly_rate
    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("hourly_rate must be a number")
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
            "power_rating": self.power_rating,
            "name": self.name,
            "hourly_rate": self.hourly_rate,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Equipment":
        """Create an Equipment from a dict (tolerant of missing keys)."""
        def parse_number(value: Any) -> float:
            if value is None:
                return 0.0
            if isinstance(value, str):
                value = value.strip().replace(",", "")
                if not value:
                    return 0.0
            try:
                return float(value)
            except (TypeError, ValueError):
                raise TypeError("numeric fields must be numbers or numeric strings")

        status = str(data.get("status", "Available")).strip()
        if not status:
            status = "Available"

        return cls(
            equipment_id=str(data.get("equipment_id", "")).strip(),
            power_rating=parse_number(data.get("power_rating", 0)),
            name=str(data.get("name", "")).strip() or "Unnamed",
            hourly_rate=parse_number(data.get("hourly_rate", 0)),
            status=status,
        )

    def __repr__(self) -> str:
        return (
            f"Equipment(equipment_id={self.equipment_id!r}, name={self.name!r}, "
            f"power_rating={self.power_rating!r}, hourly_rate={self.hourly_rate!r}, "
            f"status={self.status!r})"
        )
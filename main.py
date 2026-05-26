from services.equipment_service import EquipmentService
from models.equipment import Equipment


def main() -> None:
    service = EquipmentService()
    print("Event Equipment Rental & Logistics")
    print("Equipment records loaded:", len(service.list_all()))

    if not service.list_all():
        print("No equipment found. Creating a sample item.")
        sample = Equipment(
            equipment_id="EQ-001",
            power_rating=1500,
            name="Stage Light",
            hourly_rate=120000,
            status="Available",
        )
        service.add(sample)
        print("Sample equipment created and saved.")

    print("Available equipment:")
    for item in service.list_all():
        print(f"- {item.equipment_id}: {item.name} ({item.power_rating}W) {item.status}")


if __name__ == "__main__":
    main()

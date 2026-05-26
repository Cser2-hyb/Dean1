import unittest

from models.equipment import Equipment


class EquipmentModelTests(unittest.TestCase):
    def test_valid_equipment_creation(self):
        equipment = Equipment(
            equipment_id="EQ-100",
            power_rating=2000,
            name="Sound Mixer",
            hourly_rate=150000,
            status="Available",
        )

        self.assertEqual(equipment.equipment_id, "EQ-100")
        self.assertEqual(equipment.power_rating, 2000.0)
        self.assertEqual(equipment.name, "Sound Mixer")
        self.assertEqual(equipment.hourly_rate, 150000.0)
        self.assertEqual(equipment.status, "Available")

    def test_invalid_equipment_id_raises(self):
        with self.assertRaises(ValueError):
            Equipment(
                equipment_id="  ",
                power_rating=100,
                name="Projector",
                hourly_rate=80000,
            )

    def test_negative_hourly_rate_raises(self):
        with self.assertRaises(ValueError):
            Equipment(
                equipment_id="EQ-101",
                power_rating=200,
                name="Projector",
                hourly_rate=-50000,
            )

    def test_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            Equipment(
                equipment_id="EQ-102",
                power_rating=300,
                name="Microphone",
                hourly_rate=10000,
                status="Broken",
            )

    def test_to_dict_from_dict_roundtrip(self):
        equipment = Equipment(
            equipment_id="EQ-200",
            power_rating=220,
            name="Speaker",
            hourly_rate=20000,
            status="Maintenance",
        )
        data = equipment.to_dict()
        reconstructed = Equipment.from_dict(data)

        self.assertEqual(reconstructed.equipment_id, equipment.equipment_id)
        self.assertEqual(reconstructed.power_rating, equipment.power_rating)
        self.assertEqual(reconstructed.name, equipment.name)
        self.assertEqual(reconstructed.hourly_rate, equipment.hourly_rate)
        self.assertEqual(reconstructed.status, equipment.status)

    def test_from_dict_accepts_strings(self):
        raw = {
            "equipment_id": "EQ-201",
            "power_rating": "1800",
            "name": "Fog Machine",
            "hourly_rate": "75000",
            "status": "Rented",
        }
        equipment = Equipment.from_dict(raw)

        self.assertEqual(equipment.equipment_id, "EQ-201")
        self.assertEqual(equipment.power_rating, 1800.0)
        self.assertEqual(equipment.hourly_rate, 75000.0)
        self.assertEqual(equipment.status, "Rented")

    def test_from_dict_strips_status_and_numeric_strings(self):
        raw = {
            "equipment_id": " EQ-202 ",
            "power_rating": " 1,800 ",
            "name": "Fog Machine ",
            "hourly_rate": " 75,000 ",
            "status": " Rented ",
        }
        equipment = Equipment.from_dict(raw)

        self.assertEqual(equipment.equipment_id, "EQ-202")
        self.assertEqual(equipment.power_rating, 1800.0)
        self.assertEqual(equipment.hourly_rate, 75000.0)
        self.assertEqual(equipment.status, "Rented")


if __name__ == "__main__":
    unittest.main()

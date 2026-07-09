# DEVELOPMENT NOTES

## Project structure created

The initial project structure for Event Equipment Rental & Logistics has been created on GitHub.

## Created folders and purpose

### `models/`
Stores OOP model classes.
- `equipment.py`: will contain the `Equipment` class.
- `rental.py`: will contain the `Rental` class.

### `services/`
Stores business logic.
- `equipment_service.py`: add, search, update, and show equipment.
- `rental_service.py`: create rental, return equipment, calculate fee and late penalty.
- `analysis_service.py`: sorting and grouping functions.

### `storage/`
Stores data files and file I/O logic.
- `file_handler.py`: load/save CSV and text logs.
- `equipment.csv`: equipment data.
- `rentals.csv`: rental order data.
- `rental_history.txt`: completed rental history log.
- `maintenance_log.txt`: equipment update/maintenance log.

### `utils/`
Stores helper functions.
- `validators.py`: input validation helpers.
- `time_utils.py`: time parsing and duration helpers.

### `docs/`
Stores final documentation.
- report PDF
- presentation slides
- class diagram
- flowchart
- demo screenshots

## Created root files

### `main.py`
Starter entry point for the console application.

### `README.md`
Project overview, folder explanation, and run command.

### `ROADMAP.md`
Project plan, team roles, timeline, and checklist.

## Next step

Implement the actual code in this order:
1. `models/equipment.py`
2. `models/rental.py`
3. `storage/file_handler.py`
4. `services/equipment_service.py`
5. `services/rental_service.py`
6. `services/analysis_service.py`
7. `utils/validators.py`
8. `utils/time_utils.py`
9. `main.py`

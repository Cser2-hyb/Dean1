"""
main.py
-------
Entry point của chương trình Event Equipment Rental & Logistics.
Chạy chương trình bằng lệnh: python main.py

Cấu trúc menu:
  1. Equipment Management
  2. Rental Management
  3. Data Analysis
  4. View Logs
  5. Save and Exit
"""

import sys
import os
import logging
from typing import Optional

# Thêm thư mục gốc vào sys.path để import các module con
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Đặt stdout sang UTF-8 để hiển thị tiếng Việt trên Windows
if sys.stdout.encoding != "utf-8":
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8")
        except Exception:
            pass

from services.equipment_service import EquipmentService
from services.rental_service import RentalService
from services.analysis_service import AnalysisService
from storage.file_handler import (
    ensure_storage_files,
    load_equipment, load_rentals,
    save_equipment, save_rentals,
    read_log_file,
    RENTAL_HISTORY_TXT, MAINTENANCE_LOG_TXT,
)
from utils.time_utils import format_duration


# ═══════════════════════════════════════════════════════════════════
#  HÀM IN MENU / TIÊU ĐỀ
# ═══════════════════════════════════════════════════════════════════

def print_header(title: str):
    """In tiêu đề đẹp cho từng màn hình."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_separator():
    print("-" * 60)


def pause():
    """Pause until the user is ready to continue."""
    input("\n  [Press Enter to continue...]")


# ═══════════════════════════════════════════════════════════════════
#  MENU QUẢN LÝ THIẾT BỊ
# ═══════════════════════════════════════════════════════════════════

def menu_equipment(eq_svc: EquipmentService):
    """Display and handle the Equipment Management menu."""
    while True:
        print_header("EQUIPMENT MANAGEMENT")
        print("  1. Add new equipment")
        print("  2. View all equipment")
        print("  3. Find equipment by ID")
        print("  4. Find equipment by status")
        print("  5. Update equipment")
        print("  6. Group equipment by status")
        print("  0. Return to Main Menu")
        print_separator()

        choice = input("  Choose an option: ").strip()

        try:
            if choice == "1":
                action_add_equipment(eq_svc)
            elif choice == "2":
                action_show_all_equipment(eq_svc)
            elif choice == "3":
                action_search_by_id(eq_svc)
            elif choice == "4":
                action_search_by_status(eq_svc)
            elif choice == "5":
                action_update_equipment(eq_svc)
            elif choice == "6":
                action_group_by_status(eq_svc)
            elif choice == "0":
                break
            else:
                print("  [Error] Invalid choice. Please select 0-6.")
        except Exception as e:
            print(f"  [Error] {e}")

        pause()


def action_add_equipment(eq_svc: EquipmentService):
    """Add new equipment with validation and error handling."""
    print_header("ADD NEW EQUIPMENT")
    try:
        eq_id = input("  Enter equipment ID: ").strip()
        if not eq_id:
            raise ValueError("Equipment ID cannot be empty.")
        
        # Check if ID already exists
        if eq_svc.find_by_id(eq_id):
            raise ValueError(f"Equipment with ID '{eq_id}' already exists.")
        
        name = input("  Enter equipment name: ").strip()
        if not name:
            raise ValueError("Equipment name cannot be empty.")

        power_str = input("  Enter power rating (W): ").strip()
        if not power_str:
            raise ValueError("Power rating cannot be empty.")
        try:
            power = float(power_str)
            if power < 0:
                raise ValueError("Power rating must be non-negative.")
        except ValueError as e:
            raise ValueError(f"Power rating must be a valid number: {e}")

        rate_str = input("  Enter hourly rate (VND): ").strip()
        if not rate_str:
            raise ValueError("Hourly rate cannot be empty.")
        try:
            rate = float(rate_str)
            if rate < 0:
                raise ValueError("Hourly rate must be non-negative.")
        except ValueError as e:
            raise ValueError(f"Hourly rate must be a valid number: {e}")

        eq = eq_svc.add_equipment(eq_id, name, power, rate)
        logger.info(f"Equipment added successfully: {eq_id} - {name}")
        print(f"\n  [OK] Equipment added: {eq}")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"  [Error] {e}")
    except Exception as e:
        logger.error(f"Unexpected error adding equipment: {e}")
        print(f"  [Error] Unexpected error: {e}")


def action_show_all_equipment(eq_svc: EquipmentService):
    print_header("ALL EQUIPMENT")
    items = eq_svc.get_all()
    if not items:
        print("  (No equipment available)")
        return
    for i, eq in enumerate(items, 1):
        print(f"  {i:2}. {eq}")
    summary = eq_svc.get_summary()
    print_separator()
    print(f"  Total: {summary['total']} | Available: {summary['available']} | Rented: {summary['rented']}")


def action_search_by_id(eq_svc: EquipmentService):
    print_header("FIND EQUIPMENT BY ID")
    eq_id = input("  Enter equipment ID to find: ").strip()
    eq = eq_svc.find_by_id(eq_id)
    if eq:
        print(f"\n  Result: {eq}")
    else:
        print(f"  Equipment with ID '{eq_id}' not found.")


def action_search_by_status(eq_svc: EquipmentService):
    print_header("FIND EQUIPMENT BY STATUS")
    print("  1. Available   2. Rented")
    choice = input("  Choose (1/2): ").strip()
    if choice == "1":
        status = "Available"
    elif choice == "2":
        status = "Rented"
    else:
        raise ValueError(
            f"Choice '{choice}' is invalid. Please enter 1 (Available) or 2 (Rented)."
        )
    items = eq_svc.find_by_status(status)
    if not items:
        print(f"  No equipment found with status '{status}'.")
        return
    print(f"\n  Equipment [{status}] ({len(items)} results):")
    for i, eq in enumerate(items, 1):
        print(f"  {i:2}. {eq}")


def action_update_equipment(eq_svc: EquipmentService):
    """Update equipment with comprehensive validation."""
    print_header("UPDATE EQUIPMENT")
    try:
        eq_id = input("  Enter equipment ID to update: ").strip()
        if not eq_id:
            raise ValueError("Equipment ID cannot be empty.")
        
        eq = eq_svc.find_by_id(eq_id)
        if not eq:
            print(f"  Equipment with ID '{eq_id}' not found.")
            logger.warning(f"Update attempted for non-existent equipment: {eq_id}")
            return
        
        print(f"  Current equipment: {eq}")
        print("  (Press Enter to keep the current value)")
        
        name = input(f"  New name [{eq.name}]: ").strip() or None
        power_str = input(f"  New power rating [{eq.power_rating}W]: ").strip()
        rate_str = input(f"  New hourly rate [{eq.hourly_rate:,.0f}]: ").strip()

        power = None
        if power_str:
            try:
                power = float(power_str)
                if power < 0:
                    raise ValueError("Power rating must be non-negative.")
            except ValueError as e:
                raise ValueError(f"Invalid power rating: {e}")

        rate = None
        if rate_str:
            try:
                rate = float(rate_str)
                if rate < 0:
                    raise ValueError("Hourly rate must be non-negative.")
            except ValueError as e:
                raise ValueError(f"Invalid hourly rate: {e}")

        updated = eq_svc.update_equipment(eq_id, name, power, rate)
        logger.info(f"Equipment updated: {eq_id}")
        print(f"\n  [OK] Updated equipment: {updated}")
    except ValueError as e:
        logger.error(f"Validation error during update: {e}")
        print(f"  [Error] {e}")
    except Exception as e:
        logger.error(f"Unexpected error updating equipment: {e}")
        print(f"  [Error] Unexpected error: {e}")


def action_group_by_status(eq_svc: EquipmentService):
    print_header("GROUP EQUIPMENT BY STATUS")
    groups = eq_svc.group_by_status()
    for status, items in groups.items():
        print(f"\n  [{status}] ({len(items)} items):")
        if items:
            for eq in items:
                print(f"    - {eq}")
        else:
            print("    (None)")


# ═══════════════════════════════════════════════════════════════════
#  MENU QUẢN LÝ ĐƠN THUÊ
# ═══════════════════════════════════════════════════════════════════

def menu_rental(rental_svc: RentalService, eq_svc: EquipmentService):
    """Display and handle the Rental Management menu."""
    while True:
        print_header("RENTAL MANAGEMENT")
        print("  1. Create new rental")
        print("  2. View all rentals")
        print("  3. View unavailable equipment")
        print("  4. Preview rental fee")
        print("  5. Return equipment")
        print("  6. Group equipment by rental status")
        print("  0. Return to Main Menu")
        print_separator()

        choice = input("  Choose an option: ").strip()

        try:
            if choice == "1":
                action_create_rental(rental_svc, eq_svc)
            elif choice == "2":
                action_show_all_rentals(rental_svc)
            elif choice == "3":
                action_show_unavailable(rental_svc)
            elif choice == "4":
                action_preview_fee(rental_svc)
            elif choice == "5":
                action_return_rental(rental_svc)
            elif choice == "6":
                action_group_rental_status(rental_svc, eq_svc)
            elif choice == "0":
                break
            else:
                print("  [Error] Invalid choice. Please select 0-6.")
        except Exception as e:
            print(f"  [Error] {e}")

        pause()


def action_create_rental(rental_svc: RentalService, eq_svc: EquipmentService):
    print_header("CREATE NEW RENTAL")
    print("  Date format: YYYY-MM-DD HH:MM  (e.g. 2025-06-01 08:00)")

    rental_id = input("  Enter rental ID: ").strip()
    client_name = input("  Enter client name: ").strip()

    available = eq_svc.find_by_status("Available")
    if not available:
        print("  [Info] No equipment is currently available.")
        return
    print("\n  Available equipment:")
    for eq in available:
        print(f"    - {eq}")

    ids_input = input("\n  Enter equipment IDs (comma-separated): ").strip()
    equipment_ids = [x.strip() for x in ids_input.split(",") if x.strip()]

    start_str = input("  Rental start time: ").strip()
    return_str = input("  Expected return time: ").strip()

    rental = rental_svc.create_rental(
        rental_id, client_name, equipment_ids, start_str, return_str
    )
    print(f"\n  [OK] Rental created successfully!")
    print(f"  {rental}")


def action_show_all_rentals(rental_svc: RentalService):
    print_header("ALL RENTALS")
    items = rental_svc.get_all()
    if not items:
        print("  (No rentals found)")
        return
    for i, r in enumerate(items, 1):
        print(f"  {i:2}. {r}")
    s = rental_svc.get_summary()
    print_separator()
    print(f"  Total: {s['total']} | Active: {s['active']} | Returned: {s['returned']}")


def action_show_unavailable(rental_svc: RentalService):
    print_header("UNAVAILABLE EQUIPMENT")
    items = rental_svc.get_unavailable_equipment()
    if not items:
        print("  All equipment is currently available.")
        return
    for i, eq in enumerate(items, 1):
        print(f"  {i:2}. {eq}")


def action_preview_fee(rental_svc: RentalService):
    print_header("PREVIEW RENTAL FEE")
    rental_id = input("  Enter rental ID: ").strip()
    info = rental_svc.preview_rental_fee(rental_id)
    print(f"\n  Rental ID : {info['rental_id']}")
    print(f"  Client    : {info['client_name']}")
    print(f"  Rental fee: {info['rental_fee']:>15,.0f} VND")
    print(f"  Late fee  : {info['late_penalty']:>15,.0f} VND")
    print_separator()
    print(f"  TOTAL     : {info['total']:>15,.0f} VND")


def action_return_rental(rental_svc: RentalService):
    print_header("RETURN EQUIPMENT")
    print("  (Leave return time blank to use current time)")
    rental_id = input("  Enter rental ID to return: ").strip()
    actual_str = input("  Actual return time (Enter=now): ").strip()
    actual_str = actual_str if actual_str else None

    rental, fee, penalty = rental_svc.return_rental(rental_id, actual_str)
    print(f"\n  [OK] Equipment returned successfully!")
    print(f"  Rental ID : {rental.rental_id}")
    print(f"  Client    : {rental.client_name}")
    print(f"  Fee       : {fee:>15,.0f} VND")
    print(f"  Late fee  : {penalty:>15,.0f} VND")
    print_separator()
    print(f"  TOTAL     : {(fee + penalty):>15,.0f} VND")
    if penalty > 0:
        print("  [!] The rental is returned late!")


def action_group_rental_status(rental_svc: RentalService, eq_svc: EquipmentService):
    print_header("GROUP EQUIPMENT BY RENTAL STATUS")
    groups = rental_svc.group_equipment_by_rental_status()
    eq_dict = {eq.equipment_id: eq.name for eq in eq_svc.get_all()}
    for status, ids in groups.items():
        print(f"\n  [{status}] ({len(ids)} items):")
        if ids:
            for eid in ids:
                name = eq_dict.get(eid, "?")
                print(f"    - [{eid}] {name}")
        else:
            print("    (None)")


# ═══════════════════════════════════════════════════════════════════
#  MENU PHÂN TÍCH DỮ LIỆU
# ═══════════════════════════════════════════════════════════════════

def menu_analysis(analysis_svc: AnalysisService,
                  eq_svc: EquipmentService,
                  rental_svc: RentalService):
    """Display and handle the Data Analysis menu."""
    while True:
        print_header("DATA ANALYSIS")
        print("  1. Sort equipment by hourly rate")
        print("  2. Sort equipment by power rating")
        print("  3. Sort rentals by duration")
        print("  4. Sort rentals by client name")
        print("  5. Revenue summary")
        print("  6. Top rented equipment")
        print("  0. Return to Main Menu")
        print_separator()

        choice = input("  Choose an option: ").strip()

        try:
            eq_list = eq_svc.get_all()
            r_list = rental_svc.get_all()

            if choice == "1":
                order = input("  1=Ascending  2=Descending: ").strip()
                asc = (order != "2")
                sorted_eq = analysis_svc.sort_equipment_by_rate(eq_list, asc)
                label = "Ascending" if asc else "Descending"
                print_header(f"EQUIPMENT BY HOURLY RATE ({label})")
                for i, eq in enumerate(sorted_eq, 1):
                    print(f"  {i:2}. [{eq.equipment_id}] {eq.name} - {eq.hourly_rate:,.0f} VND/hour")

            elif choice == "2":
                order = input("  1=Ascending  2=Descending: ").strip()
                asc = (order != "2")
                sorted_eq = analysis_svc.sort_equipment_by_power(eq_list, asc)
                label = "Ascending" if asc else "Descending"
                print_header(f"EQUIPMENT BY POWER ({label})")
                for i, eq in enumerate(sorted_eq, 1):
                    print(f"  {i:2}. [{eq.equipment_id}] {eq.name} - {eq.power_rating}W")

            elif choice == "3":
                order = input("  1=Ascending  2=Descending: ").strip()
                asc = (order != "2")
                sorted_r = analysis_svc.sort_rentals_by_duration(r_list, asc)
                label = "Ascending" if asc else "Descending"
                print_header(f"RENTALS BY DURATION ({label})")
                for i, r in enumerate(sorted_r, 1):
                    h = r.get_rental_duration_hours()
                    print(f"  {i:2}. [{r.rental_id}] {r.client_name} - {format_duration(h)}")

            elif choice == "4":
                order = input("  1=A-Z  2=Z-A: ").strip()
                asc = (order != "2")
                sorted_r = analysis_svc.sort_rentals_by_client(r_list, asc)
                label = "A→Z" if asc else "Z→A"
                print_header(f"RENTALS BY CLIENT NAME ({label})")
                for i, r in enumerate(sorted_r, 1):
                    print(f"  {i:2}. [{r.rental_id}] {r.client_name} ({r.status})")

            elif choice == "5":
                summary = analysis_svc.get_revenue_summary(r_list, eq_list)
                print_header("REVENUE SUMMARY")
                print(f"  Total rental fee: {summary['total_fee']:>15,.0f} VND")
                print(f"  Total late penalty: {summary['total_penalty']:>15,.0f} VND")
                print_separator()
                print(f"  GRAND TOTAL     : {summary['grand_total']:>15,.0f} VND")

            elif choice == "6":
                top = analysis_svc.get_top_rented_equipment(r_list, eq_list)
                print_header("TOP RENTED EQUIPMENT")
                if not top:
                    print("  (No data available)")
                else:
                    for i, (eq, count) in enumerate(top, 1):
                        print(f"  {i}. [{eq.equipment_id}] {eq.name} - {count} rentals")

            elif choice == "0":
                break
            else:
                print("  [Error] Invalid choice. Please select 0-6.")
        except Exception as e:
            print(f"  [Error] {e}")

        pause()


# ═══════════════════════════════════════════════════════════════════
#  MENU XEM LOGS
# ═══════════════════════════════════════════════════════════════════

def menu_logs():
    """Display log file contents."""
    while True:
        print_header("VIEW LOG FILES")
        print("  1. View Rental History")
        print("  2. View Maintenance Log")
        print("  0. Return to Main Menu")
        print_separator()

        choice = input("  Choose: ").strip()

        if choice == "1":
            print_header("RENTAL HISTORY")
            print(read_log_file(RENTAL_HISTORY_TXT))
        elif choice == "2":
            print_header("MAINTENANCE LOG")
            print(read_log_file(MAINTENANCE_LOG_TXT))
        elif choice == "0":
            break
        else:
            print("  [Error] Invalid choice.")

        pause()


# ═══════════════════════════════════════════════════════════════════
#  MAIN MENU & KHỞI ĐỘNG
# ═══════════════════════════════════════════════════════════════════

def main():
    """Hàm chính: khởi động chương trình, load dữ liệu, hiển thị menu."""

    # --- Khởi động: tạo file lưu trữ nếu chưa có ---
    print("\n" + "=" * 60)
    print("  EVENT EQUIPMENT RENTAL & LOGISTICS")
    print("  PFP191 - Topic 06")
    print("=" * 60)
    print("\n  Starting application...")
    logger.info("Application started")

    try:
        ensure_storage_files()
        logger.info("Storage files initialized")
    except Exception as e:
        logger.warning(f"Could not create storage files: {e}")
        print(f"  [Warning] Could not create storage files: {e}")

    # --- Khởi tạo services ---
    try:
        eq_svc = EquipmentService()
        rental_svc = RentalService(eq_svc)
        analysis_svc = AnalysisService()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        print(f"  [Error] Failed to initialize services: {e}")
        return

    # --- Load dữ liệu từ CSV ---
    print("\n  Loading data...")
    try:
        eq_records = load_equipment()
        eq_svc.load_from_records(eq_records)
        logger.info(f"Loaded {len(eq_records)} equipment records")
    except Exception as e:
        logger.error(f"Could not load equipment: {e}")
        print(f"  [Error] Could not load equipment: {e}")

    try:
        rental_records = load_rentals()
        rental_svc.load_from_records(rental_records)
        logger.info(f"Loaded {len(rental_records)} rental records")
    except Exception as e:
        logger.error(f"Could not load rentals: {e}")
        print(f"  [Error] Could not load rentals: {e}")

    print("  [OK] Load du lieu hoan tat!")

    # --- Vòng lặp Main Menu ---
    while True:
        try:
            print_header("MAIN MENU - EVENT EQUIPMENT RENTAL")
            eq_sum = eq_svc.get_summary()
            r_sum = rental_svc.get_summary()
            print(f"  Equipment: {eq_sum['total']} total | {eq_sum['available']} available")
            print(f"  Rentals: {r_sum['total']} total | {r_sum['active']} active")
            print_separator()
            print("  1. Equipment Management")
            print("  2. Rental Management")
            print("  3. Data Analysis")
            print("  4. View Log Files")
            print("  5. Save and Exit")
            print_separator()

            choice = input("  Choose an option: ").strip()

            if choice == "1":
                menu_equipment(eq_svc)
            elif choice == "2":
                menu_rental(rental_svc, eq_svc)
            elif choice == "3":
                menu_analysis(analysis_svc, eq_svc, rental_svc)
            elif choice == "4":
                menu_logs()
            elif choice == "5":
                # Lưu dữ liệu và thoát
                print("\n  Saving data...")
                try:
                    save_equipment(eq_svc.get_all())
                    save_rentals(rental_svc.get_all())
                    logger.info("Data saved successfully")
                    print("  [OK] Saved equipment.csv")
                    print("  [OK] Saved rentals.csv")
                except Exception as e:
                    logger.error(f"Could not save data: {e}")
                    print(f"  [Error] Could not save data: {e}")
                print("\n  Thank you for using the program!")
                print("  Event Equipment Rental & Logistics - PFP191")
                print("=" * 60 + "\n")
                logger.info("Application closed normally")
                break
            else:
                print("  [Error] Invalid choice. Please select 1-5.")
        except KeyboardInterrupt:
            print("\n  [Notice] Ctrl+C detected.")
            print("  Saving data before exit...")
            try:
                save_equipment(eq_svc.get_all())
                save_rentals(rental_svc.get_all())
                print("  ✓ Data saved. Exiting program.")
                logger.info("Application closed by user (Ctrl+C)")
            except Exception as e:
                logger.error(f"Error saving data on exit: {e}")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            print(f"  [Unexpected Error] {e}")
            pause()


if __name__ == "__main__":
    main()


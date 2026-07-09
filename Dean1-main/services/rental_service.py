"""
services/rental_service.py
---------------------------
Service xử lý các nghiệp vụ quản lý đơn thuê thiết bị sự kiện.

Yêu cầu đáp ứng:
- Create new rental order (kiểm tra thiết bị Available, ID trùng)
- Check unavailable equipment
- Calculate rental fees
- Calculate late penalties
- Return equipment (cập nhật trạng thái thiết bị về Available)
- Group equipment by rental status
"""

from datetime import datetime
from models.rental import Rental
from storage.file_handler import append_rental_history
from utils.validators import (
    validate_non_empty,
    validate_unique_id,
    validate_client_name,
)
from utils.time_utils import parse_datetime


class RentalService:
    """
    Quản lý danh sách đơn thuê và các nghiệp vụ liên quan.

    Attributes:
        _rental_list     : list           - Danh sách Rental objects
        _equipment_service: EquipmentService - Dùng để kiểm tra và cập nhật thiết bị
    """

    def __init__(self, equipment_service):
        """
        Args:
            equipment_service: Đối tượng EquipmentService đã khởi tạo
        """
        # Danh sách đơn thuê: list of Rental objects
        self._rental_list: list = []
        self._equipment_service = equipment_service

    # ──────────────────────────────────────────────
    # LOAD từ dữ liệu đã đọc
    # ──────────────────────────────────────────────
    def load_from_records(self, records: list):
        """
        Nạp dữ liệu từ danh sách dict (đã đọc từ CSV) vào _rental_list.

        Args:
            records: Danh sách dict từ file_handler.load_rentals()
        """
        self._rental_list = []
        for record in records:
            try:
                rental = Rental.from_dict(record)
                self._rental_list.append(rental)
            except Exception as e:
                print(f"  [Warning] Bo qua dong loi trong rentals.csv: {e}")
        print(f"  Da load {len(self._rental_list)} don thue.")

    def get_all(self) -> list:
        """Trả về danh sách tất cả đơn thuê."""
        return self._rental_list

    def get_active_rentals(self) -> list:
        """Trả về danh sách đơn thuê đang Active."""
        return [r for r in self._rental_list if r.status == "Active"]

    def get_returned_rentals(self) -> list:
        """Trả về danh sách đơn thuê đã Returned."""
        return [r for r in self._rental_list if r.status == "Returned"]

    # ──────────────────────────────────────────────
    # TẠO ĐƠN THUÊ MỚI
    # ──────────────────────────────────────────────
    def create_rental(self, rental_id: str, client_name: str,
                       equipment_ids: list, start_time_str: str,
                       expected_return_str: str) -> Rental:
        """
        Tạo đơn thuê mới.

        Quy trình:
        1. Validate rental_id không trùng
        2. Validate client_name không rỗng
        3. Kiểm tra từng thiết bị tồn tại và đang Available
        4. Parse và validate thời gian
        5. Tạo Rental object
        6. Đổi trạng thái các thiết bị sang Rented

        Args:
            rental_id          : Mã đơn thuê (duy nhất)
            client_name        : Tên khách hàng
            equipment_ids      : Danh sách mã thiết bị muốn thuê
            start_time_str     : Thời gian bắt đầu (chuỗi)
            expected_return_str: Thời gian dự kiến trả (chuỗi)

        Returns:
            Đối tượng Rental vừa tạo

        Raises:
            ValueError: Nếu bất kỳ validation nào thất bại
        """
        # --- 1. Validate rental_id ---
        rental_id = validate_non_empty(rental_id, "Rental ID")
        existing_ids = [r.rental_id for r in self._rental_list]
        rental_id = validate_unique_id(rental_id, existing_ids, "Rental ID")

        # --- 2. Validate client_name ---
        client_name = validate_client_name(client_name)

        # --- 3. Validate equipment_ids ---
        if not equipment_ids:
            raise ValueError("Phải chọn ít nhất một thiết bị để thuê.")

        unavailable = []
        not_found = []
        for eq_id in equipment_ids:
            eq = self._equipment_service.find_by_id(eq_id)
            if eq is None:
                not_found.append(eq_id)
            elif eq.status != "Available":
                unavailable.append(eq_id)

        if not_found:
            raise ValueError(
                f"Không tìm thấy thiết bị với ID: {', '.join(not_found)}"
            )
        if unavailable:
            raise ValueError(
                f"Thiết bị đang được thuê (không Available): {', '.join(unavailable)}"
            )

        # --- 4. Validate thời gian ---
        start_time = parse_datetime(start_time_str)
        expected_return = parse_datetime(expected_return_str)

        if expected_return <= start_time:
            raise ValueError(
                "Thời gian dự kiến trả phải sau thời gian bắt đầu thuê."
            )

        # --- 5. Tạo Rental object ---
        new_rental = Rental(
            rental_id=rental_id,
            client_name=client_name,
            equipment_ids=equipment_ids,
            start_time=start_time,
            expected_return=expected_return,
            status="Active",
        )
        self._rental_list.append(new_rental)

        # --- 6. Cập nhật trạng thái thiết bị sang Rented ---
        for eq_id in equipment_ids:
            self._equipment_service.update_status(eq_id, "Rented")

        return new_rental

    # ──────────────────────────────────────────────
    # TRẢ THIẾT BỊ
    # ──────────────────────────────────────────────
    def return_rental(self, rental_id: str, actual_return_str: str = None):
        """
        Xử lý trả thiết bị: cập nhật trạng thái đơn thuê và thiết bị.

        Args:
            rental_id          : Mã đơn thuê cần trả
            actual_return_str  : Thời gian thực tế trả (chuỗi).
                                 Nếu None, dùng thời gian hiện tại.

        Returns:
            Tuple (rental, rental_fee, late_penalty)

        Raises:
            ValueError: Nếu không tìm thấy đơn hoặc đơn đã được trả
        """
        rental = self.find_by_id(rental_id)
        if rental is None:
            raise ValueError(f"Không tìm thấy đơn thuê với ID '{rental_id}'.")

        if rental.status == "Returned":
            raise ValueError(
                f"Đơn thuê '{rental_id}' đã được trả rồi."
            )

        # Xac dinh thoi gian tra thuc te
        if actual_return_str:
            actual_return = parse_datetime(actual_return_str)
        else:
            actual_return = datetime.now().replace(second=0, microsecond=0)

        # Validate: actual_return phai sau start_time
        if actual_return <= rental.start_time:
            raise ValueError(
                f"Thoi gian tra thuc te ({actual_return.strftime('%Y-%m-%d %H:%M')}) "
                f"phai sau thoi gian bat dau thue "
                f"({rental.start_time.strftime('%Y-%m-%d %H:%M')})."
            )

        # Cap nhat don thue
        rental.actual_return = actual_return
        rental.status = "Returned"

        # Tính phí và phạt
        all_equipment = self._equipment_service.get_all()
        rental_fee = rental.calculate_rental_fee(all_equipment)
        late_penalty = rental.calculate_late_penalty(all_equipment)

        # Cập nhật trạng thái thiết bị về Available
        for eq_id in rental.equipment_ids:
            try:
                self._equipment_service.update_status(eq_id, "Available")
            except Exception:
                pass  # Bỏ qua nếu thiết bị không tồn tại

        # Ghi vào rental_history.txt
        append_rental_history(rental, all_equipment, rental_fee, late_penalty)

        return rental, rental_fee, late_penalty

    # ──────────────────────────────────────────────
    # TÌM KIẾM ĐƠN THUÊ
    # ──────────────────────────────────────────────
    def find_by_id(self, rental_id: str):
        """
        Tìm đơn thuê theo ID.

        Returns:
            Rental object nếu tìm thấy, None nếu không.
        """
        rental_id = str(rental_id).strip().upper()
        for rental in self._rental_list:
            if rental.rental_id.upper() == rental_id:
                return rental
        return None

    # ──────────────────────────────────────────────
    # KIỂM TRA THIẾT BỊ KHÔNG KHẢ DỤNG
    # ──────────────────────────────────────────────
    def get_unavailable_equipment(self) -> list:
        """
        Lấy danh sách thiết bị đang được thuê (status = Rented).

        Returns:
            Danh sách Equipment objects đang Rented
        """
        return self._equipment_service.find_by_status("Rented")

    # ──────────────────────────────────────────────
    # TÍNH PHÍ VÀ PHẠT (xem trước, chưa confirm)
    # ──────────────────────────────────────────────
    def preview_rental_fee(self, rental_id: str) -> dict:
        """
        Xem trước phí thuê cho một đơn (đơn vẫn Active).

        Args:
            rental_id: Mã đơn thuê

        Returns:
            Dict chứa rental_fee và late_penalty (tạm tính)

        Raises:
            ValueError: Nếu không tìm thấy đơn
        """
        rental = self.find_by_id(rental_id)
        if rental is None:
            raise ValueError(f"Không tìm thấy đơn thuê với ID '{rental_id}'.")

        all_equipment = self._equipment_service.get_all()
        rental_fee = rental.calculate_rental_fee(all_equipment)
        late_penalty = rental.calculate_late_penalty(all_equipment)

        return {
            "rental_id": rental.rental_id,
            "client_name": rental.client_name,
            "rental_fee": rental_fee,
            "late_penalty": late_penalty,
            "total": rental_fee + late_penalty,
        }

    # ──────────────────────────────────────────────
    # NHÓM THIẾT BỊ THEO TRẠNG THÁI TRONG ĐƠN THUÊ
    # ──────────────────────────────────────────────
    def group_equipment_by_rental_status(self) -> dict:
        """
        Nhóm thiết bị dựa trên trạng thái đơn thuê (Active/Returned).

        Dùng dict: key = rental_status, value = list of equipment_ids

        Returns:
            Dict {"Active": [eq_id, ...], "Returned": [eq_id, ...]}
        """
        result = {"Active": [], "Returned": []}
        for rental in self._rental_list:
            for eq_id in rental.equipment_ids:
                if eq_id not in result[rental.status]:
                    result[rental.status].append(eq_id)
        return result

    def get_summary(self) -> dict:
        """Trả về thống kê tóm tắt đơn thuê."""
        active = len(self.get_active_rentals())
        returned = len(self.get_returned_rentals())
        return {
            "total": len(self._rental_list),
            "active": active,
            "returned": returned,
        }

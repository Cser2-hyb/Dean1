from datetime import datetime # thư viện xử lí thời gian
import math


def parse_datetime(value: str) -> datetime:
    value = str(value).strip()
    if not value or value.lower() == "none":
        raise ValueError("Invalid datetime value")

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Unable to parse datetime from '{value}'. "
        "Expected format 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD'."
    )


def calculate_hours(start: datetime, end: datetime) -> float:
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("start and end must be datetime objects")

    delta = end - start
    total_seconds = delta.total_seconds()
    if total_seconds <= 0:
        return 0.0

    return float(math.ceil(total_seconds / 3600.0))







class Rental:
    """
    Đại diện cho một đơn thuê thiết bị.

    Attributes (private — double underscore):
        __rental_id       : str       - Mã đơn thuê (duy nhất)
        __client_name     : str       - Tên khách hàng
        __equipment_ids   : list      - Danh sách mã thiết bị trong đơn
        __start_time      : datetime  - Thời gian bắt đầu thuê
        __expected_return : datetime  - Thời gian dự kiến trả
        __actual_return   : datetime  - Thời gian thực tế trả (None nếu chưa trả)
        __status          : str       - Trạng thái đơn: "Active" hoặc "Returned"

    Lưu ý: Bên ngoài class PHẢI truy cập qua property.
    Python áp dụng name mangling: __attr → _Rental__attr.
    """
    VALID_STATUSES = ["Active", "Returned"]

    #Tỷ lệ phạt trễ: 50% mỗi giờ trễ
    LATE_PENALTY_RATE = 0.5

    def __init__(self, rental_id:str, client_name:str, equipment_ids: list[str] , start_time, expected_return, actual_return = None, status : str = "Active"):
        """
        Khởi tạo đối tượng Rental.

        Args:
            rental_id       : Mã đơn thuê (duy nhất, không rỗng)
            client_name     : Tên khách hàng (không rỗng)
            equipment_ids   : Danh sách mã thiết bị (list of str)
            start_time      : Thời gian bắt đầu (datetime hoặc str)
            expected_return : Thời gian dự kiến trả (phải sau start_time)
            actual_return   : Thời gian thực tế trả (None nếu chưa trả)
            status          : Trạng thái đơn (mặc định: "Active")
        """

        self.rental_id = rental_id
        self.client_name = client_name
        self.equipment_ids = equipment_ids
        self.start_time = start_time
        self.expected_return = expected_return
        self.actual_return = actual_return
        self.status = status

        #_____________________________________
        #Property: rental_id
        #_____________________________________
    @property
    def rental_id(self) -> str:
        return self.__rental_id
    
    @rental_id.setter
    def rental_id(self, value: str):
        value = str(value).strip()
        if not value:
            raise ValueError("Invalid rental ID")
        self.__rental_id = value

        #Property: client_name

    @property
    def client_name(self) -> str:
        return self.__client_name
        
    @client_name.setter
    def client_name(self, value: str):
        value = str(value).strip()
        if not value:
            raise ValueError("Invalid Client name")
        self.__client_name = value

        #Property: equipment_ids

    @property
    def equipment_ids(self) -> list:
        return self.__equipment_ids
        
    @equipment_ids.setter
    def equipment_ids(self, value: list):
        if not isinstance(value, list):

            if isinstance(value, str):
                value = [v.strip() for v in value.split(";") if v.strip()]
            else:
                raise ValueError("equipment_ids must be a list")
        if len(value) == 0:
            raise ValueError("At least one equipment item is required")
        self.__equipment_ids = value

        #property start_time

    @property
    def start_time(self) -> datetime:
        return self.__start_time
    
    @start_time.setter
    def start_time(self, value):
        if isinstance(value, datetime):
            self.__start_time = value
        else:
            self.__start_time = parse_datetime(str(value))

        #property expected_return

    @property
    def expected_return(self) -> datetime:
        return self.__expected_return
    
    @expected_return.setter
    def expected_return(self, value):
        if isinstance(value, datetime):
            dt = value
        else:
            dt = parse_datetime(str(value))

        # kiem tra thoi gian phai tra sau khi start time
        if hasattr(self, "_Rental__start_time") and dt <= self.__start_time:
            raise ValueError("Expected return time must be after rental start time")
        self.__expected_return = dt
        #______________________________________________
        #property actual_return
        #Validation: actual_return phải sau start_time
        #______________________________________________

    @property
    def actual_return(self):
        return self.__actual_return
    
    @actual_return.setter
    def actual_return(self, value):
        if value is None or value == "" or value == "None":
            self.__actual_return = None
        elif isinstance(value, datetime):
            # kiem tra actual return phai tra sau start_time
            if hasattr(self, "_Rental__start_time") and value <= self.__start_time:
                raise ValueError(
                    "Actual return time must be after rental start time "
                    f"(Start: {self.__start_time.strftime('%Y-%m-%d %H:%M')})"
                    )
            self.__actual_return = value
        else:
            dt = parse_datetime(str(value))
            # Kiểm tra actual_return phải sau start_time
            if hasattr(self, "_Rental__start_time") and dt <= self.__start_time:
                raise ValueError(
                    "Actual return time must be after rental start time "
                    f"(Start: {self.__start_time.strftime('%Y-%m-%d %H:%M')})"
                    )
            self.__actual_return = dt

            #__________________________________________
            #property: status
            #__________________________________________

    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, value: str):
        value = str(value).strip()
        if value not in self.VALID_STATUSES:
            raise ValueError( 
                f"Invalid order status.: '{value}'. "
                f"Only accepts: {self.VALID_STATUSES}"
                )
        self.__status = value

        #________________________________________________
        #Phương thức tính phí
        #________________________________________________

    def calculate_rental_fee(self, equipment_list: list) -> float:
        """
        Tính tổng phí thuê dựa trên thời gian thuê và giá thuê của từng thiết bị.

        Công thức:
            rental_fee = sum(hourly_rate * hours_rented) cho mỗi thiết bị

        Args:
            equipment_list: Danh sách tất cả Equipment objects

        Returns:
            Tổng phí thuê (float), làm tròn 2 chữ số thập phân
        """
        # xác định thời gian kết thúc: dùng actual_return nếu đã hoàn trả, còn chưa trả thì dùng expected_return
        end_time = self.actual_return if self.actual_return else self.expected_return

        # tính số h thuê làm tròn lên
        hours = calculate_hours(self.start_time, end_time)

        # tạo dict để tra cứu thiết bị nhanh theo ID
        equipment_dict = {eq.equipment_id: eq for eq in equipment_list}

        total_fee = 0.0
        for eq_id in self.equipment_ids:
            if eq_id in equipment_dict:
                # cộng phí từng thiết bị
                total_fee += equipment_dict[eq_id].hourly_rate * hours

        return round(total_fee, 2)
    
    def get_rental_duration(self) -> float:
        """
        Tính tổng thời gian thuê tính theo giờ.
        Dùng actual_return nếu đã trả, ngược lại dùng expected_return.
        """
        end_time = self.actual_return if self.actual_return else self.expected_return
        return calculate_hours(self.start_time, end_time)
    # ──────────────────────────────────────────────
    # Phương thức chuyển đổi dữ liệu
    # ──────────────────────────────────────────────
    def to_dict(self) -> dict:
        """Chuyển đối tượng sang dict để lưu CSV.
        Truy cập qua property để đảm bảo đúng encapsulation."""
        # Dùng format chuẩn ISO cho datetime, dùng "None" nếu chưa có
        actual_str = (
            self.actual_return.strftime("%Y-%m-%d %H:%M")
            if self.actual_return else "None"
        )
        return {
            "rental_id": self.rental_id,
            "client_name": self.client_name,
            "equipment_ids": ";".join(self.equipment_ids),  # Nối bằng dấu ;
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M"),
            "expected_return": self.expected_return.strftime("%Y-%m-%d %H:%M"),
            "actual_return": actual_str,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Rental":
        """Tạo đối tượng Rental từ dict (dùng khi load CSV)."""
        return cls(
            rental_id=data["rental_id"],
            client_name=data["client_name"],
            equipment_ids=data["equipment_ids"],  # setter tự tách chuỗi
            start_time=data["start_time"],
            expected_return=data["expected_return"],
            actual_return=data.get("actual_return", None),
            status=data.get("status", "Active"),
        )

    def __str__(self) -> str:
        """Hiển thị thông tin đơn thuê."""
        eq_str = ", ".join(self.equipment_ids)
        actual_str = (
            self.actual_return.strftime("%Y-%m-%d %H:%M")
            if self.actual_return else "Chua tra"
        )
        return (
            f"[{self.rental_id}] KH: {self.client_name} | "
            f"Thiet bi: {eq_str} | "
            f"Bat dau: {self.start_time.strftime('%Y-%m-%d %H:%M')} | "
            f"Du kien tra: {self.expected_return.strftime('%Y-%m-%d %H:%M')} | "
            f"Thuc te tra: {actual_str} | "
            f"Trang thai: {self.status}"
        )

    def __repr__(self) -> str:
        return (
            f"Rental(id='{self.rental_id}', client='{self.client_name}', "
            f"status='{self.status}')"
        )

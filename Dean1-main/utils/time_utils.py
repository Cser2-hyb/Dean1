"""
utils/time_utils.py
-------------------
Các hàm tiện ích xử lý ngày giờ cho dự án Event Equipment Rental.

Yêu cầu đáp ứng:
- Parse chuỗi datetime theo định dạng chuẩn
- Tính số giờ giữa hai mốc thời gian (làm tròn lên)
- Validate thời gian hợp lệ
"""

from datetime import datetime
import math

# Định dạng datetime chuẩn dùng trong toàn dự án
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

# Danh sách các định dạng hỗ trợ khi parse input từ người dùng
SUPPORTED_FORMATS = [
    "%Y-%m-%d %H:%M",
    "%d/%m/%Y %H:%M",
    "%Y/%m/%d %H:%M",
    "%d-%m-%Y %H:%M",
]


def parse_datetime(value: str) -> datetime:
    """
    Parse chuỗi thời gian sang đối tượng datetime.

    Hỗ trợ nhiều định dạng phổ biến.

    Args:
        value: Chuỗi ngày giờ, ví dụ "2025-06-01 08:00"

    Returns:
        Đối tượng datetime

    Raises:
        ValueError: Nếu chuỗi không đúng định dạng
    """
    value = str(value).strip()

    # Thử lần lượt từng định dạng
    for fmt in SUPPORTED_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    # Nếu không parse được, báo lỗi rõ ràng
    raise ValueError(
        f"Định dạng thời gian không hợp lệ: '{value}'.\n"
        f"  Định dạng được hỗ trợ: YYYY-MM-DD HH:MM hoặc DD/MM/YYYY HH:MM"
    )


def calculate_hours(start: datetime, end: datetime) -> float:
    """
    Tính số giờ giữa hai mốc thời gian, làm tròn lên (ceiling).

    Ví dụ: 2 giờ 10 phút → 3 giờ (để đảm bảo thu đủ tiền)

    Args:
        start: Thời điểm bắt đầu
        end  : Thời điểm kết thúc

    Returns:
        Số giờ (float, làm tròn lên), tối thiểu là 1 giờ
    """
    delta = end - start
    total_seconds = delta.total_seconds()

    if total_seconds <= 0:
        return 0.0

    # Làm tròn lên số giờ, tối thiểu 1 giờ
    hours = math.ceil(total_seconds / 3600)
    return float(max(hours, 1))


def format_datetime(dt: datetime) -> str:
    """
    Chuyển đối tượng datetime sang chuỗi theo định dạng chuẩn.

    Args:
        dt: Đối tượng datetime

    Returns:
        Chuỗi ngày giờ, ví dụ "2025-06-01 08:00"
    """
    return dt.strftime(DATETIME_FORMAT)


def get_current_time() -> datetime:
    """Trả về thời gian hiện tại (không có giây)."""
    now = datetime.now()
    # Bỏ giây và microsecond để dễ làm việc
    return now.replace(second=0, microsecond=0)


def format_duration(hours: float) -> str:
    """
    Định dạng số giờ thành chuỗi dễ đọc.

    Ví dụ: 25.0 → "1 ngày 1 giờ"

    Args:
        hours: Số giờ (float)

    Returns:
        Chuỗi mô tả thời lượng
    """
    hours = int(hours)
    if hours < 24:
        return f"{hours} giờ"
    days = hours // 24
    remaining_hours = hours % 24
    if remaining_hours == 0:
        return f"{days} ngày"
    return f"{days} ngày {remaining_hours} giờ"

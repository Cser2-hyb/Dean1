"""Data analysis and sorting logic will be implemented here."""
# ==========================================
# ĐỊNH NGHĨA ĐỐI TƯỢNG: EQUIPMENT (THIẾT BỊ)
# ==========================================
class Equipment:
    def __init__(self, name, rate_per_hour, power):
        self.name = name                  # Tên của thiết bị
        self.rate_per_hour = rate_per_hour  # Giá thuê theo giờ 
        self.power = power                # Công suất của thiết bị 

    # Hàm này giúp khi in thiết bị ra màn hình sẽ đẹp và thẳng hàng hơn
    def __str__(self):
        return f"Equipment: {self.name:<12} | Rate: ${self.rate_per_hour}/h | Power: {self.power}W"


# ==========================================
# CÁC HÀM SẮP XẾP (LOGIC CHÍNH CỦA BÀI)
# ==========================================

# Ý 1: Sắp xếp thiết bị theo giá thuê/giờ (Tăng dần)
def sort_equipment_by_rate(equipment_list):
    # Ra lệnh cho Python sắp xếp danh sách dựa vào thuộc tính 'rate_per_hour'
    equipment_list.sort(key=lambda item: item.rate_per_hour)
    return equipment_list

# Ý 2: Sắp xếp thiết bị theo công suất (Tăng dần)
def sort_equipment_by_power(equipment_list):
    # Ra lệnh cho Python sắp xếp danh sách dựa vào thuộc tính 'power'
    equipment_list.sort(key=lambda item: item.power)
    return equipment_list


# ==========================================
# CHƯƠNG TRÌNH CHẠY THỬ (TEST CODE)
# ==========================================

# 1. Tạo một danh sách các thiết bị mẫu để chạy thử
equipment_list = [
    Equipment("Drill", 50, 800),     # Tên: Drill (Máy khoan), Giá: 50, Công suất: 800
    Equipment("Saw", 30, 1200),      # Tên: Saw (Máy cắt), Giá: 30, Công suất: 1200
    Equipment("Grinder", 45, 500)    # Tên: Grinder (Máy mài), Giá: 45, Công suất: 500
]

print("--- ORIGINAL LIST ---")
for eq in equipment_list:
    print(eq)
print("-" * 50)

# 2. Chạy thử Ý 1: Sắp xếp theo giá thuê
print("\n--- SORTED BY RATE/HOUR  ---")
# Dùng .copy() để tạo bản sao, tránh làm đảo lộn danh sách gốc ban đầu
sorted_by_rate = sort_equipment_by_rate(equipment_list.copy())
for eq in sorted_by_rate:
    print(eq)

# 3. Chạy thử Ý 2: Sắp xếp theo công suất
print("\n--- SORTED BY POWER  ---")
sorted_by_power = sort_equipment_by_power(equipment_list.copy())
for eq in sorted_by_power:
    print(eq)

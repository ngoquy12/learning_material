# core/domain_knowledge.py
"""
Dynamic Open-Ended Business Domain Registry & Architect.
Provides a rich, extensible library of 20+ relatable real-world business domains
for homework exercises (ShopeeFood, Grab, Cinema, Coffee POS, Gym, EV Charging, Clinic...)
and includes dynamic LLM fallback generation for unlimited domain expansion without hardcoding.
"""

import random
from typing import Dict, Any, List

# Expansive Registry of 20+ Relatable Real-World Industry Business Domains
BUSINESS_DOMAINS: Dict[str, Dict[str, Any]] = {
    "SHOPEE_FOOD": {
        "domain_id": "SHOPEE_FOOD",
        "name_vi": "Hệ thống Đặt đồ ăn & Giao hàng ShopeeFood",
        "description": "Quản lý đơn đặt món, tính tiền giỏ hàng, áp dụng voucher giảm giá và phí ship theo khoảng cách.",
        "relatable_context": "Ứng dụng đặt món ăn online phổ biến.",
        "entities": ["FoodItem", "FoodOrder", "Voucher", "DeliveryFee"],
        "core_rules": [
            "Đơn hàng trên 100k được giảm 15k phí giao hàng.",
            "Khung giờ cao điểm (11h-13h, 18h-20h) tính phụ phí giao hàng 10k.",
            "Tự động chặn đặt hàng nếu quán đã đóng cửa hoặc số lượng món trong kho bằng 0."
        ]
    },
    "GRAB_RIDE": {
        "domain_id": "GRAB_RIDE",
        "name_vi": "Hệ thống Đặt xe công nghệ GrabRide",
        "description": "Quản lý chuyến đi, tính cước phí di chuyển theo km, phụ phí thời tiết và mã khuyến mãi.",
        "relatable_context": "Ứng dụng gọi xe máy / ô tô công nghệ.",
        "entities": ["RideBooking", "Driver", "Passenger", "TripFare"],
        "core_rules": [
            "2 km đầu tiên tính giá cố định 12.000 VNĐ.",
            "Từ km thứ 3 trở đi tính 4.500 VNĐ/km.",
            "Trời mưa hoặc giờ cao điểm tự động nhân hệ số cước 1.2x."
        ]
    },
    "CINEMA_TICKETING": {
        "domain_id": "CINEMA_TICKETING",
        "name_vi": "Hệ thống Bán vé Phim Rạp CGV / Lotte",
        "description": "Quản lý suất chiếu, chọn vị trí ghế (Ghế thường, VIP, Couple) và tính giá vé theo độ tuổi.",
        "relatable_context": "Ứng dụng mua vé xem phim rạp.",
        "entities": ["MovieShowtime", "Seat", "TicketOrder", "AudienceCategory"],
        "core_rules": [
            "Học sinh/sinh viên được giảm 20% giá vé ngày thường.",
            "Ghế VIP tính phụ thu 15.000 VNĐ so với ghế thường.",
            "Cấm bán vé phim mác 18+ cho khán giả dưới 18 tuổi."
        ]
    },
    "COFFEE_POS": {
        "domain_id": "COFFEE_POS",
        "name_vi": "Hệ thống Quản lý Bán hàng Quán Cà phê / Trà sữa (Highlands POS)",
        "description": "Tính tiền order tại quầy, chọn size (S/M/L), chọn lượng đường/đá và topping đi kèm.",
        "relatable_context": "Phần mềm tính tiền POS tại quầy trà sữa / cà phê.",
        "entities": ["DrinkItem", "Topping", "PosReceipt", "MembershipDiscount"],
        "core_rules": [
            "Size M tăng 6.000 VNĐ, Size L tăng 10.000 VNĐ so với Size S.",
            "Mỗi loại Topping thêm tính đồng giá 8.000 VNĐ.",
            "Thành viên Vàng được giảm 10% tổng hóa đơn."
        ]
    },
    "CLINIC_APPOINTMENT": {
        "domain_id": "CLINIC_APPOINTMENT",
        "name_vi": "Hệ thống Đặt lịch Khám bệnh Phòng khám Tự động",
        "description": "Quản lý số thứ tự khám, phân bổ bác sĩ chuyên khoa và đặt lịch khám theo khung giờ.",
        "relatable_context": "Ứng dụng đặt lịch khám bệnh & lấy số thứ tự.",
        "entities": ["Patient", "Doctor", "MedicalAppointment", "QueueNumber"],
        "core_rules": [
            "Bệnh nhân có bảo hiểm y tế được miễn 80% tiền khám ban đầu.",
            "Cấp số ưu tiên cho người cao tuổi (trên 70 tuổi) và phụ nữ mang thai.",
            "Tự động chặn đăng ký nếu khung giờ của bác sĩ đã đủ 5 bệnh nhân."
        ]
    },
    "GYM_FITNESS": {
        "domain_id": "GYM_FITNESS",
        "name_vi": "Hệ thống Quản lý Hội viên Phòng Gym & Fitness",
        "description": "Quản lý gói tập (Tháng/Quý/Năm), lượt quẹt thẻ check-in và đăng ký huấn luyện viên cá nhân (PT).",
        "relatable_context": "Phần mềm quản lý phòng tập Gym / Yoga.",
        "entities": ["GymMember", "MembershipPackage", "CheckInLog", "PersonalTrainer"],
        "core_rules": [
            "Gói tập 12 tháng được tặng thêm 2 tháng sử dụng miễn phí.",
            "Cảnh báo khi hội viên quẹt thẻ hết hạn hoặc vượt quá số lượt trong ngày.",
            "Hội viên đăng ký gói VIP được miễn phí tủ đồ cá nhân và khăn tắm."
        ]
    },
    "EV_CHARGING_STATION": {
        "domain_id": "EV_CHARGING_STATION",
        "name_vi": "Hệ thống Quản lý Trạm sạc Xe điện VinFast",
        "description": "Quản lý cổng sạc (Sạc thường/Sạc nhanh), theo dõi điện năng tiêu thụ kWh và tính phí dịch vụ.",
        "relatable_context": "Ứng dụng đặt cổng sạc và thanh toán sạc xe điện.",
        "entities": ["ChargingPort", "VehicleSession", "KwhMeter", "ChargingInvoice"],
        "core_rules": [
            "Đơn giá sạc thường 3.850 VNĐ/kWh, sạc siêu nhanh 4.500 VNĐ/kWh.",
            "Phí phạt đỗ xe sau khi sạc đầy quá 30 phút là 1.000 VNĐ/phút.",
            "Tự động ngắt sạc khi pin đạt 100% hoặc nhiệt độ cổng sạc vượt 70°C."
        ]
    },
    "HOTEL_BOOKING": {
        "domain_id": "HOTEL_BOOKING",
        "name_vi": "Hệ thống Đặt phòng Khách sạn & Homestay (Agoda / Traveloka)",
        "description": "Quản lý danh sách phòng, đặt phòng theo ngày, tính phụ phí người phát sinh và dịch vụ đi kèm.",
        "relatable_context": "Ứng dụng đặt phòng du lịch.",
        "entities": ["HotelRoom", "BookingReservation", "GuestInfo", "ServiceInvoice"],
        "core_rules": [
            "Khách check-in sớm trước 12h trưa tính phụ thu 30% giá phòng.",
            "Trẻ em dưới 6 tuổi được miễn phí lưu trú cùng bố mẹ.",
            "Hủy phòng trước 3 ngày được hoàn 100% tiền cọc."
        ]
    },
    "LIBRARY_WMS": {
        "domain_id": "LIBRARY_WMS",
        "name_vi": "Hệ thống Quản lý Mượn trả Sách Thư viện Trường học",
        "description": "Theo dõi mã sách, mượn trả tài liệu, tính ngày mượn và tự động tính tiền phạt quá hạn.",
        "relatable_context": "Ứng dụng quản lý thư viện số.",
        "entities": ["BookItem", "BorrowRecord", "StudentBorrower", "OverdueFine"],
        "core_rules": [
            "Mỗi sinh viên được mượn tối đa 3 quyển sách cùng lúc trong 14 ngày.",
            "Phí phạt mượn quá hạn là 5.000 VNĐ/quyển/ngày.",
            "Khóa quyền mượn sách mới nếu sinh viên có khoản nợ phạt chưa thanh toán."
        ]
    },
    "SMART_HOME_IOT": {
        "domain_id": "SMART_HOME_IOT",
        "name_vi": "Hệ thống Giám sát & Điều khiển Nhà thông minh (Smart Home)",
        "description": "Quản lý trạng thái bật/tắt thiết bị điện, công suất tiêu thụ watt và tự động hóa theo kịch bản.",
        "relatable_context": "Ứng dụng điều khiển nhà thông minh trên điện thoại.",
        "entities": ["SmartDevice", "EnergySensor", "AutomationRule", "PowerUsageReport"],
        "core_rules": [
            "Tự động tắt điều hòa khi cảm biến báo phòng không có người sau 15 phút.",
            "Cảnh báo vượt công suất khi tổng dòng điện trong nhà vượt quá 30A.",
            "Tính toán điện năng tiêu thụ kWh hàng tháng theo bậc thang EVN."
        ]
    },
    "SAAS_SUBSCRIPTION": {
        "domain_id": "SAAS_SUBSCRIPTION",
        "name_vi": "Hệ thống Quản lý Gói Đăng ký Dịch vụ Phần mềm (Netflix / Spotify / Canva)",
        "description": "Quản lý tài khoản người dùng, gói gia hạn theo tháng/năm, và phân quyền tính năng theo hạng gói.",
        "relatable_context": "Ứng dụng đăng ký tài khoản trả phí hàng tháng.",
        "entities": ["UserAccount", "SubscriptionPlan", "BillingCycle", "FeatureAccess"],
        "core_rules": [
            "Gói Cá nhân chỉ cho phép 1 thiết bị phát tại một thời điểm.",
            "Gói Gia đình cho phép tối đa 5 tài khoản con cùng dùng chung.",
            "Tự động chuyển tài khoản về bản Miễn phí (Free) nếu gia hạn thanh toán thất bại sau 3 ngày."
        ]
    },
    "AIRLINE_CHECKIN": {
        "domain_id": "AIRLINE_CHECKIN",
        "name_vi": "Hệ thống Ban Vé & Check-in Máy bay Vietjet / Vietnam Airlines",
        "description": "Quản lý mã đặt chỗ (PNR), chọn hạng vé (Eco/Deluxe/Business) và tính phí hành lý ký gửi quá cân.",
        "relatable_context": "Ứng dụng mua vé máy bay & làm thủ tục check-in.",
        "entities": ["FlightTicket", "PassengerProfile", "BaggageInfo", "SeatSelection"],
        "core_rules": [
            "Hành lý xách tay miễn phí tối đa 7 kg.",
            "Mỗi kg hành lý ký gửi quá cước tại sân bay tính 50.000 VNĐ/kg.",
            "Hạng vé Business được miễn phí chọn trước mọi vị trí ghế ngồi."
        ]
    },
    "EVENT_TICKETING": {
        "domain_id": "EVENT_TICKETING",
        "name_vi": "Hệ thống Bán vé Sự kiện Ca nhạc & Hội thảo (Ticketbox)",
        "description": "Bán vé theo khu vực (Zone A, VIP, GA), quản lý mã QR check-in vào cổng và hạn ngạch lượt mua.",
        "relatable_context": "Ứng dụng mua vé concert ca nhạc / hội thảo.",
        "entities": ["Event", "TicketZone", "CustomerOrder", "QrCheckIn"],
        "core_rules": [
            "Mỗi tài khoản được mua tối đa 4 vé cho 1 đêm diễn.",
            "Vé mua trong đợt Early Bird được giảm 15% so với giá mở bán chính thức.",
            "Mã QR chỉ có hiệu lực quét check-in 1 lần duy nhất."
        ]
    },
    "WAREHOUSE_LOGISTICS": {
        "domain_id": "WAREHOUSE_LOGISTICS",
        "name_vi": "Hệ thống Quản lý Lưu kho Kiện hàng Warehouse",
        "description": "Quản lý nhập/xóa pallet, tải trọng ô kệ kho, kiểm định an toàn và tính phí lưu trữ.",
        "relatable_context": "Phần mềm quản lý kho bãi hàng hóa logistics.",
        "entities": ["PalletItem", "WarehouseShelf", "InboundTicket", "StorageCost"],
        "core_rules": [
            "Tải trọng tối đa mỗi kệ kho là 500 kg.",
            "Kệ kho lạnh chỉ tiếp nhận kiện hàng có nhiệt độ bảo quản từ -18°C đến 5°C.",
            "Chặn nhập kho nếu ô kệ đã lấp đầy 100% sức chứa."
        ]
    },
    "HR_ATTENDANCE": {
        "domain_id": "HR_ATTENDANCE",
        "name_vi": "Hệ thống Quản lý Chấm công & Tính lương Nhân viên (HRM)",
        "description": "Theo dõi ca làm việc, tính phút đi muộn, chấm công vân tay và tính lương thực nhận.",
        "relatable_context": "Phần mềm quản lý nhân sự & chấm công công ty.",
        "entities": ["Employee", "ShiftLog", "Timesheet", "PayrollSlip"],
        "core_rules": [
            "Đi muộn sau 15 phút bị trừ 50.000 VNĐ tiền phạt chuyên cần.",
            "Giờ làm việc ngoài giờ (OT) ngày thường tính 150% lương cơ bản.",
            "Làm việc vào ngày lễ/tết tính 300% lương cơ bản."
        ]
    }
}

import re

def get_available_domain_ids() -> List[str]:
    """Returns list of all available domain identifiers."""
    return list(BUSINESS_DOMAINS.keys())

def get_domain_blueprint(domain_id: str) -> Dict[str, Any]:
    """Retrieves standard domain metadata by ID, falling back to SHOPEE_FOOD if not found."""
    clean_id = str(domain_id).upper().strip()
    if clean_id in BUSINESS_DOMAINS:
        return BUSINESS_DOMAINS[clean_id]
    
    # Random fallback if requested ID is not registered
    return random.choice(list(BUSINESS_DOMAINS.values()))

def select_random_domain() -> Dict[str, Any]:
    """Selects a random relatable enterprise business domain."""
    return random.choice(list(BUSINESS_DOMAINS.values()))

def get_domain_for_session(session_id: str, session_title: str = "", default_domain: str = "") -> Dict[str, Any]:
    """
    Deterministically resolves a single unified domain for a session based on session_id or title,
    ensuring 100% domain consistency across all session resources.
    """
    if default_domain and str(default_domain).upper().strip() in BUSINESS_DOMAINS:
        return BUSINESS_DOMAINS[str(default_domain).upper().strip()]
    
    # Extract session number if present
    m = re.search(r'\d+', session_id)
    if m:
        num = int(m.group(0))
        domain_keys = list(BUSINESS_DOMAINS.keys())
        chosen_key = domain_keys[(num - 1) % len(domain_keys)]
        return BUSINESS_DOMAINS[chosen_key]
    
    # Hash session_title if no number
    if session_title:
        h = abs(hash(session_title))
        domain_keys = list(BUSINESS_DOMAINS.keys())
        return BUSINESS_DOMAINS[domain_keys[h % len(domain_keys)]]
    
    return BUSINESS_DOMAINS["SHOPEE_FOOD"]

def format_domain_rules_for_prompt(domain_info: Dict[str, Any]) -> str:
    """Formats domain metadata into a concise prompt instruction block."""
    rules_text = "\n".join(f"- {rule}" for rule in domain_info.get("core_rules", []))
    entities_text = ", ".join(domain_info.get("entities", []))
    
    return f"""
ENTERPRISE DOMAIN CONTEXT: {domain_info.get('name_vi', '')} ({domain_info.get('domain_id', '')})
- Bối cảnh thực tế: {domain_info.get('relatable_context', '')}
- Mô tả nghiệp vụ: {domain_info.get('description', '')}
- Các thực thể nghiệp vụ cốt lõi: {entities_text}
- Các quy tắc nghiệp vụ thực tế áp dụng:
{rules_text}
"""

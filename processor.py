import pandas as pd
from scraper import cao_du_lieu_tu_dong_100  # Gọi trực tiếp module cào dữ liệu vừa sửa ở trên

def thuat_toan_phan_loai_nganh(tieu_de):
    """
    Thuật toán phân loại dựa trên quy tắc (Rule-based) dùng Ma trận từ khóa của sinh viên.
    Chuyển tiêu đề về chữ thường để so khớp chính xác.
    """
    tieu_de_lower = tieu_de.lower()
    
    # 1. Định nghĩa ma trận từ khóa cho 4 ngành của Khoa
    it_keywords = ['it', 'lập trình', 'software', 'developer', 'python', 'java', 'web', 'data', 'mạng', 'phần mềm', 'qa', 'qc']
    oto_keywords = ['ô tô', 'automotive', 'động cơ', 'xe máy', 'chassis', 'garage', 'sửa chữa ô tô', 'vinfast']
    cokhi_keywords = ['cơ khí', 'chế tạo', 'cnc', 'solidworks', 'autocad', 'thiết kế máy', 'gia công']
    tdh_keywords = ['tự động hóa', 'automation', 'plc', 'scada', 'biến tần', 'điện công nghiệp', 'hệ thống nhúng']
    
    # 2. Logic kiểm tra trùng khớp từ khóa
    if any(kw in tieu_de_lower for kw in it_keywords):
        return "Công nghệ thông tin"
    elif any(kw in tieu_de_lower for kw in oto_keywords):
        return "Công nghệ kỹ thuật ô tô"
    elif any(kw in tieu_de_lower for kw in cokhi_keywords):
        return "Cơ khí"
    elif any(kw in tieu_de_lower for kw in tdh_keywords):
        return "Tự động hóa"
    else:
        return "Ngành khác / Chưa phân loại"

def thuc_thi_xu_ly_du_lieu():
    print("=========================================================")
    print("⏳ HỆ THỐNG ĐANG KÍCH HOẠT QUY TRÌNH XỬ LÝ NỘI DUNG 3...")
    print("=========================================================")
    
    # Quy trình 1: Gọi module Scraper lấy dữ liệu thô về
    du_lieu_tho = cao_du_lieu_tu_dong_100()
    
    if not du_lieu_tho:
        print("❌ Không có dữ liệu thô để xử lý. Vui lòng kiểm tra lại scraper!")
        return
        
    # Quy trình 2: Sử dụng thư viện Pandas biến danh sách thành bảng dữ liệu (DataFrame)
    df = pd.DataFrame(du_lieu_tho)
    print(f"📊 Đã tiếp nhận {len(df)} bản ghi thô ban đầu.")
    
    # Quy trình 3: Làm sạch dữ liệu (Xóa bỏ các tin trùng lặp link ứng tuyển nếu có)
    df.drop_duplicates(subset=['Link'], inplace=True)
    print(f"🧹 Sau khi làm sạch và xóa trùng, còn lại: {len(df)} bản ghi.")
    
    # Quy trình 4: Áp dụng thuật toán gắn nhãn ngành học tự động cho từng dòng dữ liệu
    print("🤖 Đang chạy thuật toán phân loại đa ngành bằng Ma trận từ khóa...")
    df['Ngành học'] = df['Tiêu đề'].apply(thuat_toan_phan_loai_nganh)
    
    # Quy trình 5: Xuất kết quả ra file cơ sở dữ liệu dạng CSV "0 đồng"
    ten_file_output = "jobs.csv"
    df.to_csv(ten_file_output, index=False, encoding="utf-8-sig")
    
    print(f"🎉 HOÀN THÀNH NỘI DUNG 3! Cơ sở dữ liệu đã lưu tại: {ten_file_output}")
    print("\n📊 THỐNG KÊ SỐ LƯỢNG CÔNG VIỆC THEO NGÀNH:")
    print(df['Ngành học'].value_counts())
    print("=========================================================")

# Lệnh kích hoạt chạy toàn bộ quy trình Nội dung 3
if __name__ == "__main__":
    thuc_thi_xu_ly_du_lieu()
import streamlit as st
import pandas as pd
import os

# 1. CẤU HÌNH TRANG WEB (Hiển thị trên tab trình duyệt)
st.set_page_config(
    page_title="Hệ thống Việc làm Sinh viên Kỹ thuật",
    page_icon="🤖",
    layout="wide"
)

# 2. ĐƯỜNG DẪN ĐẾN FILE CƠ SỞ DỮ LIỆU
ten_file_data = "jobs.csv"

# Kiểm tra sự tồn tại của file dữ liệu trước khi dựng giao diện
if not os.path.exists(ten_file_data):
    st.error(f"❌ Không tìm thấy file dữ liệu '{ten_file_data}'!")
    st.info("👉 Hướng dẫn: Sinh viên cần chạy file 'processor.py' trước để tạo ra file CSV này.")
else:
    # Tải dữ liệu từ file CSV vào bảng Pandas
    df = pd.read_csv(ten_file_data)
    
    # 3. PHẦN TIÊU ĐỀ CHÍNH CỦA WEBSITE
    st.title("🚀 HỆ THỐNG PHÂN LOẠI VÀ GỢI Ý VIỆC LÀM TỰ ĐỘNG")
    st.subheader("Dành cho Sinh viên các ngành Công nghệ & Kỹ thuật")
    st.markdown("---")
    
    # 4. KHU VỰC THỐNG KÊ TỔNG QUAN (Metrics)
    st.subheader("📊 Thống kê tổng quan hệ thống")
    
    # Tính toán số lượng tin theo từng ngành
    tong_so_tin = len(df)
    tin_it = len(df[df['Ngành học'] == "Công nghệ thông tin"])
    tin_oto = len(df[df['Ngành học'] == "Công nghệ kỹ thuật ô tô"])
    tin_cokhi = len(df[df['Ngành học'] == "Cơ khí"])
    tin_tdh = len(df[df['Ngành học'] == "Tự động hóa"])
    
    # Hiển thị số liệu dạng thẻ (Card) chia làm 5 cột
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Tổng số việc làm", value=tong_so_tin)
    with col2:
        st.metric(label="💻 CNTT", value=tin_it)
    with col3:
        st.metric(label="🚗 Kỹ thuật Ô tô", value=tin_oto)
    with col4:
        st.metric(label="⚙️ Cơ khí", value=tin_cokhi)
    with col5:
        st.metric(label="🕹️ Tự động hóa", value=tin_tdh)
        
    st.markdown("---")
    
    # 5. KHU VỰC BỘ LỌC TƯƠNG TÁC (Thanh Sidebar bên trái)
    st.sidebar.header("🎯 Bộ lọc tìm kiếm thông minh")
    
    # Bộ lọc từ khóa
    tu_khoa_tim = st.sidebar.text_input("Nhập từ khóa tuyển dụng (Ví dụ: Intern, Thực tập...):")
    
    # Bộ lọc chuyên ngành
    danh_sach_nganh = ["Tất cả các ngành"] + list(df['Ngành học'].unique())
    nganh_duoc_chon = st.sidebar.selectbox("Chọn chuyên ngành của bạn:", danh_sach_nganh)
    
    # 6. TIẾN HÀNH LỌC DỮ LIỆU
    df_loc = df.copy()
    
    # Lọc theo ngành học
    if nganh_duoc_chon != "Tất cả các ngành":
        df_loc = df_loc[df_loc['Ngành học'] == nganh_duoc_chon]
        
    # Lọc theo từ khóa tiêu đề (Không phân biệt chữ hoa/thường)
    if tu_khoa_tim:
        df_loc = df_loc[df_loc['Tiêu đề'].str.contains(tu_khoa_tim, case=False, na=False)]
        
    # 7. HIỂN THỊ BIỂU ĐỒ TRỰC QUAN
    st.subheader("📈 Biểu đồ cơ cấu nhu cầu tuyển dụng")
    thong_ke_nganh = df_loc['Ngành học'].value_counts()
    st.bar_chart(thong_ke_nganh)
    
    st.markdown("---")
    
    # 8. HIỂN THỊ DANH SÁCH VIỆC LÀM (An toàn tuyệt đối, tránh lỗi chuỗi)
    st.subheader(f"📋 Danh sách việc làm phù hợp ({len(df_loc)} kết quả)")
    
    if df_loc.empty:
        st.warning("😭 Không tìm thấy công việc nào phù hợp với bộ lọc hiện tại.")
    else:
        # Duyệt qua từng dòng dữ liệu để hiển thị tin
        for idx, row in df_loc.iterrows():
            # Tách riêng các biến ra trước để đảm bảo an toàn cú pháp
            tieu_de_tin = str(row['Tiêu đề'])
            cong_ty_tin = str(row['Công ty'])
            nganh_tin = str(row['Ngành học'])
            link_tin = str(row['Link'])
            
            # Dựng giao diện hiển thị bằng các hàm Streamlit thuần túy thay vì Markdown phức tạp
            with st.container():
                st.write(f"### 📌 {tieu_de_tin}")
                
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"🏢 **Doanh nghiệp:** {cong_ty_tin}")
                with c2:
                    st.info(f"📁 Chuyên ngành: {nganh_tin}")
                    
                # Tạo đường link ứng tuyển sạch
                st.markdown(f"[🔗 Xem chi tiết & Ứng tuyển tại đây]({link_tin})")
                st.write("---") # Đường kẻ mờ phân cách giữa các tin

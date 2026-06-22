import streamlit as st
import pandas as pd
import os

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ thống Việc làm Sinh viên Kỹ thuật",
    page_icon="🤖",
    layout="wide"
)

# 2. ĐƯỜNG DẪN ĐẾN FILE CƠ SỞ DỮ LIỆU TĨNH TRÊN GITHUB
ten_file_data = "jobs.csv"

# Kiểm tra sự tồn tại của file dữ liệu trước khi dựng giao diện để tránh lỗi sập trang
if not os.path.exists(ten_file_data):
    st.error(f"❌ Không tìm thấy file cơ sở dữ liệu '{ten_file_data}' trên GitHub!")
    st.info("👉 Hướng dẫn: Sinh viên cần upload file 'jobs.csv' (đã chạy ra kết quả từ máy tính) lên kho chứa GitHub này.")
else:
    try:
        # Tải dữ liệu từ file CSV
        df = pd.read_csv(ten_file_data)
        
        # 3. PHẦN TIÊU ĐỀ CHÍNH CỦA WEBSITE
        st.title("🚀 HỆ THỐNG PHÂN LOẠI VÀ GỢI Ý VIỆC LÀM TỰ ĐỘNG")
        st.subheader("Dành cho Sinh viên các ngành Công nghệ & Kỹ thuật")
        st.markdown("---")
        
        # 4. KHU VỰC THỐNG KÊ TỔNG QUAN (Metrics Dashboard)
        st.subheader("📊 Thống kê tổng quan hệ thống")
        
        tong_so_tin = len(df)
        tin_it = len(df[df['Ngành học'] == "Công nghệ thông tin"])
        tin_oto = len(df[df['Ngành học'] == "Công nghệ kỹ thuật ô tô"])
        tin_cokhi = len(df[df['Ngành học'] == "Cơ khí"])
        tin_tdh = len(df[df['Ngành học'] == "Tự động hóa"])
        
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
        tu_khoa_tim = st.sidebar.text_input("Nhập từ khóa tuyển dụng (Ví dụ: Intern, Thực tập...):")
        
        danh_sach_nganh = ["Tất cả các ngành"] + list(df['Ngành học'].unique())
        nganh_duoc_chon = st.sidebar.selectbox("Chọn chuyên ngành của bạn:", danh_sach_nganh)
        
        # 6. TIẾN HÀNH LỌC DỮ LIỆU
        df_loc = df.copy()
        if nganh_duoc_chon != "Tất cả các ngành":
            df_loc = df_loc[df_loc['Ngành học'] == nganh_duoc_chon]
            
        if tu_khoa_tim:
            df_loc = df_loc[df_loc['Tiêu đề'].str.contains(tu_khoa_tim, case=False, na=False)]
            
        # 7. HIỂN THỊ BIỂU ĐỒ TRỰC QUAN
        st.subheader("📈 Biểu đồ cơ cấu nhu cầu tuyển dụng")
        thong_ke_nganh = df_loc['Ngành học'].value_counts()
        st.bar_chart(thong_ke_nganh)
        
        st.markdown("---")
        
        # 8. HIỂN THỊ DANH SÁCH VIỆC LÀM (Sử dụng hàm st.write sạch để tránh hoàn toàn lỗi dấu ngoặc)
        st.subheader(f"📋 Danh sách việc làm phù hợp ({len(df_loc)} kết quả)")
        
        if df_loc.empty:
            st.warning("😭 Không tìm thấy công việc nào phù hợp với bộ lọc hiện tại.")
        else:
            for idx, row in df_loc.iterrows():
                tieu_de_tin = str(row['Tiêu đề'])
                cong_ty_tin = str(row['Công ty'])
                nganh_tin = str(row['Ngành học'])
                link_tin = str(row['Link'])
                
                with st.container():
                    st.write("### 📌 " + tieu_de_tin)
                    
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write("🏢 **Doanh nghiệp:** " + cong_ty_tin)
                    with c2:
                        st.info("📁 Chuyên ngành: " + nganh_tin)
                        
                    st.markdown(f"[🔗 Xem chi tiết & Ứng tuyển tại đây]({link_tin})")
                    st.write("---")

    except Exception as e:
        st.error(f"❌ Có lỗi phát sinh khi xử lý cấu trúc dữ liệu: {e}")

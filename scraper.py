import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def cao_du_lieu_tu_dong_100():
    """
    Hàm sử dụng Selenium điều khiển trình duyệt Chrome ảo để tự động cào dữ liệu.
    Đã được tối ưu chạy ngầm (Headless) để phối hợp mượt mà với module xử lý dữ liệu.
    """
    print("🔄 Bước 1.1: Đang khởi tạo trình duyệt Chrome ngầm (Headless)...")
    
    # Cấu hình tối ưu cho Selenium chạy trên máy ảo hoặc chạy ngầm không giao diện
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Chạy ngầm để không giải phóng giao diện gây rối mắt cho người dùng
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Tự động quản lý và nạp WebDriver tương thích với Chrome trên máy
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://ybox.vn/tuyen-dung"
    danh_sach_tin = []
    
    try:
        print(f"🌐 Bước 1.2: Trình duyệt ảo đang truy cập: {url}")
        driver.get(url)
        
        # Chờ 4 giây để trang web kích hoạt JavaScript và render giao diện
        time.sleep(4)
        
        # Cuộn chuột tự động 2 lần để kích hoạt tải thêm dữ liệu mới
        print("📜 Bước 1.3: Đang cuộn trang tự động để lấy dữ liệu thời gian thực...")
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
        # Nạp toàn bộ mã nguồn HTML đã dựng hoàn chỉnh từ trình duyệt ảo
        html_hoan_chinh = driver.page_source
        
        # Tắt trình duyệt ngay sau khi lấy xong để tối ưu và giải phóng bộ nhớ RAM
        driver.quit()
        print("🛑 Bước 1.4: Thu thập HTML hoàn tất, đóng trình duyệt ảo.")
        
        # --- TIẾN HÀNH TRÍCH XUẤT DỮ LIỆU ---
        soup = BeautifulSoup(html_hoan_chinh, "html.parser")
        tat_ca_the_a = soup.find_all("a")
        
        # Bộ lọc từ khóa cơ bản để nhận diện các tin liên quan đến cơ hội việc làm
        tu_khoa = ["tuyển", "tuyển dụng", "intern", "thực tập", "job", "hiring", "việc làm", "kỹ sư", "cơ khí", "ô tô", "lập trình"]
        cac_link_da_quet = set()
        
        for the_a in tat_ca_the_a:
            tieu_de = the_a.text.strip()
            link = the_a.get("href", "")
            
            # Kiểm tra tiêu đề có hợp lệ và chứa từ khóa việc làm hay không
            if len(tieu_de) > 15 and any(tu in tieu_de.lower() for tu in tu_khoa):
                # Chuẩn hóa đường link (Bù domain nếu thiếu)
                if link.startswith("//"):
                    link = "https:" + link
                elif link.startswith("/"):
                    link = "https://ybox.vn" + link
                    
                # Chống trùng lặp link trong quá trình duyệt danh sách thẻ a
                if link in cac_link_da_quet or not link.startswith("http"):
                    continue
                    
                cac_link_da_quet.add(link)
                
                # Đóng gói dữ liệu thô
                danh_sach_tin.append({
                    "Tiêu đề": tieu_de,
                    "Công ty": "Xem chi tiết tại link gốc",
                    "Link": link
                })
                
        return danh_sach_tin

    except Exception as e:
        print(f"❌ Lỗi phát sinh tại Module Scraper: {e}")
        try:
            driver.quit()
        except:
            pass
        return []
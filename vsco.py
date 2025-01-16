import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request as ur
import traceback as tb
import json
import re

# Konfigurasi ChromeDriver
chrome_options = Options()
chrome_service = Service("chromedriver.exe")  

# Fungsi untuk memilih bahasa
def pilih_bahasa():
    print("Pilih bahasa:")
    print("1. English")
    print("2. Indonesia")
    print("3. 中文 (Chinese)")
    pilihan = input("Masukkan pilihan (1/2/3): ")
    if pilihan == "1":
        return "en"
    elif pilihan == "2":
        return "id"
    elif pilihan == "3":
        return "zh"
    else:
        print("Pilihan tidak valid, menggunakan English secara default.")
        return "en"

# Terjemahan
TRANSLATIONS = {
    "en": {
        "enter_email": "Enter email: ",
        "enter_password": "Enter password: ",
        "enter_username": "Enter username: ",
        "login_success": "[INFO] Login successful.",
        "login_page": "[INFO] Opening login page...",
        "fill_email_password": "[INFO] Filling in email and password...",
        "open_profile_page": "[INFO] Opening profile page: {url}",
        "load_more_button": "[INFO] Clicking 'Load More' button...",
        "no_more_load_more": "[INFO] No more 'Load More' buttons or all content loaded.",
        "scroll_down": "[INFO] Scrolling down to load content...",
        "no_new_content": "[INFO] No new content loaded.",
        "fetch_links": "[INFO] Fetching media links...",
        "download_success": "[INFO] Successfully downloaded: {filename}",
        "start_extraction": "[INFO] Starting link extraction...",
        "found_links": "[INFO] Found {count} links. Downloading media...",
        "download_complete": "[INFO] All results saved in folder: {folder}",
        "error": "[ERROR] An error occurred: {error}",
        "select_download_method": "Select download method:",
        "method_1": "1. Download using username (login required).",
        "method_2": "2. Download using file links.txt (no login required).",
        "method_3": "3. Download using paste single links (no login required).",
        "invalid_choice": "Invalid choice, defaulting to login method.",
        "enter_media_url": "Enter media URL (e.g., https://vsco.co/janefluff/media/66006e145d173b263ec58693): ",
        "start_downloading": "Starting to download media from",
    },
    "id": {
        "enter_email": "Masukkan email: ",
        "enter_password": "Masukkan password: ",
        "enter_username": "Masukkan username: ",
        "login_success": "[INFO] Login berhasil.",
        "login_page": "[INFO] Membuka halaman login...",
        "fill_email_password": "[INFO] Mengisi email dan password...",
        "open_profile_page": "[INFO] Membuka halaman profil: {url}",
        "load_more_button": "[INFO] Klik tombol 'Load More'...",
        "no_more_load_more": "[INFO] Tidak ada tombol 'Load More' lagi atau semua konten telah dimuat.",
        "scroll_down": "[INFO] Scroll ke bawah untuk memuat konten...",
        "no_new_content": "[INFO] Tidak ada konten baru yang dimuat.",
        "fetch_links": "[INFO] Mengambil tautan media...",
        "download_success": "[INFO] Berhasil mengunduh: {filename}",
        "start_extraction": "[INFO] Memulai pengambilan tautan...",
        "found_links": "[INFO] Ditemukan {count} tautan. Mengunduh media...",
        "download_complete": "[INFO] Semua hasil disimpan di folder: {folder}",
        "error": "[ERROR] Terjadi kesalahan: {error}",
        "select_download_method": "Pilih metode download:",
        "method_1": "1. Download menggunakan username (login diperlukan).",
        "method_2": "2. Download menggunakan file links.txt (tanpa login).",
        "method_3": "3. Download menggunakan paste satu links (tanpa login).",
        "invalid_choice": "Pilihan tidak valid, memilih metode login secara default.",
        "enter_media_url": "Masukkan URL media (misal: https://vsco.co/janefluff/media/66006e145d173b263ec58693): ",
        "start_downloading": "Mulai mengunduh media dari",
    },
    "zh": {
        "enter_email": "输入电子邮件：",
        "enter_password": "输入密码：",
        "enter_username": "输入用户名：",
        "login_success": "[INFO] 登录成功。",
        "login_page": "[INFO] 打开登录页面...",
        "fill_email_password": "[INFO] 填写电子邮件和密码...",
        "open_profile_page": "[INFO] 打开个人资料页面：{url}",
        "load_more_button": "[INFO] 点击“加载更多”按钮...",
        "no_more_load_more": "[INFO] 没有更多的“加载更多”按钮或所有内容已加载。",
        "scroll_down": "[INFO] 向下滚动以加载内容...",
        "no_new_content": "[INFO] 没有加载新内容。",
        "fetch_links": "[INFO] 获取媒体链接...",
        "download_success": "[INFO] 成功下载：{filename}",
        "start_extraction": "[INFO] 开始提取链接...",
        "found_links": "[INFO] 找到 {count} 个链接。 正在下载媒体...",
        "download_complete": "[INFO] 所有结果保存在文件夹中：{folder}",
        "error": "[ERROR] 出现错误：{error}",
        "select_download_method": "选择下载方法：",
        "method_1": "1. 使用用户名下载（需要登录）。",
        "method_2": "2. 使用文件 links.txt 下载（无需登录）。",
        "method_3": "3. 使用粘贴单个链接下载（无需登录）。",
        "invalid_choice": "无效的选择，默认选择登录方法。",
        "enter_media_url": "请输入媒体URL（例如：https://vsco.co/janefluff/media/66006e145d173b263ec58693）：",
        "start_downloading": "开始从",
    },
}

# Fungsi untuk mendapatkan teks berdasarkan bahasa
def get_text(key, lang, **kwargs):
    text = TRANSLATIONS[lang].get(key, key)
    return text.format(**kwargs)

# Pemilihan bahasa
bahasa = pilih_bahasa()

# Fungsi utama untuk memilih metode download
def pilih_metode_download():
    print(get_text("select_download_method", bahasa))
    print(get_text("method_1", bahasa))
    print(get_text("method_2", bahasa))
    print(get_text("method_3", bahasa))
    pilihan = input(get_text("Masukkan pilihan (1/2): ", bahasa))
    if pilihan == "1":
        return "login"
    elif pilihan == "2":
        return "file"
    elif pilihan == "3":
        return "single_link"
    else:
        print(get_text("invalid_choice", bahasa))
        return "login"

# Pilih metode download
metode = pilih_metode_download()

# Fungsi untuk login ke VSCO
def login_to_vsco(driver):
    login_url = "https://vsco.co/user/login"
    driver.get(login_url)
    print(get_text("login_page", bahasa))
    
    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identity")))
    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    
    
    print(get_text("fill_email_password", bahasa))
    email_input.send_keys(email)
    password_input.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
    login_button.click()
    print(get_text("login_success", bahasa))
    time.sleep(5)

# Fungsi untuk mengekstrak semua tautan media
def extract_vsco_links(url):
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    try:
        login_to_vsco(driver)
        driver.get(url)
        print(get_text("open_profile_page", bahasa, url=profile_url))
        time.sleep(5)

        # Klik tombol "Load More" hingga tidak ada lagi
        while True:
            try:
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "grain-button"))
                )
                print(get_text("load_more_button", bahasa))
                load_more_button.click()
                time.sleep(3)
            except Exception:
                print(get_text("no_more_load_more", bahasa))
                break

        # Scroll ke bawah hingga tidak ada konten baru
        last_height = 0
        while True:
            print(get_text("scroll_down", bahasa))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(get_text("no_new_content", bahasa))
                break
            last_height = new_height

        # Ambil semua tautan posting
        print(get_text("fetch_links", bahasa))
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        post_links = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href") and "media" in link.get_attribute("href")
        ]

        # Hilangkan duplikat tautan
        unique_links = list(set(post_links))
        return unique_links

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")
        return []
    finally:
        driver.quit()

# Fungsi untuk mengunduh media dari tautan
def download(vsco_media_url, output_path, get_video_thumbnails=True, save=True):
    request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    request = ur.Request(vsco_media_url, headers=request_header)
    data = ur.urlopen(request).read()

    data_cleaned_1 = str(data).split("<script>window.__PRELOADED_STATE__ =")[1]
    data_cleaned_2 = str(data_cleaned_1).split("</script>")[0]
    data_cleaned_3 = str(data_cleaned_2).strip()
    data_cleaned_4 = str(data_cleaned_3).replace("\\x", "\\u00")
    data_cleaned_5 = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', data_cleaned_4)

    try:
        json_data = json.loads(data_cleaned_5)
    except Exception as e:
        print("ERROR: Failed to load json data!")
        tb.print_exc()
        return 1

    opener = ur.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64)")]
    ur.install_opener(opener)

    try:
        medias = json_data["medias"]["byId"]
        for media in medias:
            info = medias[media]["media"]
            media_name = os.path.join(output_path, f"{media}.{'mp4' if bool(info['isVideo']) else 'jpg'}")
            media_url = "https://" + str(
                (info["videoUrl"] if bool(info["isVideo"]) else info["responsiveUrl"]).encode().decode("unicode-escape")
            )
            if save:
                ur.urlretrieve(media_url, media_name)
            print(get_text("download_success", bahasa, filename=media_name))
    except Exception as e:
        print("ERROR: Failed to extract image/video location!")
        tb.print_exc()
        return 1

# Fungsi untuk membaca tautan dari file links.txt
def read_links_from_file(file_path):
    links = []
    try:
        with open(file_path, 'r') as file:
            links = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"[ERROR] File {file_path} tidak ditemukan!")
    return links



# Program utama
if __name__ == '__main__':
    print(get_text("start_extraction", bahasa))

    if metode == "login":
        # Input dari pengguna hanya untuk metode login
        email = input(get_text("enter_email", bahasa))
        password = input(get_text("enter_password", bahasa))
        username = input(get_text("enter_username", bahasa))

        profile_url = f"https://vsco.co/{username}"
        output_dir = os.path.join(os.getcwd(), username)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Ekstrak link menggunakan login (dari username)
            links = extract_vsco_links(profile_url)
            print(get_text("found_links", bahasa, count=len(links)))

            # Simpan semua tautan ke dalam file teks
            links_file_path = os.path.join(output_dir, f"{username}.txt")
            with open(links_file_path, "w") as links_file:
                for link in links:
                    links_file.write(link + "\n")

            # Download media berdasarkan tautan
            for link in links:
                download(link, output_dir)
            print(get_text("download_complete", bahasa, folder=output_dir))
        except Exception as e:
            print(get_text("error", bahasa, error=e))

    elif metode == "file":
        # Baca tautan dari file links.txt dan download media
        links_file_path = os.path.join(os.getcwd(), "links.txt")
        links = read_links_from_file(links_file_path)

        if links:
            print(get_text("found_links", bahasa, count=len(links)))
            output_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(output_dir, exist_ok=True)
            for link in links:
                download(link, output_dir)
            print(get_text("download_complete", bahasa, folder=output_dir))
        else:
            print(get_text("error", bahasa, error="Tidak ada tautan yang ditemukan."))
    
    # Fungsi untuk menangani download berdasarkan satu link media yang dimasukkan
    elif metode == "single_link":
        # Menangani download berdasarkan satu link media yang dimasukkan
        url = input(get_text("enter_media_url", bahasa)) 
        print(f"[INFO] {get_text('start_downloading', bahasa)} {url}...")  

        output_dir = os.path.join(os.getcwd(), "single_link_downloads")
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Panggil fungsi download untuk mengunduh media dari URL tunggal
            download(url, output_dir)
            print(get_text("download_complete", bahasa, folder=output_dir))
        except Exception as e:
            print(get_text("error", bahasa, error="Terjadi kesalahan saat mengunduh media."))

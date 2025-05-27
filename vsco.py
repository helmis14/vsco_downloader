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
from bs4 import BeautifulSoup
from html import unescape
from tqdm import tqdm
import time


chrome_options = Options()
chrome_service = Service("chromedriver.exe")  

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


def get_text(key, lang, **kwargs):
    text = TRANSLATIONS[lang].get(key, key)
    return text.format(**kwargs)


bahasa = pilih_bahasa()


def pilih_metode_download():
    print(get_text("select_download_method", bahasa))
    print(get_text("method_1", bahasa))
    print(get_text("method_2", bahasa))
    print(get_text("method_3", bahasa))
    pilihan = input(get_text("Masukkan pilihan (1/2/3): ", bahasa))
    if pilihan == "1":
        return "login"
    elif pilihan == "2":
        return "file"
    elif pilihan == "3":
        return "single_link"
    else:
        print(get_text("invalid_choice", bahasa))
        return "login"


metode = pilih_metode_download()


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


def extract_vsco_links(url):
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        login_to_vsco(driver)
        driver.get(url)
        print(get_text("open_profile_page", bahasa, url=url))
        time.sleep(5)

        # Klik tombol Load more langsung (tanpa if)
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "grain-button"))
        )
        print(get_text("load_more_button", bahasa))
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(2)
        load_more_button.click()
        time.sleep(2)

        # Scroll hingga tidak ada perubahan lagi
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

        # Ambil semua tautan media
        print(get_text("fetch_links", bahasa))
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        post_links = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href") and "media" in link.get_attribute("href")
        ]

        return list(set(post_links))

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")
        tb.print_exc()
        return []

    finally:
        driver.quit()



def download_file(url, dest_path):
    """Unduh file dengan progress bar dan headers agar tidak diblokir."""
    req = ur.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with ur.urlopen(req) as response:
        total = int(response.getheader('Content-Length', 0))
        with open(dest_path, 'wb') as out_file, tqdm(
            desc=os.path.basename(dest_path),
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            while True:
                buffer = response.read(1024)
                if not buffer:
                    break
                out_file.write(buffer)
                bar.update(len(buffer))

def download(vsco_media_url, output_path, get_video_thumbnails=True, save=True, current_index=1, total=1):

    try:
        request_header = {"User-Agent": "Mozilla/5.0"}
        request = ur.Request(vsco_media_url, headers=request_header)
        data = ur.urlopen(request).read().decode('utf-8')  # HTML as string

        match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\})\s*</script>', data, re.DOTALL)
        if not match:
            print("[INFO] Parsing JSON gagal, lanjut ke fallback HTML parsing...")
            raise ValueError("JSON not found")

        json_raw = match.group(1)
        json_data = json.loads(json_raw)
    except Exception:
        print("[INFO] Parsing JSON gagal, lanjut ke fallback HTML parsing...")

        try:
            soup = BeautifulSoup(data, "html.parser")
            video_tag = soup.find("video")
            if video_tag and video_tag.has_attr("poster"):
                video_poster = unescape(video_tag["poster"])
                filename = os.path.basename(video_poster.split("?")[0])
                media_path = os.path.join(output_path, filename)
                if os.path.exists(media_path):
                    print(f"[SKIP] {current_index}/{total} Sudah ada: {filename}")
                    return 0
                if save:
                    download_file(video_poster, media_path)
                print(f"[INFO] {current_index}/{total} Mengunduh: {filename}")
                print(f"[SUCCESS] Fallback video poster downloaded: {media_path}")
                return 0

            img_tag = soup.find("img")
            if img_tag and img_tag.has_attr("src") and "vsco" in img_tag["src"]:
                img_url = unescape(img_tag["src"])
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                filename = os.path.basename(img_url.split("?")[0])
                media_path = os.path.join(output_path, filename)
                if os.path.exists(media_path):
                    print(f"[SKIP] Sudah ada: {filename}")
                    return 0
                if save:
                    download_file(img_url, media_path)
                print(f"[INFO] {current_index}/{total} Mengunduh: {filename}")
                print(f"[SUCCESS] Fallback image downloaded: {media_path}")
                return 0

            print("[ERROR] Fallback HTML parsing gagal: Tidak menemukan media!")
            return 1
        except Exception:
            print("[ERROR] Fallback HTML parsing gagal sepenuhnya!")
            tb.print_exc()
            return 1

    try:
        medias = json_data["medias"]["byId"]
        total = len(medias)
        for i, (media_id, media_obj) in enumerate(medias.items(), start=1):
            info = media_obj["media"]
            is_video = info.get("isVideo", False)
            filename = f"{media_id}.{'mp4' if is_video else 'jpg'}"
            media_url = "https://" + (
                info.get("videoUrl") if is_video else info.get("responsiveUrl", "")
            )
            media_url = media_url.encode().decode("unicode-escape")
            media_path = os.path.join(output_path, filename)

            if os.path.exists(media_path):
                print(f"[SKIP] {i}/{total} Sudah ada: {filename}")
                continue

            print(f"[INFO] {current_index}/{total} Mengunduh: {filename}")
            if save:
                start_time = time.time()
                download_file(media_url, media_path)
                elapsed = time.time() - start_time
                print(f"[INFO] Selesai {current_index}/{total} ({elapsed:.2f}s): {filename}")

        return 0

    except Exception:
        print("ERROR: Gagal mengambil data media dari JSON.")
        tb.print_exc()
        return 1

def read_links_from_file(file_path):
    links = []
    try:
        with open(file_path, 'r') as file:
            links = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"[ERROR] File {file_path} tidak ditemukan!")
    return links

def extract_username_from_url(url):
    """Ambil username dari link VSCO."""
    match = re.search(r"vsco\.co/([^/]+)/", url)
    return match.group(1) if match else "unknown"





if __name__ == '__main__':
    print(get_text("start_extraction", bahasa))

    if metode == "login":
        
        email = input(get_text("enter_email", bahasa))
        password = input(get_text("enter_password", bahasa))
        username = input(get_text("enter_username", bahasa))

        profile_url = f"https://vsco.co/{username}"
        output_dir = os.path.join(os.getcwd(), username)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            
            links = extract_vsco_links(profile_url)
            print(get_text("found_links", bahasa, count=len(links)))

            
            links_file_path = os.path.join(output_dir, f"{username}.txt")
            with open(links_file_path, "w") as links_file:
                for link in links:
                    links_file.write(link + "\n")

            
            for link in links:
                download(link, output_dir)
            print(get_text("download_complete", bahasa, folder=output_dir))
        except Exception as e:
            print(get_text("error", bahasa, error=e))

    elif metode == "file":
        links_file_path = os.path.join(os.getcwd(), "links.txt")
        links = read_links_from_file(links_file_path)

        if links:
            print(get_text("found_links", bahasa, count=len(links)))

            first_username = extract_username_from_url(links[0])
            output_dir = os.path.join(os.getcwd(), "downloads", first_username)
            os.makedirs(output_dir, exist_ok=True)

            total_links = len(links)
            for idx, link in enumerate(links, 1):
                download(link, output_dir, current_index=idx, total=total_links)

            print(get_text("download_complete", bahasa, folder=output_dir))
        else:
            print(get_text("error", bahasa, error="Tidak ada tautan yang ditemukan."))

    

    elif metode == "single_link":
        url = input(get_text("enter_media_url", bahasa)) 
        print(f"[INFO] {get_text('start_downloading', bahasa)} {url}...")  

        username = extract_username_from_url(url)
        output_dir = os.path.join(os.getcwd(), "downloads", username)
        os.makedirs(output_dir, exist_ok=True)

        try:
            download(url, output_dir, current_index=1, total=1)
            print(get_text("download_complete", bahasa, folder=output_dir))
        except Exception as e:
            print(get_text("error", bahasa, error="Terjadi kesalahan saat mengunduh media."))


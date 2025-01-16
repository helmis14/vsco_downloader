import os
import subprocess
import platform
import winreg
import requests
import zipfile

def get_platform():
    
    system = platform.system().lower()
    architecture = platform.architecture()[0]  # 32bit atau 64bit
    if system == "windows":
        return "win32" if architecture == "32bit" else "win64"
    elif system == "linux":
        return "linux32" if architecture == "32bit" else "linux64"
    elif system == "darwin":  
        return "mac-arm64" if "arm" in platform.machine().lower() else "mac-x64"
    else:
        return "unknown"

def get_chrome_version():
    
    system = platform.system().lower()
    if system == "windows":
        return get_chrome_version_windows()
    elif system == "linux":
        return get_chrome_version_linux()
    elif system == "darwin":  
        return get_chrome_version_macos()
    else:
        print(f"Unsupported OS: {system}")
        return None

def get_chrome_version_windows():
    try:
        
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(registry_key, "version")
        return version
    except Exception as e:
        print(f"Error on Windows: {e}")
        return None

def get_chrome_version_linux():
    try:
        
        version = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8").strip()
        return version
    except Exception as e:
        print(f"Error on Linux: {e}")
        return None

def get_chrome_version_macos():
    try:
        
        version = subprocess.check_output(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]).decode("utf-8").strip()
        return version
    except Exception as e:
        print(f"Error on MacOS: {e}")
        return None

def get_chromedriver_download_url(chrome_version, platform_type):
    
    print(f"[INFO] Detected Chrome Version: {chrome_version}")
    print(f"[INFO] Platform: {platform_type}")
    
    
    direct_url = "https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.83/win64/chromedriver-win64.zip"
    print(f"[INFO] Using static ChromeDriver URL: {direct_url}")
    return direct_url

def download_chromedriver(driver_url):
    print(f"[INFO] Downloading ChromeDriver from {driver_url}")
    response = requests.get(driver_url, stream=True)
    if response.status_code == 200:
        driver_zip_path = os.path.join(os.getcwd(), "chromedriver.zip")
        with open(driver_zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"[INFO] Download complete. Saved to {driver_zip_path}")
        return driver_zip_path
    else:
        print(f"[ERROR] Failed to download ChromeDriver. Status code: {response.status_code}")
        return None

def extract_zip(zip_path):
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                
                filename = os.path.basename(member)
                if filename:  
                    source = zip_ref.open(member)
                    target = open(os.path.join(os.getcwd(), filename), "wb")
                    with source, target:
                        target.write(source.read())
        print("[INFO] ChromeDriver extracted successfully without folder structure.")
    except Exception as e:
        print(f"[ERROR] Could not extract ChromeDriver: {e}")



chrome_version = get_chrome_version()
platform_type = get_platform()

if chrome_version:
    print(f"chrome/{platform_type} {chrome_version}")
    chromedriver_url = get_chromedriver_download_url(chrome_version, platform_type)
    if chromedriver_url:
        chromedriver_zip = download_chromedriver(chromedriver_url)
        if chromedriver_zip:
            extract_zip(chromedriver_zip)
else:
    print("[ERROR] Google Chrome is not installed or version not found.")

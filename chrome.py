import os
import subprocess
import platform
import winreg
import requests
import zipfile

def get_platform():
    system = platform.system().lower()
    architecture = platform.architecture()[0]
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
        print(f"[ERROR] Windows registry: {e}")
        return None

def get_chrome_version_linux():
    try:
        version = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8").strip()
        return version.replace("Google Chrome", "").strip()
    except Exception as e:
        print(f"[ERROR] Linux: {e}")
        return None

def get_chrome_version_macos():
    try:
        version = subprocess.check_output(
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
        ).decode("utf-8").strip()
        return version.replace("Google Chrome", "").strip()
    except Exception as e:
        print(f"[ERROR] MacOS: {e}")
        return None

def get_chromedriver_download_url(chrome_version, platform_type):
    print(f"[INFO] Detected Chrome Version: {chrome_version}")
    print(f"[INFO] Platform: {platform_type}")

    # Ambil versi mayor dari Chrome, contoh: "122.0.5615.138" -> "122"
    major_version = chrome_version.split(".")[0]
    try:
        url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/{platform_type}/chromedriver-{platform_type}.zip"
        print(f"[INFO] Using download URL: {url}")
        return url
    except Exception as e:
        print(f"[ERROR] Get download URL: {e}")
        return None

def download_chromedriver(driver_url):
    print(f"[INFO] Downloading ChromeDriver from {driver_url}")
    try:
        response = requests.get(driver_url, stream=True)
        response.raise_for_status()
        driver_zip_path = os.path.join(os.getcwd(), "chromedriver.zip")
        with open(driver_zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"[INFO] Download complete: {driver_zip_path}")
        return driver_zip_path
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return None

def extract_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        print("[INFO] Extraction successful.")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")

def main():
    chrome_version = get_chrome_version()
    platform_type = get_platform()

    if chrome_version:
        chromedriver_url = get_chromedriver_download_url(chrome_version, platform_type)
        if chromedriver_url:
            zip_path = download_chromedriver(chromedriver_url)
            if zip_path:
                extract_zip(zip_path)
    else:
        print("[ERROR] Chrome version not detected.")

if __name__ == "__main__":
    main()

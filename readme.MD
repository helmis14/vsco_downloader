# VSCO Downloader  

VSCO Downloader is a Python script that allows you to download media from VSCO profiles using three different methods:  
- **Download by Username** (requires a VSCO account).  
- **Download by Multi-Link** (no VSCO account needed).  
- **Download by Single Link** (no VSCO account needed).  

With VSCO Downloader, you can easily access and save your favorite media from VSCO efficiently.  

---

## 🚀 Key Features  

- **User-Friendly**: Start downloading media with just a few simple steps.  
- **Flexible**: Supports various download methods based on your needs.  
- **No Login Required**: Link-based downloads do not require VSCO credentials.  

---

## 🛠️ Installation  

Follow these steps to set up your project for the first time:  

1. Create a Python virtual environment:  
   ```sh
   py -m venv venv
   ```

2. Activate the virtual environment:
    ```sh
    .\venv\Scripts\Activate
    ```

3. Install the required dependencies:  
   ```sh
   pip install -r requirements.txt
   or
   pip install selenium beautifulsoup4 requests
   ```  
   (Note: You may need to install additional packages depending on your system configuration.)

4. Run the script to check chrome and chromedriver versions:
    ```sh
    py chrome.py
    ```   
    (Note: You may need to install the correct version of chromedriver based on your chrome version)

5. Run the script to download media:
    ```sh
    py vsco.py
    ```   
    (Note: You may need to adjust the script to suit your needs)
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
import winsound  # for sound alert on Windows

# === Configuration ===
URL = "https://rk9.gg/register/PT02mMVCgJGPQcHccDoy"
REFRESH_INTERVAL = 30  # seconds between checks

# === Setup Firefox profile ===
# Option 1: Use your existing Firefox profile with login cookies
PROFILE_PATH = r"C:\Users\Chase Thompson\AppData\Roaming\Mozilla\Firefox\Profiles\hjptfabk.default"  

profile = FirefoxProfile(PROFILE_PATH)

# === Firefox options ===
options = Options()
options.profile = profile
options.headless = False  # set True if you want no GUI
options.add_argument("--start-maximized")

# === Initialize driver ===
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# === Open registration page ===
driver.get(URL)
print("Browser opened. Make sure you are logged in!")

# === Loop to refresh and check ===
while True:
    driver.refresh()
    page_text = driver.page_source.lower()
    
    if "register" in page_text and "closed" not in page_text:
        print("🎉 Registration appears to be open!")
        # Play alert sound
        winsound.Beep(1000, 1000)  # frequency 1000Hz, duration 1 second
        break
    else:
        print(f"Still closed. Refreshing in {REFRESH_INTERVAL} seconds...")
    
    time.sleep(REFRESH_INTERVAL)

# driver.quit()  # uncomment to close browser when done

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
import logging
import re
from colorama import init, Fore, Style
import json
import os

# Initialize Colorama with autoreset to automatically reset colors after each print
init(autoreset=True)

# Reduce logging output from undetected_chromedriver
logging.getLogger("undetected_chromedriver").setLevel(logging.CRITICAL)

# Configure Chrome options with a comprehensive set of stealth arguments
chrome_options = uc.ChromeOptions()

# Disable automation-controlled features
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Disable sandbox and GPU features (may help in some environments)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")

# Attempt to disable the Chrome DevTools Protocol (CDP) runtime (note: Selenium relies on CDP, so complete disablement is not possible)
chrome_options.add_argument("--remote-debugging-port=0")

# Set a natural User-Agent string
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Optionally, run in non-headless mode (headless mode is more easily detected)
chrome_options.headless = False

# Function to save browser data to JSON
def save_browser_data(driver, filename="browser_data.json"):
    data = {
        "cookies": driver.get_cookies(),
        "user_agent": driver.execute_script("return navigator.userAgent;"),
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(Fore.GREEN + f"Browser data saved to {filename}")

# Function to load browser data from JSON
def load_browser_data(driver, filename="browser_data.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Load cookies
        for cookie in data.get("cookies", []):
            driver.add_cookie(cookie)
        
        # Set user agent if needed (already set via chrome_options, but keeping it here for completeness)
        if "user_agent" in data:
            chrome_options.add_argument(f"user-agent={data['user_agent']}")
        
        print(Fore.GREEN + f"Browser data loaded from {filename}")
        return True
    return False

# Launch the browser using undetected_chromedriver
driver = uc.Chrome(options=chrome_options)

# Inject advanced JavaScript to override and remove automation fingerprints
driver.execute_script("""
    (function() {
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        if (window.chrome && window.chrome.runtime) {
            Object.defineProperty(window.chrome, 'runtime', { get: () => undefined });
        }
        for (let key in window) {
            if (key.startsWith('cdc_')) {
                try {
                    delete window[key];
                } catch(e) {}
            }
        }
        Object.defineProperty(window, 'devtools', { get: () => undefined });
        const originalConsoleLog = console.log;
        console.log = function(...args) {
            if (!args.some(arg => typeof arg === 'string' && arg.includes('undetected chromedriver 1337!'))) {
                originalConsoleLog.apply(console, args);
            }
        };
        console.debug = function() {};
        Object.defineProperty(window, 'outerWidth', { get: () => window.innerWidth });
        Object.defineProperty(window, 'outerHeight', { get: () => window.innerHeight });
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter.apply(this, arguments);
        };
        if (navigator.mediaDevices) {
            Object.defineProperty(navigator, 'mediaDevices', { get: () => undefined });
        }
        window.addEventListener('devtoolschange', function(event) {
            event.stopPropagation();
            event.preventDefault();
        }, true);
    })();
""")

# Helper functions for waiting
def wait_for_element(driver, xpath, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def wait_and_click(driver, xpath, timeout=30):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

def wait_until_element_not_visible(driver, xpath, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, xpath))
        )
    except:
        pass

def get_group_xpath(index, version=1):
    if version == 1:
        return f"/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[{index}]"
    elif version == 2:
        return f"/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[{index}]"
    elif version == 3:
        return f"/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[{index}]"
    elif version == 4:
        return f"####"
    else:
        raise ValueError("Invalid version specified. Please use a valid version (1-3).")

def get_version_based_on_xpath(driver):
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]")
        return 1
    except Exception:
        try:
            driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]")
            return 2
        except Exception:
            try:
                driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[3]")
                return 3
            except Exception:
                return None

def extract_group_xpath():
    global all_group_xpaths
    all_group_xpaths = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[{index}]"

def filter_bmp(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

# =======================
# 1. Login Credentials
# =======================
all_group_xpaths = None
username = input(Fore.CYAN + "Enter your account name: " + Style.RESET_ALL)
password = input(Fore.CYAN + "Enter your password: " + Style.RESET_ALL)
start_group = int(input(Fore.CYAN + "From which group number do you want to start (e.g., 1 for the first group): " + Style.RESET_ALL))

# ==============================
# 2. Open Browser and Log in to Facebook
# ==============================
driver.get("https://www.facebook.com/")

# Check if browser data exists and load it
data_loaded = load_browser_data(driver)
time.sleep(5)

try:
    if not data_loaded:
        # Log in: Enter email and password
        email_input = wait_for_element(driver, '//*[@id="email"]')
        email_input.send_keys(username)
        pass_input = wait_for_element(driver, '//*[@id="pass"]')
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        print(Fore.GREEN + "Logged in successfully.")
        time.sleep(5)  # Wait for login to complete
        save_browser_data(driver)  # Save browser data after successful login
    else:
        email_input = wait_for_element(driver, '//*[@id="email"]')
        email_input.send_keys(username)
        pass_input = wait_for_element(driver, '//*[@id="pass"]')
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        print(Fore.GREEN + "Logged in successfully.")
        time.sleep(5)  # Wait for page to load with cookies
        print(Fore.GREEN + "Logged in using saved browser data.")
except Exception as e:
    driver.get("https://www.facebook.com/")  # Reload page to apply cookies


# ============================================================
# 3. Wait for User to Manually Open the Desired Post
# ============================================================
print(Fore.YELLOW + "Please navigate to your profile and open the desired post, then press Enter...")
input()

# ============================================================
# 4. Read the Sharing Message from post.txt
# ============================================================
with open("post.txt", "r", encoding="utf-8") as f:
    post_message = f.read().strip()

# ================================
# XPath Constants as Requested
# ================================
share_button_xpath = (
    "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div[1]"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div/div"
    )
group_button_xpath = (
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[5]/div/div/div/div/div/div[2]/div/div/div[4]/div/div[1]/div/div[1]/div"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[7]/div/div/div/div/div/div[5]/div/div[1]"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[6]/div/div/div/div/div/div[5]/div/div[1]/div/div[1]/div"
    " | "
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[6]/div/div/div/div/div/div[5]/div/div[1]/div/div[1]/div"
    )
scroll_container_xpath = (
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div"
    )
text_area_xpath = """
//div[@contenteditable='true' and (
    @aria-label='إنشاء منشور عام...' or
    @aria-label='اكتب شيئًا...' or
    @aria-label='Create a public post...' or
    @aria-label='Write something...' or
    @aria-label='Créer une publication publique...' or
    @aria-label='Écrire quelque chose...' or
    @aria-label='Crea un post pubblico...' or
    @aria-label='Scrivi qualcosa...' or
    @aria-label='Crea una publicación pública...' or
    @aria-label='Escribe algo...' or
    @aria-label='Criar uma publicação pública...' or
    @aria-label='Escreva algo...' or
    @aria-label='Öffentliche Beitrag erstellen...' or
    @aria-label='Schreibe etwas...' or
    @aria-label='Criar uma publicação pública...' or
    @aria-label='Escreva algo...' or
    @aria-label='Maak een openbaar bericht...' or
    @aria-label='Schrijf iets...' or
    @aria-label='Stwórz publiczny post...' or
    @aria-label='Napisz coś...' or
    @aria-label='Создать публичный пост...' or
    @aria-label='Напишите что-нибудь...' or
    @aria-label='สร้างโพสต์สาธารณะ...' or
    @aria-label='เขียนอะไรบางอย่าง...' or
    @aria-label='Buat postingan publik...' or
    @aria-label='Tulis sesuatu...' or
    @aria-label='建立公开贴文...' or
    @aria-label='写点什么...' or
    @aria-label='创建公开帖子...' or
    @aria-label='Gumawa ng pampublikong post...' or
    @aria-label='Sumulat ng isang bagay...'
)]
"""
publish_button_xpath = (
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div"
    " | "
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[3]/div[3]/div/div"
)
close_button = (
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[1]/div[1]/div[2]/div/div"
    " | "
    "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div"
    " | "
    "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div"
)

# ===============================================
# 5. Open Share Window for Groups and Count Them
# ===============================================
wait_and_click(driver, share_button_xpath)
time.sleep(1)
wait_and_click(driver, group_button_xpath)
time.sleep(2)

# Determine the version based on the available XPath
time.sleep(5)
version = get_version_based_on_xpath(driver)


# Check if the version was successfully determined
if version:
    print(f"Using version {version}")
else:
    print("Unable to determine version.")


# Scroll the group list to the end using the specified container
scroll_container = wait_for_element(driver, scroll_container_xpath)
start_time = time.time()
while time.time() - start_time < 30:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
    time.sleep(2)

group_item_base_xpath = "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div"
groups = driver.find_elements(By.XPATH, group_item_base_xpath)

if len(groups) < 10:
    group_item_base_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div"
    groups = driver.find_elements(By.XPATH, group_item_base_xpath)

group_count = len(groups)
print(Fore.CYAN + f"Number of available groups: {group_count}")

wait_and_click(driver, close_button)
time.sleep(1)

# ======================================================
# 6. Validate the Starting Group Number
# ======================================================
while True:
    try:
        if 1 <= start_group <= group_count:
            break
        else:
            print(Fore.RED + "Please enter a valid group number within the range.")
            start_group = int(input(Fore.CYAN + "Enter a valid group number: " + Style.RESET_ALL))
    except ValueError:
        print(Fore.RED + "Please enter an integer.")
        start_group = int(input(Fore.CYAN + "Enter a valid group number: " + Style.RESET_ALL))

print("\n" + Fore.CYAN + "="*50)
print(Fore.CYAN + "Starting to share the post to groups...")
print(Fore.CYAN + "="*50 + "\n")

# ======================================================
# 7. Share the Post in Each Group Starting from the Specified Group
# ======================================================
for i in range(start_group, group_count + 1):
    print(Fore.CYAN + f"Processing group number {i}...")
    wait_and_click(driver, share_button_xpath)
    time.sleep(1)
    wait_and_click(driver, group_button_xpath)
    time.sleep(2)
    
    text_area = None
    version = get_version_based_on_xpath(driver)
    group_xpath = get_group_xpath(i, version=version)
    try:
        group_element = wait_for_element(driver, group_xpath, timeout=15)
        driver.execute_script("arguments[0].scrollIntoView();", group_element)
        group_name = group_element.text
        print(Fore.GREEN + f"Posting to group: {group_name}")
        time.sleep(2)
        group_element.click()
    except Exception as e:
        print(Fore.RED + f"Group number {i} not found: {e}")
        continue

    time.sleep(5)
    try:
        text_area = wait_for_element(driver, text_area_xpath, timeout=10)
    except Exception as e:
        print(Fore.RED + f"Text area not found: {e}")

    if text_area:
        try:
            text_area.click()
            time.sleep(1)
            text_area.send_keys(Keys.CONTROL, "a")
            text_area.send_keys(Keys.BACKSPACE)
            filtered_text = filter_bmp(post_message)
            try:
                text_area.send_keys(filtered_text)
            except Exception as send_err:
                print(Fore.YELLOW + f"send_keys failed, trying JavaScript: {send_err}")
                js_text = filtered_text.replace("\n", "<br>")
                driver.execute_script("arguments[0].innerHTML = '<p>' + arguments[1] + '</p>';", text_area, js_text)
        except Exception as e:
            print(Fore.RED + f"Error while entering text: {e}")
    else:
        print(Fore.RED + "Text area not found.")

    time.sleep(1)
    try:
        wait_and_click(driver, publish_button_xpath, timeout=15)
        print(Fore.GREEN + f"Post shared successfully in group number {i}.")
    except Exception as e:
        print(Fore.RED + f"Error during publishing: {e}")

    xpath_to_check = (
        "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[1]/div[1]/div[1]"
        " | "
        "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[3]/form/div/div[1]/div/div/div/div[1]/div[1]"
    )
    wait_until_element_not_visible(driver, xpath_to_check)
    time.sleep(3)
    print(Fore.CYAN + "-"*30)

print(Fore.GREEN + "Sharing completed in all specified groups.")
input(Fore.YELLOW + "Press Enter to close the program..." + Style.RESET_ALL)
driver.quit()

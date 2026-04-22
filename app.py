import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
CORS(app)

@app.route('/fetch-heloprint', methods=['POST'])
def fetch_from_heloprint():
    data = request.get_json()
    user_aadhaar = data.get('number') 
    
    if not user_aadhaar:
        return jsonify({"status": "error", "message": "Aadhaar number is required!"})

    driver = None 
    step = "Starting Chrome in Stealth Mode"

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Wapas normal headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        
        # === STEALTH MODE SETTINGS ===
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        # Webdriver flag ko JavaScript se gayab karna
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # === WARM UP BROWSER ===
        step = "Warming up browser (Google.com)"
        driver.get("https://www.google.com")
        time.sleep(2) # Google khol kar 2 second wait

        step = "Opening Login Page Directly"
        driver.get("https://heloprint.xyz/login.php")
        
        time.sleep(5) 
        
        if driver.current_url == "data:,":
            raise Exception("Website ka Firewall Render Server ko block kar raha hai (IP Blocked).")

        step = "Filling Username"
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.clear() 
        username_field.send_keys("7619815009")

        step = "Filling Password"
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("Noor@1997")

        step = "Clicking Sign In button"
        sign_in_btn = driver.find_element(By.CLASS_NAME, "fxt-btn-fill")
        driver.execute_script("arguments[0].click();", sign_in_btn)

        time.sleep(4)

        step = "Waiting for Pan Card Services option"
        pan_services = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu"]/li[10]/a/div[2]')))
        driver.execute_script("arguments[0].click();", pan_services)

        step = "Clicking Pan Number Find option"
        pan_find_option = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/a/div[1]')))
        driver.execute_script("arguments[0].click();", pan_find_option)
        
        time.sleep(3)

        step = "Entering Aadhaar Number"
        aadhaar_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadhaar_no"]')))
        aadhaar_field.clear()
        aadhaar_field.send_keys(user_aadhaar)

        step = "Clicking Verify Now button"
        verify_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div/form/div[2]/button')))
        driver.execute_script("arguments[0].click();", verify_btn)

        step = "Waiting for final result"
        time.sleep(5)

        return jsonify({
            "status": "success", 
            "message": "Process Completed Successfully! Data Fetched."
        })

    except Exception as e:
        curr_url = driver.current_url if driver else "Unknown URL"
        
        return jsonify({
            "status": "error", 
            "message": f"Failed at step: '{step}'.<br><b>Current URL:</b> {curr_url}<br><b>Error:</b> {str(e)}"
        })

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

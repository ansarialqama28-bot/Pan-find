
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
    step = "Starting Chrome" # Yahan se hum step track karenge

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Ye line website ko batayegi ki hum Windows PC se aaye hain (Bot block se bachne ke liye)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)

        step = "Opening heloprint.xyz"
        driver.get("https://heloprint.xyz")

        step = "Waiting for Login button on Nav Menu"
        login_nav_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navMenu"]/a[4]')))
        login_nav_btn.click()

        step = "Filling Username"
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys("7619815009")

        step = "Filling Password"
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("Noor@1997")

        step = "Clicking Sign In button"
        sign_in_btn = driver.find_element(By.CLASS_NAME, "fxt-btn-fill")
        sign_in_btn.click()

        step = "Waiting for Pan Card Services option"
        pan_services = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/li[10]/a/div[2]')))
        pan_services.click()

        step = "Clicking Pan Number Find option"
        pan_find_option = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/a/div[1]')))
        pan_find_option.click()

        step = "Entering Aadhaar Number"
        aadhaar_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadhaar_no"]')))
        aadhaar_field.send_keys(user_aadhaar)

        step = "Clicking Verify Now button"
        verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div/form/div[2]/button')))
        verify_btn.click()

        step = "Waiting for final result"
        time.sleep(5)

        return jsonify({
            "status": "success", 
            "message": "Process Completed Successfully! Data Fetched."
        })

    except Exception as e:
        error_str = str(e).strip()
        # Agar error message khali ho, toh hum khud ka message dalenge
        if not error_str or error_str == "Message:":
            error_str = "Timeout: 20 seconds lag gaye par button nahi mila."
            
        # Ab humein exactly pata chalega ki kis STEP par ruka hai
        return jsonify({"status": "error", "message": f"Failed at step: '{step}'. Error detail: {error_str}"})

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

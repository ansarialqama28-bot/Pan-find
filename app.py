import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

@app.route('/fetch-heloprint', methods=['POST'])
def fetch_from_heloprint():
    data = request.get_json()
    user_aadhaar = data.get('number') 
    
    if not user_aadhaar:
        return jsonify({"status": "error", "message": "Aadhaar number is required!"})

    driver = None # Driver ko pehle khali define kar rahe hain

    try:
        # Chrome settings ko try block ke andar rakha hai
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Ye line Render par install hue Chrome ka rasta batati hai
        chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 20)

        # 1. Website par jana
        driver.get("https://heloprint.xyz")

        # 2. Login button par click karna
        login_nav_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navMenu"]/a[4]')))
        login_nav_btn.click()

        # 3. Login Form bharna
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys("7619815009")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("Noor@1997")

        # 4. Sign In button par click karna
        sign_in_btn = driver.find_element(By.CLASS_NAME, "fxt-btn-fill")
        sign_in_btn.click()

        # 5. Pan Card Services par click karna
        pan_services = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/li[10]/a/div[2]')))
        pan_services.click()

        # 6. Pan Number Find option par click karna
        pan_find_option = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/a/div[1]')))
        pan_find_option.click()

        # 7. Aadhaar number input field me number fill karna
        aadhaar_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadhaar_no"]')))
        aadhaar_field.send_keys(user_aadhaar)

        # 8. Verify Now button par click karna
        verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div/form/div[2]/button')))
        verify_btn.click()

        time.sleep(5)

        return jsonify({
            "status": "success", 
            "message": "Process Completed Successfully!"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Python Error: {str(e)}"})

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

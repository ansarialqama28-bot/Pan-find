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
    # Frontend se aane wala Aadhaar number (placeholder logic)
    user_aadhaar = data.get('number') 
    
    if not user_aadhaar:
        return jsonify({"status": "error", "message": "Aadhaar number is required!"})

    # Render/Linux par chalne ke liye Headless Chrome settings
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Chrome Driver setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20) # 20 second tak wait karega elements ke liye

    try:
        # 1. Website par jana
        driver.get("https://heloprint.xyz")

        # 2. Login button par click karna (Aapka diya hua XPath)
        login_nav_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navMenu"]/a[4]')))
        login_nav_btn.click()

        # 3. Login Form bharna (ID "username" aur "password")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys("7619815009")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("Noor@1997")

        # 4. Sign In button par click karna (Class: fxt-btn-fill)
        sign_in_btn = driver.find_element(By.CLASS_NAME, "fxt-btn-fill")
        sign_in_btn.click()

        # 5. Pan Card Services par click karna (Aapka diya hua XPath)
        pan_services = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/li[10]/a/div[2]')))
        pan_services.click()

        # 6. Pan Number Find option par click karna (Aapka diya hua XPath)
        pan_find_option = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div[1]/a/div[1]')))
        pan_find_option.click()

        # 7. Aadhaar number input field me number fill karna (Aapka diya hua XPath)
        # Note: user_aadhaar me user ka bheja gaya number jayega
        aadhaar_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadhaar_no"]')))
        aadhaar_field.send_keys(user_aadhaar)

        # 8. Verify Now button par click karna (Aapka diya hua XPath)
        verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div/form/div[2]/button')))
        verify_btn.click()

        # 9. Result aane ka thoda wait (Kyunki page process hota hai)
        time.sleep(5)

        # 10. Result ko extract karna
        # Yahan aapko result wale element ka id ya xpath dalna hoga
        # Filhaal hum page ka title ya success message return kar rahe hain
        return jsonify({
            "status": "success", 
            "message": "Process Completed",
            "url_reached": driver.current_url
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        # Browser ko band karna mat bhulein
        driver.quit()

if __name__ == '__main__':
    # Render port assign karne ke liye
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

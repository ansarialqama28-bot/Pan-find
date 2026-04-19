import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Doosri website (aapke frontend) se request allow karne ke liye

@app.route('/fetch-heloprint', methods=['POST'])
def fetch_from_heloprint():
    data = request.get_json()
    user_number = data.get('number')
    
    if not user_number:
        return jsonify({"status": "error", "message": "Number is required!"})

    # Session create karna (taki cookies maintain rahein)
    session = requests.Session()

    # ⚠️ DHYAN DEIN: Yahan aapko heloprint.xyz ka exact POST URL dalna hoga
    # Jab aap unki site par submit button dabate hain, toh data kis URL par jata hai
    target_post_url = "https://heloprint.xyz/submit_action_url" # Isko replace karein

    # ⚠️ DHYAN DEIN: Payload mein input field ka exact 'name' attribute use karein
    payload = {
        "aadhaar_input_name": user_number, # 'aadhaar_input_name' ko real name se badlein
    }

    # Browser jaisa dikhne ke liye User-Agent add karna zaroori hai
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        # heloprint.xyz par data submit karna
        response = session.post(target_post_url, data=payload, headers=headers)
        
        # Agar submission successful raha
        if response.status_code == 200:
            # Us page ka HTML parse karna BeautifulSoup se
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Maan lijiye result kisi specific class ya id mein aata hai
            # Usko yahan find kar sakte hain. Example:
            # result_div = soup.find('div', class_='result-box')
            # final_text = result_div.text if result_div else "No result found"
            
            # Abhi ke liye hum pura HTML text bhej rahe hain
            return jsonify({
                "status": "success", 
                "message": "Data fetched successfully",
                "html_response": response.text[:500] # Sirf shuruwaat ka 500 character bhej rahe hain test karne ke liye
            })
        else:
            return jsonify({"status": "error", "message": f"Target site returned status: {response.status_code}"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

async function fetchPanDetails() {
    const aadhaar = document.getElementById('aadhaarNumber').value;
    const resultDiv = document.getElementById('resultDisplay');
    const loader = document.getElementById('loader');

    if(!aadhaar) {
        alert("Please enter an Aadhaar number.");
        return;
    }

    // Loader dikhana aur purana result chupana
    resultDiv.style.display = 'none';
    loader.style.display = 'block';

    try {
        // Aapka exact Render Backend URL fetch-heloprint endpoint ke sath
        const renderBackendUrl = 'https://pan-find.onrender.com/fetch-heloprint';
        
        const response = await fetch(renderBackendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ number: aadhaar })
        });

        const data = await response.json();
        
        // Loader chupana aur result dikhana
        loader.style.display = 'none';
        resultDiv.style.display = 'block';

        if(data.status === "success") {
            resultDiv.innerHTML = "<strong>Result:</strong><br>" + data.message;
        } else {
            resultDiv.innerHTML = "<span style='color:red;'>Error: " + data.message + "</span>";
        }
    } catch (error) {
        loader.style.display = 'none';
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = "<span style='color:red;'>Server connection failed! Make sure your Render app is running properly.</span>";
    }
}

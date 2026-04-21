// Ye function Frontend JS (Blogger) se call hoga
async function sendDataToPythonApp(aadhaarNumber) {
    try {
        // Aapka Render Backend URL
        const renderBackendUrl = 'https://pan-find.onrender.com/fetch-heloprint';
        
        // Data Python app.py ko bhej rahe hain
        const response = await fetch(renderBackendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ number: aadhaarNumber })
        });

        // Python app.py se jo result mila
        const data = await response.json();
        
        // Ye result wapas Blogger wale Frontend JS ko return kar dega
        return data; 

    } catch (error) {
        // Agar connection fail hua to error return karega
        return { status: "error", message: "Server connection failed! Make sure Render is running." };
    }
}

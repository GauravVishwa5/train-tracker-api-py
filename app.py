from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

@app.route('/api/train/<train_no>')
def track_train(train_no):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Set Chrome binary path if available
        chrome_bin = "/usr/bin/google-chrome"  # fallback, but not required
        if os.path.exists(chrome_bin):
            options.binary_location = chrome_bin

        # Use WebDriver Manager with Chrome
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://enquiry.indianrail.gov.in/mntes/")
        time.sleep(2)

        input_box = driver.find_element(By.ID, "trainNo")
        input_box.send_keys(train_no)

        search_btn = driver.find_element(By.ID, "searchTrain")
        search_btn.click()

        time.sleep(3)

        try:
            table = driver.find_element(By.ID, "trainStatusTable")
            html = table.get_attribute("outerHTML")
            driver.quit()
            return jsonify({"success": True, "html": html})
        except:
            driver.quit()
            return jsonify({"success": False, "error": "Train status table not found or rendered by JS"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

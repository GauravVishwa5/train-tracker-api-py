from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/api/train/<train_no>')
def track_train(train_no):
    try:
        # Configure headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("https://enquiry.indianrail.gov.in/mntes/")

        # Wait for JS to render
        time.sleep(3)  # you can replace with WebDriverWait for better handling

        # Now interact with the page
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
    app.run(host='0.0.0.0', port=5000)

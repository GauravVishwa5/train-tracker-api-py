from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/api/train/<train_no>', methods=['GET'])
def get_train_status(train_no):
    # Set up headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://enquiry.indianrail.gov.in/mntes/')

        # Wait for input to appear and enter train number
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "trainNo"))).send_keys(train_no)

        # Click the Search button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchTrain"))).click()

        # Wait for table to load
        table = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "trainStatusTable")))

        # Extract data
        headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, 'thead th')]
        rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        data = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            entry = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
            data.append(entry)

        return jsonify({"success": True, "data": data})

    except Exception as e:
        print("Scraping error:", e)
        return jsonify({"success": False, "error": "Failed to retrieve train status"})

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
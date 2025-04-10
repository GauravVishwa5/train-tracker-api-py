from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/api/train/<train_no>')
def get_train_status(train_no):
    try:
        url = f"https://enquiry.indianrail.gov.in/mntes/"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        status_table = soup.find('table', {'id': 'trainStatusTable'})
        if not status_table:
            return jsonify({'success': False, 'error': 'Train status table not found or rendered by JavaScript'})

        return jsonify({'success': True, 'html': str(status_table)})

    except Exception as e:
        print('Scraping error:', str(e))
        return jsonify({'success': False, 'error': 'Failed to retrieve train status.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

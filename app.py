from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/train/<train_no>')
def get_train_status(train_no):
    try:
        # This site is just an example - real site may require dynamic scraping
        url = f"https://enquiry.indianrail.gov.in/mntes/"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Example placeholder — you'd need to inspect the actual structure
        status_table = soup.find('table', {'id': 'trainStatusTable'})
        if not status_table:
            return jsonify({'success': False, 'error': 'Train status table not found or rendered by JavaScript'})

        return jsonify({'success': True, 'html': str(status_table)})

    except Exception as e:
        print('Scraping error:', str(e))
        return jsonify({'success': False, 'error': 'Failed to retrieve train status.'})

if __name__ == '__main__':
    app.run(debug=True)

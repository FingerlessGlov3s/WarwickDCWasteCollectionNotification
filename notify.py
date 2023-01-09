import requests
import re
import datetime
import os
from bs4 import BeautifulSoup

"""
Find your UPRN: https://estates7.warwickdc.gov.uk/PropertyPortal/Property/Search
Telgram Bot Docs: https://core.telegram.org/bots
"""

# User Vars
uprn = os.getenv("UPRN", "")
token = os.getenv("TOKEN", "")
chat_id = os.getenv("CHAT_ID", "")
notify_days = os.getenv("NOTIFY_DAYS", 1)

# Sends markdown formatted message
def send_telegram_message(message):
    message_url = f'https://api.telegram.org/bot{token}/sendMessage'
    response = requests.post(message_url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'markdown'})
    if response.status_code != 200:
        print(response.text)
        raise Exception(f'Received non 200 HTTP code for URL: {message_url}')

# Dictonary array of waste collections and their up coming collection days
def get_collection_dates():
    url = f'https://estates7.warwickdc.gov.uk/PropertyPortal/Property/Recycling/{uprn}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Received non 200 HTTP code for URL: {url}')
    if response.text.__contains__('Waste Collection') == False:
        raise Exception(f'Failed to find `Waste Collection`: {url}')

    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='col-xs-12 text-center waste-dates margin-bottom-15')
    data = {}
    for div in divs:
        heading_items = [ele.replace('\r\n', '') for ele in div.find('strong').text.split(' ') if ele != '']
        for item in ('', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            if item in heading_items:
                heading_items.remove(item)
        heading = ' '.join(heading_items)
        date_elements = div.find_all('p')
        dates = [tag.text for tag in date_elements if re.match(r'^\d{2}\/\d{2}\/\d{4}$', tag.text)]
        data[heading] = dates
    return data

def main():
    # Get tomorrow's date, so we have a date to look for
    notify_date = (datetime.datetime.now() + datetime.timedelta(days=notify_days)).strftime('%d/%m/%Y')

    # The heading of our message in bold
    message = f'*Waste Collection ({notify_date})*'
    collections = 0

    # Get our collection dates and look for any collection that are tomorrows date
    data = get_collection_dates()

    for bin, value in data.items():
        for date in value:
            if date == notify_date:
                collections += 1
                message += "\n - " + bin

    # Find collections found send telegram message
    if collections > 0:
        send_telegram_message(message)

if __name__ == "__main__":
    main()

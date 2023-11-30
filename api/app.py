from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def format_category(li_element):
    text = li_element.get_text(separator=' ^ ', strip=True)  # Remove extra spaces
    parts = text.split('^')  # Split text by '|'
    formatted_parts = []
    current_line = ""
    category_list = []  

    for part in parts:
        if part.strip().isdigit() and current_line:
            # If the part is a number and we have content in the current_line, add a newline
            current_line += '\n' + part.strip()
        else:
            if current_line:
                formatted_parts.append(current_line)
            current_line = part.strip()

            separated_current_line = current_line.split('|')

            if len(separated_current_line) > 1:
                category_id = separated_current_line[1].split(':')
                category_name=separated_current_line[0]
                if len(category_id) > 1:
                    category = {
                    'category_name': category_name,
                    'ID': category_id[1]
                    }
                    category_list.append(category)
                else:
                 print('Unexpected format: ' + current_line)
            else:
                 print('Unexpected format: ' + current_line)
            # print(category_list)
    if current_line:
        formatted_parts.append(current_line)
    
    # return '  '.join(formatted_parts)
    return category_list


@app.route('/get-ebay-categories')
def category():
    try:
        # Get the URL from the request's JSON data
        # data = request.json
        url = 'https://pages.ebay.com/sellerinformation/news/categorychanges/preview2023.html'
        # url = 'https://pages.ebay.com/sellerinformation/news/categorychanges/preview2023_09.html' #NEW CATEGORIES

        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data from the HTML using BeautifulSoup
        # For example, find all <a> tags with a specific class
        data = []
        ul = soup.find('ul', class_='categoryListContainer')
        if ul:
            li_elements = ul.find_all('li', recursive=False)
            for li in li_elements:
                formatted_text = format_category(li)
                # print(formatted_text)
                data+=formatted_text

        # Return the extracted data as JSON
        return jsonify({'ebay_categories': data})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

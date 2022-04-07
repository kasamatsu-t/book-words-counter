import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def scraping(isbn):
    url = "http://www.seg.co.jp/sss_review/jsp/frm_a_110.jsp"
    payload = {
        "kb_sort": 0,
        "cd_sc": "a_110",
        "dt_before": "frm_a_110",
        "fg_detail": 0,
        "dt_page": 10,
        "fg_arasuji": 1,
        "dt_sort": 3,
        "fg_isbn_search": 1,
        "dt_isbn_search_110": isbn,
        "nm_page": 1,
        "dt_isbn_search_110_2": isbn,
        "dt_sort_in": 3,
        "dt_page_in": 10,
        "dt_isbn_search": isbn
    }

    r = requests.post(url, payload)

    soup = BeautifulSoup(r.content, "html.parser")
    book_info = soup.select('td.subj')
    data = str(book_info[0]).split()
    categoty = str(book_info[1]).split('●')
    YL = ''
    words = ''
    series = ''
    for item in data:
        if 'YL' in item:
            YL = item.split('：')[1]
        if '総語数' in item:
            words = item.split('：')[1]
            break
    for item in categoty:
        if 'シリーズ' in item:
            series = item.split('：')[1].replace('\n', '').replace(' ', '')

    em = soup.select_one('em')
    name = em.select_one('b').string

    book_data = {
        'name': name,
        'YL': YL,
        'words': words,
        'series': series,
        'ISBN': isbn
    }

    book_data_json = json.dumps(book_data)
    return book_data_json


@app.route('/')
def get_foreign_books_data():
    try:
        args = request.args
        isbn = args.get("isbn")

        data = scraping(isbn)
        return jsonify(data)
    except Exception as e:
        abort(e.code)


if __name__ == '__main__':
    app.run()

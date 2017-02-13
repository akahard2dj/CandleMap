from flask import Flask, abort, request
from profanity import profanity
import json
from SQLiteDB.candle_location_db import CandleLocation
from SQLiteDB.candle_board_db import CandleBoard
from SQLiteDB.candle_count_db import CandleCount
from SQLiteDB.api_key_db import APIKey
from util.verification import VerificationText

app = Flask(__name__)

candle_location_db = CandleLocation()
candle_board_db = CandleBoard()
candle_count_db = CandleCount()
api_key_db = APIKey()
verify_text = VerificationText()

f = open('banned_word_list.txt', 'r', encoding='utf-8')
banned_words = f.readlines()
for idx in range(len(banned_words)):
    banned_words[idx] = banned_words[idx].rstrip('\n')
profanity.load_words(banned_words)
profanity.set_censor_characters('-')


@app.route('/')
def main_page():
    return 'test'


@app.route('/api/v2/candle_count', methods=['GET', 'POST'])
def candle_count_api():
    # api key comparing
    api_key = request.args.get("apikey")
    api_key_db.connect()
    is_available = api_key_db.is_issued_key(api_key)
    res_dict = dict()
    if is_available == True:
        if request.method == 'GET':
            status = candle_count_db.connect()
            if status['connection_status'] == 'failed':
                res_dict['result'] = 'fail'
                res_dict['result_detail'] = 'sqlite3 connection error'

                return res_dict

            count = candle_count_db.get_candle_count()
            if not count:
                count = 0
            # res_dict['result'] = 'ok'
            # res_dict['type'] = 'CandleCount'
            res_dict['count'] = count

        if request.method == 'POST':
            status = candle_count_db.connect()
            if status['connection_status'] == 'failed':
                # res_dict['result'] = 'fail'
                # res_dict['result_detail'] = 'sqlite3 connection error'

                return res_dict

            json_data = request.get_json()
            candle_count_db.db_update(json_data)
            count = candle_count_db.get_candle_count()
            # res_dict['result'] = 'ok'
            # res_dict['type'] = 'CandleCount'

            res_dict['count'] = count
    else:
        res_dict['count'] = []

    return json.dumps(res_dict)


@app.route('/api/v2/candle_board', methods=['GET', 'POST', 'DELETE'])
def candle_board_api():
    method_flag = {'POST': 1, 'DELETE': 2, 'GET': 3}

    # api key comparing
    api_key = request.args.get("apikey")
    api_key_db.connect()
    is_available = api_key_db.is_issued_key(api_key)
    res_dict = dict()
    if is_available == True:
        if request.method == 'POST':
            # todo 금칙어 update
            status = candle_board_db.connect()
            if status['connection_status'] == 'failed':
                res_dict['result_msg'] = 'failed'
                res_dict['result_detail'] = 'sqlite3 connection error'

                return res_dict

            json_data = request.get_json()
            text = json_data['content']
            text_verify_html = verify_text.html_remove(text)
            # if text == text_verify_html:
            # res_dict['text_verify'] = {'html': 'not_removed'}
            # else:
            # res_dict['text_verify'] = {'html': 'removed'}

            db_to_json = {'content': text_verify_html}
            candle_board_db.db_update(method_flag['POST'], db_to_json)
            offset = request.args.get("offset")
            limit = request.args.get("limit")

            board_contents = candle_board_db.fetch_posted_step(offset, limit)
            # res_dict['result_msg'] = 'success'
            # res_dict['result_detail'] = 'POST connection'

            res_dict['data'] = board_contents

        elif request.method == 'GET':
            status = candle_board_db.connect()
            if status['connection_status'] == 'failed':
                res_dict['result_msg'] = 'failed'
                res_dict['result_detail'] = 'sqlite3 connection error'

                return res_dict

            offset = request.args.get("offset")
            limit = request.args.get("limit")

            board_contents = candle_board_db.fetch_posted_step(offset, limit)
            # res_dict['result_msg'] = 'success'
            # res_dict['result_detail'] = 'GET connection'
            res_dict['data'] = board_contents

        elif request.method == 'DELETE':
            status = candle_board_db.connect()
            if status['connection_status'] == 'failed':
                res_dict['result_msg'] = 'failed'
                res_dict['result_detail'] = 'sqlite3 connection error'

            json_data = request.get_json()
            offset = request.args.get("offset")
            limit = request.args.get("limit")
            candle_board_db.db_update(method_flag['DELETE'], json_data)
            board_contents = candle_board_db.fetch_posted_step(offset, limit)
            # res_dict['result_msg'] = 'success'
            # res_dict['result_detail'] = 'DELETE connection'
            res_dict['data'] = board_contents
        else:
            res_dict['result_msg'] = 'success'
            res_dict['result_detail'] = 'invalid connection'

    else:
        res_dict['data'] = []

    return json.dumps(res_dict, ensure_ascii=False)


@app.route('/api/v1/candle_count/', methods=['GET', 'POST'])
def candle_count():
    res_dict = {}
    if request.method == 'GET':
        status = candle_count_db.connect()
        if status['connection_status'] == 'failed':
            res_dict['result'] = 'fail'
            res_dict['result_detail'] = 'sqlite3 connection error'

            return res_dict

        count = candle_count_db.get_candle_count()
        if not count:
            count = 0
        #res_dict['result'] = 'ok'
        #res_dict['type'] = 'CandleCount'
        res_dict['count'] = count

    if request.method == 'POST':
        status = candle_count_db.connect()
        if status['connection_status'] == 'failed':
            #res_dict['result'] = 'fail'
            #res_dict['result_detail'] = 'sqlite3 connection error'

            return res_dict

        json_data = request.get_json()
        candle_count_db.db_update(json_data)
        count = candle_count_db.get_candle_count()
        #res_dict['result'] = 'ok'
        #res_dict['type'] = 'CandleCount'

        res_dict['count'] = count

    return json.dumps(res_dict)



@app.route('/api/v1/candle_location/', methods=['POST'])
def candle_location():
    res_dict = {}
    if request.method == 'POST':
        if not request.get_json():
            res_dict["result_msg"] = "fail"
            return json.dumps(res_dict)

        json_data = request.get_json()
        candle_location_db.connect()
        candle_location_db.db_update(json_data)

        # result -> candle_flag
        flag = candle_location_db.get_candle_flag(json_data)
        res_dict["result_msg"] = "success"
        res_dict["candle_flag"] = flag
    else:
        res_dict["result_msg"] = "success"
        res_dict["result_detail"] = "invalid access"

    return json.dumps(res_dict)


@app.route('/api/v1/candle_board', methods=['GET', 'POST', 'DELETE'])
def candle_board():
    res_dict = dict()
    method_flag = {'POST': 1, 'DELETE': 2, 'GET': 3}

    if request.method == 'POST':
        #todo 금칙어 update
        status = candle_board_db.connect()
        if status['connection_status'] == 'failed':
            res_dict['result_msg'] = 'failed'
            res_dict['result_detail'] = 'sqlite3 connection error'

            return res_dict

        json_data = request.get_json()
        text = json_data['content']
        text_verify_html = verify_text.html_remove(text)
        #if text == text_verify_html:
            #res_dict['text_verify'] = {'html': 'not_removed'}
        #else:
            #res_dict['text_verify'] = {'html': 'removed'}

        profanity_check = profanity.censor(text_verify_html)

        db_to_json = {'content': profanity_check}
        candle_board_db.db_update(method_flag['POST'], db_to_json)
        offset = request.args.get("offset")
        limit = request.args.get("limit")

        board_contents = candle_board_db.fetch_posted_step(offset, limit)
        #res_dict['result_msg'] = 'success'
        #res_dict['result_detail'] = 'POST connection'

        res_dict['data'] = board_contents

    elif request.method == 'GET':
        status = candle_board_db.connect()
        if status['connection_status'] == 'failed':
            res_dict['result_msg'] = 'failed'
            res_dict['result_detail'] = 'sqlite3 connection error'

            return res_dict

        offset = request.args.get("offset")
        limit = request.args.get("limit")

        board_contents = candle_board_db.fetch_posted_step(offset, limit)
        #res_dict['result_msg'] = 'success'
        #res_dict['result_detail'] = 'GET connection'
        res_dict['data'] = board_contents

    elif request.method == 'DELETE':
        status = candle_board_db.connect()
        if status['connection_status'] == 'failed':
            res_dict['result_msg'] = 'failed'
            res_dict['result_detail'] = 'sqlite3 connection error'

        json_data = request.get_json()
        offset = request.args.get("offset")
        limit = request.args.get("limit")
        candle_board_db.db_update(method_flag['DELETE'], json_data)
        board_contents = candle_board_db.fetch_posted_step(offset, limit)
        #res_dict['result_msg'] = 'success'
        #res_dict['result_detail'] = 'DELETE connection'
        res_dict['data'] = board_contents
    else:
        res_dict['result_msg'] = 'success'
        res_dict['result_detail'] = 'invalid connection'

    return json.dumps(res_dict, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(debug=True)

# CandleMap

api 명세서
게시판

http://ip:5000/api/v1/candle_board/

통신 방법 ['GET', 'POST', 'DELETE']

'GET'

<Request>
URL = http://ip:5000/api/v1/candle_board?offset=0&limit=2

 - offset : 쿼리 offset
 - limit : 쿼리 요청 갯수
 - Get통신 할때 기기자체에서 offset값을 Count해야 함(ex. 요청할때 마다 offset 증가)

<Response>
{"result_msg": "success", 
 "result_detail": "GET connection", 
 "data": [query result(UTF-8 encoded)], }
 
 result_msg 
  - success : 성공
  - failed : 실패 (result_detail에 상세 명기)
  - data : 쿼리 결과(list, utf-8 encoded)
  
  
  
'POST'

<Request>
URL = http://ip:5000/api/v1/candle_board?offset=0&limit=2

 - offset : 쿼리 offset
 - limit : 쿼리 요청 갯수
 - POST통신 할때 기기자체에서 offset/limit 을 결정해야함 글 등록후 업데이트 된 쿼리

Content-Type: application/json
{"content":"Message"}


<Response>
{"result_msg": "success", 
 "result_detail": "POST connection", 
 "text_verify": {"html": "not_removed"},
 "data": [query result(UTF-8 encoded)], }
 
 result_msg 
  - success : 성공
  - failed : 실패 (result_detail에 상세 명기)
  - text_verify : 현재 html 태그 정보만 검출 --> 검출 되었으면 removed, 검출 되지 않았으면 not_removed
  - data : 쿼리 결과(list, utf-8 encoded)
  
  
'DELETE'

<Request>
URL = http://ip:5000/api/v1/candle_board?offset=0&limit=2

 - offset : 쿼리 offset
 - limit : 쿼리 요청 갯수
 - DELETE 통신 할때 기기자체에서 offset/limit 을 결정해야함 글 등록후 업데이트 된 쿼리

Content-Type: application/json
{"rowid": 1}

<Response>
{"result_msg": "success", 
 "result_detail": "DELETE connection", 
 "data": [query result(UTF-8 encoded)], }
 
 result_msg 
  - success : 성공
  - failed : 실패 (result_detail에 상세 명기)
  - data : 쿼리 결과(list, utf-8 encoded)





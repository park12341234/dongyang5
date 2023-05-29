import openai
from flask import Flask, render_template, request, jsonify
# render_template : html 랜더링 시 사용되는 메서드

# 텍스트 출력 함수 생성
def generate_text(prompt):
    response = openai.Completion.create(
        engine='curie:ft-personal:schedule-6-2023-05-14-10-52-28',
        prompt=prompt,
        max_tokens=300,
        temperature=0,
        top_p=1,
        n=1,
        stop = ['**']
    )
    return response.choices[0].text

# Flask 웹서버 생성
app = Flask(__name__)

holiday = {'어린이':'1학기','31절':'1학기','3ㆍ1절':'1학기','석가탄신일':'1학기','현충':'1학기','광복':'2학기',
            '추석':'2학기','개천':'2학기','한글날':'2학기','성탄':'2학기','크리스마스':'2학기', '근로자의 날':'1학기', 
            '노들축제':'1학기','개교기념일':'1학기'}
pre = []


# html 파일을 열 때 경로 지정
@app.route('/') # 127.0.0.1 / 하고 뒤에 hello 가 출력
def open():
    return render_template("index.html")

@app.route('/process-data', methods=['POST'])
def post():
    if request.method == 'POST':
        global holiday
        data = request.json
        val = data['message']
        c = 0
        for h, s in enumerate(holiday):
            if s in val:
                query = 'Sch : 동양미래대\nSme : ' + holiday[s] + '\n\nQuestion : ' + val + '\n ->'
                break
            c += 1
        if (c == len(holiday)) & ('학기' not in val):
            pre.append(val)
            answer = '몇 학기 인가요?'
            return jsonify({'result': answer})
        else:
            if len(pre) > 0:
                query = 'Sch : 동양미래대\nSme : ' + val[val.find('학기')-1:val.find('학기')+2] + '\n\nQuestion : ' + pre[-1] + '\n ->'
                pre.clear()
            else:
                query = 'Sch : 동양미래대\nSme : ' + val[val.find('학기')-1:val.find('학기')+2] + ' \n\nQuestion : ' + val + '\n ->'

        answer = generate_text(query)
        return jsonify({'result': answer})

def main():
    # 발급받은 API 키 설정
    OPENAI_API_KEY = "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"

    # open API 키 인증
    openai.api_key = OPENAI_API_KEY

    app.run()
    # host='0.0.0.0' 이면 외부에서도 연결할 수 있도록 한다는 의미
    # debug=True 면 오류 시 알림
    # port=80 은 보안에 취약함으로 잘 사용하지 않음

if __name__ == '__main__':
    main()
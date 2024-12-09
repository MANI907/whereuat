import os
from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory

client = OpenAI()


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 1️⃣ 기본 경로('/')에 대해 frontend 폴더의 index.html을 반환
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')  # frontend 폴더의 index.html 반환


# 2️⃣ 이미지 설명 생성 API
@app.route('/generate', methods=['POST'])
def generate_description():
    try:
        # 1️⃣ 업로드된 이미지 파일 확인
        if 'image' not in request.files:
            return jsonify({'error': '이미지가 요청에 포함되어 있지 않습니다.'}), 400

        # 2️⃣ 이미지 파일 저장
        image = request.files['image']
        filename = image.filename
        if '..' in filename or '/' in filename:
            return jsonify({'error': '잘못된 파일 이름입니다.'}), 400  # 경로 탐색 공격 방지
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        print(f"이미지 저장 경로: {image_path}")

        # OpenAI API 요청
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )

        print(completion.choices[0].message.content)


        if response.get('choices'):
            description = response.choices[0]['text']
            return jsonify({'description': description})
        else:
            return jsonify({'error': '응답에서 설명을 찾을 수 없습니다.'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'에러 발생: {str(e)}'}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=8080)

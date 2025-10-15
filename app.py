from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import base64
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

client = genai.Client(api_key=GOOGLE_API_KEY)

# Telegram API URL
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Inline keyboard（按鈕）
keyboard = {
    "inline_keyboard": [
        [{"text": "View Details", "url": "https://m4hir0.github.io/ICITY2025/"}]
    ]
}

# 發送照片的函式
def send_photo(filepath, description):
    url = f"{BASE_URL}/sendPhoto"
    with open(filepath, "rb") as photo:
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": "🔥 Possible wildfire detected. Description: " + description,
            "reply_markup": json.dumps(keyboard)  # 要轉成 JSON 字串
        }
        files = {"photo": photo}
        response = requests.post(url, data=data, files=files)
    print("✅ Response:", response.json())


def analyze(filepath):
  with open(filepath, 'rb') as f:
      image_bytes = f.read()

  response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      'Please analyze the content of this image and determine its processing status (depending on whether the photo shows wildfire that requires attention; if it is not wildfire, set the status to "done"). The status must be one of three values: todo, doing, or done. Please output strictly in the following JSON format without extra words: {"ai_result":"Provide the analysis result in English with a few sentences, wrapped in quotes.", "status":"One of the strings todo, doing, or done, wrapped in quotes."}'
    ]
  )
  print("Raw Content (for debug): ", response.text)
  result = json.loads(response.text)

  return result['ai_result'], result['status']

def upload_to_imgbb(img_file):
    # Upload Image to imgBB
    image_data = open(img_file, "rb").read()
    filename = img_file.split("/")[-1]

    # Convert image to base64 format
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    # Call imgBB API to upload image
    upload_url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": encoded_image,
        "name": filename
    }
    res = requests.post(upload_url, data=payload)

    # Show result
    if res.status_code == 200:
        result = res.json()
        img_url = result["data"]["url"]
        print("✅ Image Upload Succeeded! Image URL is at: ", img_url)
        return img_url
    else:
        print("❌ Upload failed - Error Message as follows: ")
        return res.text

def get_exif_data(image):
    exif_data = {}
    try:
        info = image._getexif()
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                exif_data[tag_name] = value
    except:
        pass
    return exif_data

def get_gps_info(gps_info_raw):
    gps_info = {}
    for key in gps_info_raw:
        name = GPSTAGS.get(key, key)
        gps_info[name] = gps_info_raw[key]
    return gps_info

def convert_gps_info(gps_info_raw):
    def convert_value(v):
        # Convert IFDRational to float
        if isinstance(v, (tuple, list)):
            return [float(x) for x in v]
        try:
            return float(v)
        except Exception:
            return str(v)

    gps_info = {}
    for key, val in gps_info_raw.items():
        gps_info[str(key)] = convert_value(val)
    return gps_info

def extract_image_metadata(img_file):
    image = Image.open(img_file)

    # Parsing EXIF
    exif = get_exif_data(image)
    timestamp = exif.get("DateTime", "No Timestamp")
    has_gps = "GPSInfo" in exif
    gps_raw = exif.get("GPSInfo")
    gps_info = get_gps_info(gps_raw) if gps_raw else "No GPS Info"

    result = f"📅 Capture Time: {timestamp}\n📍 GPS Info: \n{gps_info}"
    return result

# -------------------------------
# 🔧 Initialize Firebase（This only run once）
def init_firebase():
    global db
    
    # 從環境變數建立 Firebase 認證
    firebase_config = {
        "type": os.getenv('FIREBASE_TYPE'),
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
        "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
        "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
        "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
    }
    
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

# 📝 Write data to Firestore
def save_to_firestore(image_url, description, ai_result, status, filename, has_gps, gps_info_raw):

    if has_gps:
      gps_info = convert_gps_info(gps_info_raw)

    doc_ref = db.collection("photos").add({
        "image_url": image_url,
        "description": description,
        "ai_result": ai_result,
        "filename": filename,
        "has_gps": has_gps,
        "exif": gps_info,
        "status": status,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "updateTime": firestore.SERVER_TIMESTAMP
    })
    print("✅ Succeeded! Document ID:", doc_ref[1].id)

def analyze_and_upload(img_file, description):
    image = Image.open(img_file)

    # Parsing EXIF
    exif = get_exif_data(image)
    timestamp = exif.get("DateTime", "No Timestamp")
    has_gps = "GPSInfo" in exif
    gps_raw = exif.get("GPSInfo")
    gps_info = get_gps_info(gps_raw) if gps_raw else "No GPS Info"

    # Upload to Imgbb
    imgbb_url = upload_to_imgbb(img_file)

    ## Get AI analysis result
    ai_result, status = analyze(img_file)

    print(f"AI Analysis Result: {ai_result}")
    print(f"Status: {status}")

    if has_gps:
      save_to_firestore(imgbb_url, description, ai_result, status, img_file, has_gps, gps_info)
      send_photo(img_file, description)

    result = f"📅 Capture Time: {timestamp}\n📍 GPS Info: \n{gps_info}\n🖼️ Imgbb URL: {imgbb_url}\nAI Analysis Result: {ai_result}\nStatus: {status}"
    return image, result

app = Flask(__name__)

# 設定上傳路徑與允許副檔名
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 建立資料夾（若不存在）
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return "沒有上傳檔案"

    file = request.files['photo']
    description = request.form.get('description', '')

    if file.filename == '':
        return "未選擇檔案"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image, result = analyze_and_upload(filepath, description)

        return render_template('result.html', filename=filename, description=description)
    else:
        return "不支援的檔案格式"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

init_firebase()

# if __name__ == '__main__':
#     init_firebase()
#     app.run(debug=True)


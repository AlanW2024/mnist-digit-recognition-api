# ======================================================================
# 進化版 AI 伺服器 (lesson9_api_v2.py)
# 新增功能：使用 OpenCV 進行專業的圖片預處理
#
# 注意：你需要先安裝 Flask, TensorFlow, Pillow 和 opencv-python-headless
# pip install Flask tensorflow Pillow opencv-python-headless
# ======================================================================

from flask import Flask, request, jsonify
import numpy as np
from tensorflow import keras
from PIL import Image
import io
import cv2 # 導入 OpenCV

# --- 初始化與讀取模型 (與之前相同) ---
app = Flask(__name__)
try:
    model = keras.models.load_model('my_first_mnist_model.h5')
    print(" * 模型讀取成功，伺服器準備就緒！")
except Exception as e:
    print(f" * 讀取模型失敗: {e}")
    model = None

def preprocess_image(image_stream):
    """
    專業的圖片預處理函式
    1. 讀取圖片並轉為灰階
    2. 反轉顏色 (黑底白字)
    3. 裁切掉多餘的白邊
    4. 將數字置中放入 28x28 的畫布
    """
    # 將資料流轉為 NumPy 陣列
    nparr = np.frombuffer(image_stream.read(), np.uint8)
    # 從陣列解碼成圖片
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    # 2. 反轉顏色：變成白字黑底，並進行二值化
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    
    # 3. 找出數字的邊界並裁切
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("在圖片中找不到數字輪廓")
        
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped = img[y:y+h, x:x+w]
    
    # 4. 將數字置中放入 28x28 畫布
    # 為了維持比例，我們先把裁切後的圖片放到一個更大的正方形中
    side = max(w, h)
    padded = np.zeros((side, side), dtype=np.uint8)
    pad_x = (side - w) // 2
    pad_y = (side - h) // 2
    padded[pad_y:pad_y+h, pad_x:pad_x+w] = cropped
    
    # 將正方形圖片縮小到 20x20，周圍留白
    resized = cv2.resize(padded, (20, 20))
    
    # 建立一個 28x28 的黑色畫布，並把 20x20 的數字放中間
    canvas = np.zeros((28, 28), dtype=np.uint8)
    canvas[4:24, 4:24] = resized
    
    return canvas

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': '模型尚未準備好'}), 500
    if 'file' not in request.files:
        return jsonify({'error': '請求中找不到檔案'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '沒有選擇檔案'}), 400

    try:
        # --- 5. 使用新的預處理函式 ---
        processed_image = preprocess_image(file.stream)
        
        # 標準化並準備預測
        image_array = processed_image / 255.0
        image_to_predict = np.expand_dims(image_array, 0)

        # --- 6. 進行預測 (與之前相同) ---
        predictions = model.predict(image_to_predict)
        predicted_label = int(np.argmax(predictions))
        confidence = float(np.max(predictions))

        # --- 7. 回傳結果 (與之前相同) ---
        return jsonify({
            'predicted_digit': predicted_label,
            'confidence': f"{confidence:.2%}"
        })

    except Exception as e:
        return jsonify({'error': f'處理圖片時發生錯誤: {e}'}), 500

# --- 啟動伺服器 (與之前相同) ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

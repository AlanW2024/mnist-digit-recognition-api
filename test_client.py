# ======================================================================
# API 測試客戶端 (test_client.py)
# 目的：扮演顧客的角色，發送一張圖片給我們的 AI 伺服器，並接收預測結果。
#
# 注意：你需要先安裝 requests 函式庫:
# pip install requests
# ======================================================================

import requests  # requests 是 Python 中用來發送網路請求最方便的函式庫。
import os

# --- 1. 設定目標 ---
# 我們的 AI 伺服器正在這個網址等待我們
API_URL = "http://127.0.0.1:5000/predict"

# 我們要測試的圖片檔案名稱
# 請確保這個檔案和你的 test_client.py 在同一個資料夾下
IMAGE_PATH = "my_digit.png" # <--- 在這裡更改你要測試的圖片檔案名稱

# --- 2. 檢查圖片是否存在 ---
if not os.path.exists(IMAGE_PATH):
    print(f"錯誤：找不到圖片檔案 '{IMAGE_PATH}'。")
    print("請先用小畫家等工具，畫一個數字並存成 my_digit.png，然後再試一次。")
else:
    # --- 3. 準備「點餐」(發送請求) ---
    print(f"正在讀取圖片 '{IMAGE_PATH}' 並發送到進化版伺服器...")
    
    # 'rb' 代表以「二進位讀取 (read binary)」模式打開圖片檔案
    with open(IMAGE_PATH, 'rb') as f:
        # 準備要上傳的檔案，'file' 這個鍵必須和我們 Flask 伺服器中 request.files['file'] 的名稱一致
        files = {'file': f}
        
        try:
            # 使用 requests.post() 發送一個 POST 請求
            response = requests.post(API_URL, files=files)
            
            # --- 4. 接收並印出「餐點」(伺服器回應) ---
            if response.status_code == 200:
                # 如果成功，印出伺服器回傳的 JSON 結果
                print("\n--- 伺服器回應 ---")
                print(response.json())
            else:
                # 如果失敗，印出錯誤狀態碼和內容
                print(f"\n錯誤！伺服器回應狀態碼: {response.status_code}")
                print(f"錯誤訊息: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n錯誤：無法連接到伺服器。")
            print("請確認你的 Flask 伺服器 (lesson9_api_v2.py) 正在另一個終端機視窗中運行。")

# 手寫數字辨識 API (MNIST Digit Recognition API)

這是一個從零到一，完整實現的深度學習專案。此專案的目標是訓練一個神經網絡模型來辨識 MNIST 手寫數字數據集，並將其部署為一個可以透過網路請求進行即時預測的線上 API 服務。

## 專案亮點

- **端到端實現：** 涵蓋了從數據探索、預處理、模型訓練、評估、到最終使用 Flask 部署為線上 API 的完整 AI 專案流程。
- **真實世界挑戰：** 專案不僅在標準測試集上取得了高準確率，更深入探討並解決了「真實世界手寫圖片」與「標準化訓練數據」之間的差異問題。
- **專業預處理：** 最終版本的 API 整合了 OpenCV，能夠對用戶上傳的、不完美的圖片進行自動化的預處理（如顏色反轉、裁切、置中），大幅提升了模型的泛化能力和實用性。

## 技術棧 (Tech Stack)

- **程式語言：** Python 3
- **深度學習框架：** TensorFlow / Keras
- **API 框架：** Flask
- **數據處理/數值運算：** Pandas, NumPy
- **圖像處理：** OpenCV, Pillow

## 專案結構

```
/mnist-api
|-- my_first_mnist_model.h5     # 訓練好的 Keras 模型檔案
|-- lesson9_api_v2.py           # 進化版的 Flask API 伺服器
|-- test_client.py              # 用於測試 API 的客戶端腳本
|-- my_digit.png                # 用於測試的手寫數字範例圖片
|-- README.md                   # 專案說明文件 (就是本文件)
```

## 安裝與設定

1.  複製此專案庫至本地：
    ```bash
    git clone [https://github.com/你的使用者名稱/mnist-digit-recognition-api.git](https://github.com/你的使用者名稱/mnist-digit-recognition-api.git)
    ```
2.  進入專案資料夾並安裝必要的 Python 函式庫：
    ```bash
    cd mnist-digit-recognition-api
    pip install tensorflow Flask numpy Pillow opencv-python-headless requests
    ```

## 如何使用

1.  **啟動 AI 伺服器：**
    在終端機中，執行以下指令來啟動 Flask 伺服器。

    ```bash
    python lesson9_api_v2.py
    ```

    你將會看到伺服器成功啟動的訊息。

2.  **發送預測請求：**
    打開**另一個**新的終端機，執行客戶端腳本來發送預測請求。
    ```bash
    python test_client.py
    ```
    客戶端將會讀取 `my_digit.png` 圖片，發送給伺服器，並印出 AI 的預測結果。

## 關鍵學習與挑戰

這個專案最有價值的學習，來自於**解決模型在真實世界預測失敗的問題**。

- **初次失敗：** 最初版本的 API 在辨識我們自己畫的數字時，發生了嚴重錯誤（例如將 `8` 辨識為 `3`）。經過分析，我們發現這是因為真實世界的圖片（筆劃纖細、大量留白）與標準化的 MNIST 訓練數據存在巨大差異。
- **進化與解決：** 為了解決這個問題，我們升級了 API，整合了 OpenCV 進行專業的圖像預處理。這個進化版的伺服器能夠自動將任意格式的輸入圖片，轉換成更接近 MNIST 風格的「標準化考題」，從而大幅提升了預測的準確性。
- **最終洞見：** 即使經過預處理，模型依然可能因為「書寫風格」的差異而犯錯（例如將底為圓圈的 `2` 誤判為 `8`）。這讓我們深刻理解到：**沒有模型是完美的，一個成功的 AI 專案，不僅在於追求高準確率，更在於理解模型的極限，並圍繞這個極限去設計更健壯的系統。**

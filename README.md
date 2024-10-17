# BackEndSystem
後台與API

# 安裝套件指令
pip install -r requirements.txt

## 設定資料庫、WEBSOCKET_URL、LINEBOT、OPENAI等連線與token資訊
1. 複製 `.env-example` 檔案。
2. 另存新檔為 `.env`。
3. 打開 `.env` 並設定裡面的資訊。

## 啟動後端
python manage.py runserver

## 文字轉語音之語音列表 更改 `voice` 參數即可
找英文 => `en-US` 開頭  
找繁體中文 => `zh-TW` 開頭  
[語音列表參考連結](https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462)

---

***以下兩者需自行下載，並設置環境變數，否則無法執行 react 虛擬人對話運行***

### 語音轉檔套件下載點 - ffmpeg
[下載連結](https://www.ffmpeg.org/download.html)

### wav 轉嘴型 json 檔案套件下載點 - Rhubarb
[下載連結](https://github.com/DanielSWolf/rhubarb-lip-sync/releases)  
參閱安裝教學：[點此參閱](https://vocus.cc/article/64701a2cfd897800014daed0)


from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from django.utils import timezone
from django.apps import apps
from django.db import connection
import torch
import os

class BackendappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendApp'

    def ready(self):
        # 檢查是否在主進程中運行，避免重複調度
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        
        # 使用相對路徑來加載模型
        self.model_path = os.path.join(self.path, 'module', 'emotion')
        self.model = BertForSequenceClassification.from_pretrained(self.model_path)
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        self.device = 0 if torch.cuda.is_available() else -1
        self.classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer, device=self.device)

        # 啟動定時任務
        self.start_scheduler()

    def start_scheduler(self):
        # 初始化 BackgroundScheduler
        scheduler = BackgroundScheduler()

        # 每隔 60 秒執行一次分析任務
        scheduler.add_job(self.analyze_chatlogs, 'interval', seconds=60)

        # 啟動 scheduler
        scheduler.start()

    def analyze_chatlogs(self):
        print("Checking for new ChatLogs to analyze...")

        # 使用 apps.get_model 動態加載模型
        ChatLogs = apps.get_model('backendApp', 'ChatLogs')  # 使用 apps 動態獲取模型

        # 查詢需要進行情緒分析的聊天紀錄
        chatlogs = ChatLogs.objects.filter(emotion_score__isnull=True)

        # 如果沒有新的聊天紀錄，直接返回
        if not chatlogs.exists():
            print("No new ChatLogs found, pausing...")
            return

        # 遍歷每條記錄，對患者的訊息進行情緒分析
        for log in chatlogs:
            try:
                result = self.classifier(log.patient_message)
                label = result[0]['label']
                score = result[0]['score']

                # 根據情緒分數進行五等分
                if 'LABEL_1' in label:
                    if score >= 0.8:
                        final_emotion = 1  # 非常負面
                    elif score >= 0.6:
                        final_emotion = 2  # 負面
                    else:
                        final_emotion = 3  # 中立
                elif 'LABEL_0' in label:
                    if score >= 0.8:
                        final_emotion = 5  # 非常正面
                    elif score >= 0.6:
                        final_emotion = 4  # 正面
                else:
                    final_emotion = 3  # 中立

                # 更新 emotion_score 欄位並保存到資料庫
                log.emotion_score = final_emotion
                log.save()

                print(f"Updated ChatLog ID {log.chatLog_id} with emotion score {final_emotion}")
            except Exception as e:
                print(f"Error during sentiment analysis: {e}")
            finally:
                connection.close()
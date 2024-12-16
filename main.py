from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest
)
from datetime import datetime, timedelta
import json
import os
import requests
from PIL import Image
from io import BytesIO
from firebase import firebase
import google.generativeai as genai


# 使用環境變量讀取憑證
secret = os.getenv('ChannelSecret', None)
token = os.getenv('ChannelAccessToken', None)
firebase_url = os.getenv('FIREBASE_URL')
gemini_key = os.getenv('GOOGLE_GEMINI_API_KEY')


# Initialize the Gemini Pro API
genai.configure(api_key=gemini_key)

handler = WebhookHandler(secret)
configuration = Configuration(
    access_token=token
)


def linebot(request):
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:

        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        event = json_data['events'][0]
        reply_token = event['replyToken']
        user_id = event['source']['userId']
        msg_type = event['message']['type']

        fdb = firebase.FirebaseApplication(firebase_url, None)
        user_chat_path = f'chat/{user_id}'
        chat_state_path = f'state/{user_id}'
        chatgpt = fdb.get(user_chat_path, None)

        if msg_type == 'text':
            msg = event['message']['text']
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(
                    chatId=user_id, loadingSeconds=20))

                if msg == '!empty':
                    reply_msg = 'cleared'
                    fdb.delete(user_chat_path, None)
                elif msg == 'Introduction':
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(
                        f"please introduce Watson's Pharmacy and Yongle Market \n")
                    reply_msg = response.text
                elif msg == "Waston" :
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(
                        f"please describe Watson's Pharmacy more detail \n"
                    )
                    reply_msg = response.text
                elif msg == "Yongle Market":
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(
                        f"please describe Yongle Market more detail \n"
                    )
                    reply_msg = response.text
                elif msg == "Food" or msg == "Eat":
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(
                        f"Please give me food near Yongle Market and Watson's Pharmacy \n"
                    )
                    reply_msg = response.text
                elif msg == "arrange":
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(
                        f"Please help me arrange the itinerary for Watson's Pharmacy and Yongle Market \n"

                    )
                    reply_msg = response.text
                            
                elif msg == "weather":
                    # 動態計算 timeFrom 和 timeTo
                    current_time = datetime.now().replace(minute=0, second=0, microsecond=0)  # 取整點時間
                    time_from = current_time + timedelta(hours=1)  # 往後推一個小時作為開始時間
                    time_to = time_from + timedelta(hours=24)  # 開始時間後推 24 小時作為結束時間

                    # 格式化時間為 ISO8601 格式
                    formatted_time_from = time_from.strftime("%Y-%m-%dT%H:%M:%S")
                    formatted_time_to = time_to.strftime("%Y-%m-%dT%H:%M:%S")

                    # 呼叫氣象 API
                    api_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-061"
                    params = {
                        "Authorization": "CWA-B8287E63-5178-44EE-8ADC-98FD7A7E4036",
                        "locationName": "中正區",
                        "timeFrom": formatted_time_from,
                        "timeTo": formatted_time_to
                    }
                    response = requests.get(api_url, params=params)
                    if response.status_code == 200:
                        weather_data = response.json()

                        # 使用 Gemini 生成分析結果
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content([
                            f"""
                            Based on the weather forecast data below for Zhongzheng District, Taipei, provide a summary of current and upcoming weather conditions. 
                            Include details such as precipitation probability, temperature range, and general weather description. Offer actionable advice for outdoor activities and preparation.

                            Weather data:
                            {json.dumps(weather_data, indent=2)}
                            """
                        ])
                        reply_msg = response.text
                    else:
                        reply_msg = "無法取得天氣資訊，請稍後再試。"

                elif msg == "clothes":
                    # 動態計算 timeFrom 和 timeTo
                    current_time = datetime.now().replace(minute=0, second=0, microsecond=0)  # 取整點時間
                    time_from = current_time + timedelta(hours=1)  # 往後推一個小時作為開始時間
                    time_to = time_from + timedelta(hours=24)  # 開始時間後推 24 小時作為結束時間

                    # 格式化時間為 ISO8601 格式
                    formatted_time_from = time_from.strftime("%Y-%m-%dT%H:%M:%S")
                    formatted_time_to = time_to.strftime("%Y-%m-%dT%H:%M:%S")

                    # 呼叫氣象 API
                    api_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-061"
                    params = {
                        "Authorization": "CWA-B8287E63-5178-44EE-8ADC-98FD7A7E4036",
                        "locationName": "中正區",
                        "timeFrom": formatted_time_from,
                        "timeTo": formatted_time_to
                    }
                    response = requests.get(api_url, params=params)
                    if response.status_code == 200:
                        weather_data = response.json()

                        # 使用 Gemini 生成穿衣建議
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content([
                            f"""
                            Based on the weather forecast data below for Zhongzheng District, Taipei, provide suitable clothing recommendations. 
                            Consider factors such as temperature range, precipitation probability, and general weather conditions.

                            Weather data:
                            {json.dumps(weather_data, indent=2)}
                            """
                        ])
                        reply_msg = response.text
                    else:
                        reply_msg = "無法取得穿衣建議，請稍後再試。"

               
                else:
                    if chatgpt is None:
                        messages = []
                    else:
                        messages = chatgpt
                    model = genai.GenerativeModel('gemini-pro')
                    messages.append({'role': 'user', 'parts': [msg]})
                    response = model.generate_content(messages)
                    messages.append(
                        {'role': 'model', 'parts': [response.text]})
                    reply_msg = response.text
                    # 更新firebase中的對話紀錄
                    fdb.put_async(user_chat_path, None, messages)

                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[
                            TextMessage(text=reply_msg),
                        ]))
        else:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[
                            TextMessage(text='你傳的不是文字訊息呦'),
                        ]))

    except Exception as e:
        detail = e.args[0]
        print(detail)
    return 'OK'



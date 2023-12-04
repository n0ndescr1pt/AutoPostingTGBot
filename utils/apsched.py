import sqlite3
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode

from data.config import Chat_id


async def send_message_interval(bot: Bot):
    connection = sqlite3.connect('posts.db')
    cursor = connection.execute("SELECT user_id, text, image, createDate, liveTime FROM post;")
    for row in cursor:
        dateTimeStr = row[3]
        elapsedTime = datetime.now() - datetime.strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S.%f')
        print(elapsedTime.seconds)
        if (elapsedTime.seconds>row[4]):
            if(len(row[2])==0):
                await bot.send_message(chat_id=Chat_id,text=f"{str(row[1])}\n\nавтопостинг @avtoaid\\_bot", disable_web_page_preview=True)
            else:
                await bot.send_photo(chat_id=Chat_id,caption=f"{str(row[1])}\n\nавтопостинг",photo= row[2])
            connection.execute("DELETE FROM post where user_id = (?) and createDate = (?)",(row[0],row[3]))

    connection.commit()
    connection.close()
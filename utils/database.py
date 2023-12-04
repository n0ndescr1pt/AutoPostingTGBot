import sqlite3
from sqlite3 import IntegrityError

from aiogram.types import DateTime

from data.config import interval


def addData(message_id, message, image, user_id, count):
    # Подключение к базе данных
    connection = sqlite3.connect('posts.db')

    # Вставка данных в таблицу
    connection.execute("INSERT INTO uncheck (message_id, text,image, user_id, count) VALUES (?, ?, ?, ?, ?)",
                       (message_id, message, image, user_id, count))

    # Сохранение изменений
    connection.commit()

    # Закрытие соединения
    connection.close()


async def delData(message_id):
    connection = sqlite3.connect('posts.db')
    connection.execute("DELETE FROM uncheck WHERE message_id=?", (message_id,))
    connection.commit()
    connection.close()


async def addToReady(message_id, count: int,user_id: int):
    connection = sqlite3.connect('posts.db')
    for i in range(count):
        userPost = await getUserPostCount(user_id)
        connection.execute("INSERT INTO post ( user_id, text, image, createDate, liveTime) "
                           "Values( (?), (SELECT text FROM uncheck WHERE message_id=?), (SELECT image FROM uncheck WHERE message_id=?), (?), (?))",(user_id, message_id, message_id, DateTime.now(),userPost*interval))
        connection.commit()
    connection.execute("DELETE FROM uncheck WHERE message_id=?", (message_id,))
    connection.commit()
    connection.close()

async def getUserPostCount(user_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    info = cursor.execute("SELECT COUNT(*) FROM post WHERE user_id = (?)", (user_id,)).fetchone()
    connection.close()
    return info[0]


async def add_new_payment(payment_id: int, summa: float):
    connection = sqlite3.connect('posts.db')
    connection.execute("INSERT INTO payments (payment_id, summa) VALUES(?,?)", (payment_id, summa))
    try:
        connection.commit()
    except IntegrityError:
        connection.rollback()
    connection.close()


async def select_payment(payment_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    info = cursor.execute("SELECT payment_id,summa FROM payments WHERE payment_id = (?)", (payment_id,)).fetchone()
    connection.close()
    return info


async def delete_payment(payment_id: int):
    connection = sqlite3.connect('posts.db')
    connection.execute("DELETE FROM payments WHERE payment_id = (?)", (payment_id,))
    connection.commit()
    connection.close()


async def update_balance(user_id: int, balance: float):
    connection = sqlite3.connect('posts.db')
    nowBalance = await getBalance(user_id)
    connection.execute(f"UPDATE users set balance = {balance+nowBalance} WHERE user_id = (?)", (user_id,))
    connection.commit()
    connection.close()


async def addNewUser(user_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    id = cursor.execute("SELECT * FROM users WHERE user_id = (?)", (user_id,)).fetchone()

    # print(id)
    if id is None:
        connection.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        connection.commit()
    connection.close()


async def giveAllUsers():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users")
    res = cursor.fetchall()
    connection.close()
    return res


async def setPricePerPost(price: float):
    connection = sqlite3.connect('posts.db')
    connection.execute(f"UPDATE prices set price_per_post = (?) WHERE id = (?) ", (price, 1))
    connection.commit()
    connection.close()


async def checkMyPost(user_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    posts = cursor.execute("SELECT text, image FROM uncheck WHERE user_id = (?)", (user_id,)).fetchall()
    connection.close()
    return posts


###################################################################
async def orderPosts():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    posts = cursor.execute("SELECT count(id) FROM post ").fetchone()
    connection.close()
    return posts[0]


###################################################################

async def getPrice():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    posts = cursor.execute("SELECT price_per_post FROM prices WHERE id = (?) ", (1,)).fetchone()
    connection.close()
    return posts[0]


async def getBalance(user_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.execute("SELECT balance FROM users WHERE user_id = (?)", (user_id,))
    records = cursor.fetchone()
    connection.close()
    return records[0]


async def payForPost(user_id: int):
    price = await getPrice()
    balance = await getBalance(user_id)
    min = balance - price
    connection = sqlite3.connect('posts.db')
    connection.execute(f"UPDATE users set balance = (?) WHERE user_id = (?) ", (min, user_id))
    connection.commit()
    connection.close()


async def getCountMessage(message_id: int):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    posts = cursor.execute("SELECT count FROM uncheck WHERE message_id = (?) ", (message_id,)).fetchone()
    connection.close()
    return posts[0]

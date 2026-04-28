import random
import time
import sqlite3
import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler )
from telegram.ext import MessageHandler, filters
TOKEN = ("8788193406:AAExA1aI4feuzuf5hgD2CPc5r9MsCEL0hT4")
ADMIN_ID = 1257248239
COOLDOWN = 1800

IMAGES = [
    ("https://i.pinimg.com/originals/82/b9/8f/82b98f58172f08476b66d6fa59f31b3f.jpg?nii=t",
     "Мопс косий\nредкий\nкарточка 1/45"),
    ("https://media.istockphoto.com/id/2172252904/ru/%D1%84%D0%BE%D1%82%D0%BE/%D1%81%D1%87%D0%B0%D1%81%D1%82%D0%BB%D0%B8%D0%B2%D1%8B%D0%B9-%D1%87%D0%B5%D1%80%D0%BD%D1%8B%D0%B9-%D0%BC%D0%BE%D0%BF%D1%81-%D0%BD%D0%B0-%D1%80%D0%BE%D0%B7%D0%BE%D0%B2%D0%BE%D0%BC-%D1%84%D0%BE%D0%BD%D0%B5.jpg?s=612x612&w=0&k=20&c=5WylBMpnENILEM81bYHcjvqTWI_DlA_opwtWYXWTyms=",
     "Мопс черний\nредкий\nкарточка 2/45"),
    ("https://as2.ftcdn.net/jpg/06/77/95/69/1000_F_677956993_UZfjfMDyy73fWmeUSY79zlY3L11e4o7s.jpg",
     "Мопс на пляже\nэпик\nкарточка 3/45"),
    ("https://www.image2url.com/r2/default/images/1777233831523-65beec46-1310-406a-9d17-1a7143805428.jpg",
     "Мопс курьер\nобычный\nкарточка 4/45"),
    ("https://www.image2url.com/r2/default/images/1777234174893-0239379e-139a-4341-9202-87c945419851.jpg",
     "Мопс таксист\nредкий\nкарточка 5/45"),
    ("https://www.image2url.com/r2/default/images/1777234279965-64d6b4ed-cc69-43f4-9b5c-598c7d404762.jpg",
     "Мопс руфер\nлегендарный\nкарточка 6/45"),
    ("https://www.image2url.com/r2/default/images/1777234633183-5c033e32-b326-448d-81fd-bded36a7ea54.jpg",
     "Мопс бомбер\nмифик\nкарточка 7/45"),
    ("https://www.image2url.com/r2/default/images/1777234750003-f3fa46ea-506a-4022-ada2-89dfb3ab60cf.jpg",
     "Мопс зацепер\nмифик\nкарточка 8/45"),
    ("https://cdn.corenexis.com/files/c/3787565720.jpg", "Бедный мопс\nобычный\nкарточка 9/45"),
    ("https://www.image2url.com/r2/default/images/1777296284110-83bc0494-0f4b-46cd-9ca4-87a2439de8cb.jpg",
     "Мопс хардкорщик\nредкий\nкарточка 10/45"),
    ("https://cdn.corenexis.com/files/c/2996862720.jpg", "Мопс сталкер\nобычный\nкарточка 11/45"),
    ("https://cdn.corenexis.com/files/c/1516565720.jpg", "Деловой мопс\nэпик\nкарточка 12/45"),
    ("https://cdn.corenexis.com/files/c/9577361720.jpg", "Богатый мопс\nлегендарный\nкарточка 13/45"),
    ("https://cdn.corenexis.com/files/c/2167515720.jpg", "СЕКРЕТНЫЙ МОПС\nэксклюзив\nкарточка 99"),
    ("https://cdn.corenexis.com/files/c/1163111720.jpg", "Мопс водолаз\nмифик\nкарточка 15/45"),
    ("https://cdn.corenexis.com/files/c/1496982720.jpg", "Мопс строитель\nредкий\nкарточка 16/45"),
    ("https://cdn.corenexis.com/files/c/7184372720.jpg", "Мопс геймер\nэпик\nкарточка 17/35"),
    ("https://cdn.corenexis.com/files/c/8897744720.jpg", "Мопс атлет\nобычный\nкарточка 18/45"),
    ("https://cdn.corenexis.com/files/c/4737463720.jpg", "Мопс сантехник\nредкий\nкарточка 19/45"),
    ("https://cdn.corenexis.com/files/c/1518365720.jpg", "Мопс повар\nэпик\nкарточка 21/35"),
    ("https://cdn.corenexis.com/files/c/2952629720.jpg", "Мопс продавец\nобычный\nкарточка 22/45"),
    ("https://cdn.corenexis.com/files/c/3393823720.jpg", "Мопс на самокате\nэпик\nкарточка 23/45"),
    ("https://cdn.corenexis.com/files/c/9499629720.jpg", "Мопс учитель\nобычный\nкарточка 24/45"),
    ("https://cdn.corenexis.com/files/c/6413233720.jpg", "Мопс скалолаз\nредкий\nкарточка 25/45"),
    ("https://cdn.corenexis.com/files/c/7784419720.jpg", "Мопс водитель\nредкий\nкарточка 26/45"),
    ("https://cdn.corenexis.com/files/c/7924959720.jpg", "Мопс консультант\nредкий\nкарточка 27/45"),
    ("https://cdn.corenexis.com/files/c/8222652720.jpg", "Пухлый мопс\nобычный\nкарточка 28/45"),
    ("https://cdn.corenexis.com/files/c/1225294720.jpg", "Мопс боксер\nобычный\nкарточка 29/45"),
    ("https://cdn.corenexis.com/files/c/3366882720.jpg", "Мопс в очках\nобычный\nкарточка 31/45"),
    ("https://cdn.corenexis.com/files/c/7121318720.jpg", "Зловещий мопс\nобычный\nкарточка 30/45"),
    ("https://cdn.corenexis.com/files/c/3553262720.jpg", "Мопс полицейский\nредкий\nкарточка 32/45"),
    ("https://cdn.corenexis.com/files/c/7835327720.jpg", "Мопс в бане\nобычный\nкарточка 33/45"),
    ("https://cdn.corenexis.com/files/c/7533156720.jpg", "Мопс в отеле\nобычный\nкарточка 34/45"),
    ("https://cdn.corenexis.com/files/c/8412442720.jpg", "Мопс судья\nэпик\nкарточка 35/35"),
    ("https://cdn.corenexis.com/files/c/6978758720.jpg", "Мопс бандит\nмифик\nкарточка 36/45"),
    ("https://cdn.corenexis.com/files/c/3829398720.jpg", "Мопс пчеловод\nобычный\nкарточка 37/45"),
    ("https://cdn.corenexis.com/files/c/7946282720.jpg", "Мопс в ванне\nобычный\nкарточка 38/45"),
    ("https://cdn.corenexis.com/files/c/8288725720.jpg", "Мопс военный\nобычный\nкарточка 39/45"),
    ("https://cdn.corenexis.com/files/c/1853145720.jpg", "Мопс снайпер\nэрпик\nкарточка 40/45"),
    ("https://cdn.corenexis.com/files/c/1963245720.jpg", "Мопс гонщик\nредкий\nкарточка 41/45"),
    ("https://cdn.corenexis.com/files/c/8697164720.jpg", "Мопс хакер\nЭксклюзив\nкарточка 42/45"),

]

REWARD = {
    "обычный": 5,
    "редкий": 10,
    "эпик": 20,
    "мифик": 40,
    "легендарный": 80

}

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    last_used REAL,
    streak INTEGER DEFAULT 0,
    coins INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collection (
    user_id INTEGER,
    card_id INTEGER,
    UNIQUE(user_id, card_id)
)
""")

conn.commit()


def get_rarity(text):
    text = text.lower()
    for r in REWARD:
        if r in text:
            return r
    return "обычный"


async def mops_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower().strip() == "мопс":
        await mops(update, context)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n\n"
        "Добавляй бота в группу и получай мопсов с друзьями!\n"
        "тгк-https://t.me/fraksup\n"
        "/mops — получить мопса\n"
        "/profil — профиль\n"
        "/tops — топ\n"
        "/shop — магазин"
    )


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Купить секретного мопса (500💰)", callback_data="buy_secret")],
        [InlineKeyboardButton("🎲 Купить случайную картинку за 250💰", callback_data="buy_random_image")]
    ]
    await update.message.reply_text("Магазин:", reply_markup=InlineKeyboardMarkup(keyboard))


async def mops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
    message = update.message
else:
    message = update.callback_query.message
    user_id = update.effective_user.id
    now = time.time()
    today = datetime.date.today()

    cursor.execute("SELECT last_used, streak, coins FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if row:
        last_used, streak, coins = row
        last_date = datetime.date.fromtimestamp(last_used)
        if now - last_used < COOLDOWN:
            remaining = int(COOLDOWN - (now - last_used))

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            if hours > 0:
                await update.message.reply_text(f"⏳ Подожди {hours} ч. {minutes} мин.")
            else:
                await update.message.reply_text(f"⏳ Подожди {minutes} мин.")

            return

        if last_date == today:
            pass
        elif (today - last_date).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
        coins = 0

    cursor.execute("SELECT card_id FROM collection WHERE user_id=?", (user_id,))
    owned = {row[0] for row in cursor.fetchall()}

    # список доступных (которых еще нет)
    available = [i for i in range(len(IMAGES) - 1) if i not in owned]
    if not available:
        await query.message.reply_text("Ты собрал все карты 🐶")
        return

    card_id = random.choice(available)

    # если все собраны — даем любую
    available = [i for i in range(len(IMAGES) - 1) if i not in owned]

    if not available:
        card_id = random.randint(0, len(IMAGES) - 2)
    else:
        card_id = random.choice(available)

    img, cap = IMAGES[card_id]

    rarity = get_rarity(cap)
    reward = REWARD.get(rarity, 5)
    coins += reward

    cursor.execute("SELECT 1 FROM collection WHERE user_id=? AND card_id=?", (user_id, card_id))
    cursor.execute("INSERT OR IGNORE INTO collection VALUES (?, ?)", (user_id, card_id))
    cursor.execute("""
    INSERT INTO users (user_id, last_used, streak, coins)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        last_used=excluded.last_used,
        streak=excluded.streak,
        coins=excluded.coins
    """, (user_id, now, streak, coins))

    conn.commit()

    await update.message.reply_photo(
        photo=img,
        caption=f"{cap}\n\n💰 +{reward}\n🔥 {streak}\n💸 {coins}"
    )


async def profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("SELECT coins, streak FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    coins = row[0] if row else 0
    streak = row[1] if row else 0

    keyboard = [
        [InlineKeyboardButton("Мои мопсы", callback_data="show")]
    ]

    await update.message.reply_text(
        f"👤 Профиль\n\n💸 Монеты: {coins}\n🔥 Стрик: {streak}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # 🛒 покупка
    if query.data == "buy_secret":
        cursor.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()

        if not row or row[0] < 500:
            await query.message.reply_text("Нет денег")
            return

        coins = row[0] - 500
        secret_id = len(IMAGES) - 1

        cursor.execute("UPDATE users SET coins=? WHERE user_id=?", (coins, user_id))
        cursor.execute("INSERT INTO collection VALUES (?, ?)", (user_id, secret_id))
        conn.commit()

        img, cap = IMAGES[secret_id]
        await query.message.reply_photo(photo=img, caption=cap)
        return
    if query.data == "buy_random_image":
        cursor.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()

        if not row or row[0] < 250:
            await query.message.reply_text("Нет денег")
            return

        coins = row[0] - 250

        # получаем карты пользователя
        cursor.execute("SELECT card_id FROM collection WHERE user_id=?", (user_id,))
        owned = {r[0] for r in cursor.fetchall()}

        # доступные карты
        available = [i for i in range(len(IMAGES)) if i not in owned]

        if not available:
            await query.message.reply_text("Ты собрал все карты 🐶")
            return

        card_id = random.choice(available)
        img, cap = IMAGES[card_id]

        # награда
        rarity = get_rarity(cap)
        reward = REWARD.get(rarity, 15)
        coins += reward

        # добавляем карту
        cursor.execute(
            "INSERT OR IGNORE INTO collection VALUES (?, ?)",
            (user_id, card_id)
        )

        # обновляем баланс
        cursor.execute("UPDATE users SET coins=? WHERE user_id=?", (coins, user_id))
        conn.commit()

        await query.message.reply_photo(
            photo=img,
            caption=f"{cap}\n\n💰 +{reward}\n💸 {coins}"
        )
        return

    if query.data == "top_streak":
        cursor.execute("SELECT user_id, streak FROM users ORDER BY streak DESC LIMIT 10")
        rows = cursor.fetchall()

        text = "🔥 Топ по стрику:\n\n"
        for i, (uid, streak) in enumerate(rows, 1):
            try:
                user = await context.bot.get_chat(uid)
                name = user.first_name if user.first_name else "Без имени"
                text += f"{i}. {name} — {streak}\n"
            except:
                text += f"{i}. Без имени — {streak}\n"

        await query.message.reply_text(text)
        return

    if query.data == "top_coins":
        cursor.execute("SELECT user_id, coins FROM users ORDER BY coins DESC LIMIT 10")
        rows = cursor.fetchall()

        text = "💰 Топ по монетам:\n\n"
        for i, (uid, coins) in enumerate(rows, 1):
            try:
                user = await context.bot.get_chat(uid)
                name = user.first_name if user.first_name else "Без имени"
                text += f"{i}. {name} — {coins}\n"
            except:
                text += f"{i}. Без имени — {coins}\n"

        await query.message.reply_text(text)
        return

    if query.data == "top_cards":
        cursor.execute("""
            SELECT user_id, COUNT(DISTINCT card_id)
            FROM collection
            GROUP BY user_id
            ORDER BY COUNT(DISTINCT card_id) DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()

        text = "🐶 Топ по картам:\n\n"
        for i, (uid, total) in enumerate(rows, 1):
            try:
                user = await context.bot.get_chat(uid)
                name = user.first_name if user.first_name else "Без имени"
                text += f"{i}. {name} — {total}\n"
            except:
                text += f"{i}. Без имени — {total}\n"

        await query.message.reply_text(text)
        return

    # 📦 профиль
    cursor.execute("SELECT card_id FROM collection WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    for (cid,) in set(rows):
        img, cap = IMAGES[cid]
        await query.message.reply_photo(photo=img, caption=cap)


async def tops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Стрик", callback_data="top_streak")],
        [InlineKeyboardButton("💰 Монеты", callback_data="top_coins")],
        [InlineKeyboardButton("🐶 Карты", callback_data="top_cards")]
    ]

    await update.message.reply_text(
        "Выбери топ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# админка (НЕ ТРОГАЛ)
async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()

    await update.message.reply_text(f"👥 Всего: {len(rows)}")

    for (uid,) in rows:
        try:
            user = await context.bot.get_chat(uid)
            name = user.first_name
            username = f"@{user.username}" if user.username else ""
            await update.message.reply_text(f"{name} {username}")
        except:
            await update.message.reply_text("Пользователь")

        await asyncio.sleep(1)


async def add_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    amount = int(context.args[1])
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id=?", (amount, uid))
    conn.commit()
    await update.message.reply_text("Монеты выданы")


async def remove_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    amount = int(context.args[1])
    cursor.execute("UPDATE users SET coins = coins - ? WHERE user_id=?", (amount, uid))
    conn.commit()
    await update.message.reply_text("Монеты сняты")


async def set_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    streak = int(context.args[1])
    cursor.execute("UPDATE users SET streak=? WHERE user_id=?", (streak, uid))
    conn.commit()
    await update.message.reply_text("Стрик установлен")


async def add_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    amount = int(context.args[1])
    cursor.execute("UPDATE users SET streak = streak + ? WHERE user_id=?", (amount, uid))
    conn.commit()
    await update.message.reply_text("Стрик добавлен")


async def remove_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    amount = int(context.args[1])
    cursor.execute("UPDATE users SET streak = streak - ? WHERE user_id=?", (amount, uid))
    conn.commit()
    await update.message.reply_text("Стрик уменьшен")
async def give_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    card_id = int(context.args[1])

    cursor.execute("INSERT INTO collection VALUES (?, ?)", (uid, card_id))
    conn.commit()

    await update.message.reply_text("Карта выдана")


async def remove_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    card_id = int(context.args[1])

    cursor.execute("DELETE FROM collection WHERE user_id=? AND card_id=?", (uid, card_id))
    conn.commit()

    await update.message.reply_text("Карта удалена")



# 🏀 КОЛЬЦО
async def ring_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) < 1:
        await update.message.reply_text("Использование: /ring сумма")
        return

    try:
        bet = int(context.args[0])
    except:
        await update.message.reply_text("Введи число")
        return

    if bet <= 0 or bet > 20:
        await update.message.reply_text("Ставка: 1-20")
        return

    cursor.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if not row or row[0] < bet:
        await update.message.reply_text("Нет денег")
        return

    coins = row[0] - bet

    msg = await update.message.reply_dice(emoji="🏀")
    await asyncio.sleep(3)

    if msg.dice.value >= 4:
        win = int(bet * 1.8)
        coins += win
        text = f"🏀 Попал!\n+{win}"
    else:
        text = "🏀 Мимо!"

    cursor.execute("UPDATE users SET coins=? WHERE user_id=?", (coins, user_id))
    conn.commit()

    await update.message.reply_text(f"{text}\n💸 {coins}")
    return


# 🎲 КУБИК
async def dice_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) < 1:
        await update.message.reply_text("Использование: /dice сумма")
        return

    try:
        bet = int(context.args[0])
    except:
        await update.message.reply_text("Введи число")

    if bet <= 0 or bet > 20:
        await update.message.reply_text("Ставка: 1-20")
        return

    cursor.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if not row or row[0] < bet:
        await update.message.reply_text("Нет денег")
        return

    coins = row[0] - bet

    roll = random.randint(1, 6)

    if roll >= 4:
        win = bet * 2
        coins += win
        result = f"🎲 Выпало {roll}\n+{win}"
    else:
        result = f"🎲 Выпало {roll}\nПроиграл"

    cursor.execute("UPDATE users SET coins=? WHERE user_id=?", (coins, user_id))
    conn.commit()

    await update.message.reply_text(f"{result}\n💸 {coins}")
    return



app = ApplicationBuilder().token(TOKEN).build()


app.add_handler(CommandHandler("dice", dice_game))
app.add_handler(CommandHandler("ring", ring_game))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mops", mops))
app.add_handler(CommandHandler("profil", profil))
app.add_handler(CommandHandler("tops", tops))
app.add_handler(CommandHandler("shop", shop))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mops_trigger))



app.add_handler(CommandHandler("users", users_list))
app.add_handler(CommandHandler("givecard", give_card))
app.add_handler(CommandHandler("removecard", remove_card))
app.add_handler(CommandHandler("addcoins", add_coins))
app.add_handler(CommandHandler("removecoins", remove_coins))
app.add_handler(CommandHandler("setstreak", set_streak))
app.add_handler(CommandHandler("addstreak", add_streak))
app.add_handler(CommandHandler("removestreak", remove_streak))

app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()

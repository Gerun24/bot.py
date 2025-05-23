from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import random

bot = Bot(token="7864244507:AAEfNjZSVsN9NSdTOvxJrxhMSuUsuyURXFU")  # ← сюда вставь свой токен от BotFather
dp = Dispatcher(bot)

users = {}  # user_id: {"bank": 1000, "sequence": [100, 100]}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    uid = message.from_user.id
    users[uid] = {"bank": 1000, "sequence": [100, 100]}
    await message.answer("Добро пожаловать! Ваш банк: 1000.\nГотовы делать ставки по стратегии Фибоначчи.")

@dp.message_handler(commands=["bet"])
async def bet(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        await message.answer("Сначала введите /start")
        return
    user = users[uid]
    seq = user["sequence"]
    if len(seq) < 2:
        seq = [100, 100]
    stake = seq[-1] + seq[-2]
    result = random.choice(["win", "lose"])
    if result == "win":
        user["bank"] += int(stake * 0.9)
        if len(seq) > 2:
            seq = seq[1:-1]
        else:
            seq = [100, 100]
        await message.answer(f"✅ Победа!\nСтавка: {stake} → выигрыш ~{int(stake*0.9)}\nНовый банк: {user['bank']}")
    else:
        user["bank"] -= stake
        seq.append(stake)
        await message.answer(f"❌ Поражение.\nСтавка: {stake}\nНовый банк: {user['bank']}")
    user["sequence"] = seq

@dp.message_handler(commands=["status"])
async def status(message: types.Message):
    uid = message.from_user.id
    if uid not in users:
        await message.answer("Сначала введите /start")
        return
    user = users[uid]
    await message.answer(f"💰 Банк: {user['bank']}\n🔁 Стратегия: {user['sequence']}")

@dp.message_handler(commands=["reset"])
async def reset(message: types.Message):
    uid = message.from_user.id
    users[uid] = {"bank": 1000, "sequence": [100, 100]}
    await message.answer("Стратегия и банк сброшены.")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.answer("/start – начать\n/bet – сделать ставку\n/status – банк и стратегия\n/reset – сброс\n/help – помощь")

if __name__ == "__main__":
    executor.start_polling(dp)

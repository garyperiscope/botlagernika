import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import BOT_TOKEN, supabase
from database import save_user, get_user, update_user

# 🔹 Настройка логирования
logging.basicConfig(level=logging.INFO)

# 🔹 Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔹 Клавиатура с кнопками
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Проверить данные"), KeyboardButton(text="✏️ Обновить данные")],
        [KeyboardButton(text="ℹ️ О лагере")]
    ],
    resize_keyboard=True
)

# 🔹 Хэндлер команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Введи свои данные.\n\n"
        "Напиши: Имя родителя, Имя ребенка, Дата рождения (ГГГГ-ММ-ДД), Посещенные смены",
        reply_markup=menu_keyboard
    )

# 🔹 Хэндлер сохранения данных
@dp.message()
async def save_user_data(message: types.Message):
    if "," in message.text:
        try:
            data = message.text.split(",")
            parent_name, child_name, birth_date, attended_shifts = map(str.strip, data)

            save_user(parent_name, child_name, birth_date, attended_shifts)
            await message.answer(f"✅ Данные сохранены!\n\n"
                                 f"👨‍👩‍👧 Родитель: {parent_name}\n"
                                 f"👶 Ребенок: {child_name}\n"
                                 f"📅 Дата рождения: {birth_date}\n"
                                 f"🏕 Посещенные смены: {attended_shifts}")
        except Exception:
            await message.answer("⚠ Ошибка! Введите данные через запятую: Имя родителя, Имя ребенка, Дата рождения (ГГГГ-ММ-ДД), Посещенные смены")

# 🔹 Хэндлер команды /check (проверка данных)
@dp.message(lambda message: message.text == "📋 Проверить данные")
async def check_user_data(message: types.Message):
    parent_name = message.from_user.full_name  # Берём имя родителя как username
    user_data = get_user(parent_name)

    if user_data:
        data = user_data[0]
        response = (f"📌 Данные:\n\n"
                    f"👨‍👩‍👧 Родитель: {data['parent_name']}\n"
                    f"👶 Ребенок: {data['child_name']}\n"
                    f"📅 Дата рождения: {data['birth_date']}\n"
                    f"🏕 Посещенные смены: {data['attended_shifts']}")
    else:
        response = "❌ Данные не найдены. Введите их заново."

    await message.answer(response)

# 🔹 Хэндлер обновления данных
@dp.message(lambda message: message.text == "✏️ Обновить данные")
async def update_user_data(message: types.Message):
    await message.answer("🔄 Введи новые данные в формате: Имя родителя, Имя ребенка, Дата рождения (ГГГГ-ММ-ДД), Посещенные смены")

@dp.message()
async def update_data(message: types.Message):
    if "," in message.text:
        try:
            data = message.text.split(",")
            parent_name, child_name, birth_date, attended_shifts = map(str.strip, data)

            update_user(parent_name, {"child_name": child_name, "birth_date": birth_date, "attended_shifts": attended_shifts})
            await message.answer(f"✅ Данные обновлены!\n\n"
                                 f"👨‍👩‍👧 Родитель: {parent_name}\n"
                                 f"👶 Ребенок: {child_name}\n"
                                 f"📅 Дата рождения: {birth_date}\n"
                                 f"🏕 Посещенные смены: {attended_shifts}")
        except Exception:
            await message.answer("⚠ Ошибка! Проверь формат данных.")

# 🔹 Проверка подключения к Supabase
try:
    data = supabase.table("users").select("*").execute()
    print("✅ Подключение к Supabase успешно! Данные:", data.data)
except Exception as e:
    print("❌ Ошибка подключения к Supabase:", e)

# 🔹 Функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

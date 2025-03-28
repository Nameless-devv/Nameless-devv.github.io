import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Bot tokenini shu yerga qo'shing
API_TOKEN = "7669996293:AAFUXTV08VqJWenWRA2G07N0guTDLtdIN3E"

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratamiz
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Foydalanuvchi tillari
user_languages = {}


# JSON fayllardan ma'lumotlarni yuklash
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


districts_data = load_json("tuman.json")
neighborhoods_data = load_json("mahalla.json")


# Til tanlash klaviaturasi
def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" Ўзбек тили", callback_data="lang_uz"),
         InlineKeyboardButton(text=" Қорақалпоқ тили", callback_data="lang_kk")]
    ])


# Tuman tugmalari
def get_districts_keyboard(lang):
    keyboard_buttons = []

    # Tilga qarab birinchi tugmalarni joylashtirish
    if lang == "uz":
        first_button = [InlineKeyboardButton(text="Нукус шаҳар", callback_data="district_nukus")]
    else:
        first_button = [InlineKeyboardButton(text="Нөкис қаласы", callback_data="district_nukus")]

    keyboard_buttons.append(first_button)

    temp_buttons = []
    for district_id, district_info in districts_data.items():
        if district_info["name_uz"] == "Нукус шаҳар" or district_info["name_kk"] == "Нөкис қаласы":
            continue  # Avvaldan qo‘shilgan tugmalarni qayta chiqarmaslik

        text = district_info["name_uz"] if lang == "uz" else district_info["name_kk"]
        temp_buttons.append(InlineKeyboardButton(text=text, callback_data=f"district_{district_id}"))

        if len(temp_buttons) == 2:
            keyboard_buttons.append(temp_buttons)
            temp_buttons = []

    if temp_buttons:
        keyboard_buttons.append(temp_buttons)

    keyboard_buttons.append([
        InlineKeyboardButton(text="🔙 Орқага" if lang == "uz" else "🔙 Артқа", callback_data="back_to_language")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


# Mahalla tugmalari
def get_neighborhoods_keyboard(district_id, lang):
    keyboard_buttons = []
    temp_buttons = []
    for neighborhood in neighborhoods_data.get(district_id, []):
        text = neighborhood["name_uz"] if lang == "uz" else neighborhood["name_kk"]
        temp_buttons.append(InlineKeyboardButton(text=text, callback_data=f"neigh_{neighborhood['id']}"))
        if len(temp_buttons) == 2:
            keyboard_buttons.append(temp_buttons)
            temp_buttons = []

    if temp_buttons:
        keyboard_buttons.append(temp_buttons)

    keyboard_buttons.append([
        InlineKeyboardButton(text="🔙 Орқага" if lang == "uz" else "🔙 Артқа", callback_data="back")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

# Mahalla tanlanganda
@dp.callback_query(F.data.startswith("neigh_"))
async def send_inspector_info(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "uz")
    neighborhood_id = callback.data.split("_")[1]
    for district_id, neighborhoods in neighborhoods_data.items():
        for neighborhood in neighborhoods:
            if neighborhood["id"] == neighborhood_id:
                inspector = neighborhood.get("inspektor", "Номаълум")
                phone = neighborhood.get("telefon", "Номаълум")
                msg = f"📍 {neighborhood['name_uz']} маҳалласи\n👮 Инспектор: {inspector}\n📞 Телефон: {phone}" if lang == "uz" else f"📍 {neighborhood['name_kk']} мәхәлләси\n👮 Инспектор: {inspector}\n📞 Телефон: {phone}"
                await callback.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🔙 Орқага" if lang == "uz" else "🔙 Артқа", callback_data="back")]]
                ))
                return


# /start buyrug'iga javob
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Тилни танланг / Тилди сайлаң:", reply_markup=get_language_keyboard())


# Til tanlanganda saqlash
@dp.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang
    msg = "Туманингизни танланг:" if lang == "uz" else "Районыңызды сайлаң:"
    await callback.message.edit_text(msg, reply_markup=get_districts_keyboard(lang))


# Tuman tanlanganda
@dp.callback_query(F.data.startswith("district_"))
async def send_neighborhoods(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "uz")
    district_id = callback.data.split("_")[1]

    if district_id == "nukus":
        msg = "📍 Нукус шаҳаридаги маҳаллаларни танланг:" if lang == "uz" else "📍 Нөкис қаласындағы мәхәллелерди сайлаң:"
    else:
        district_name = districts_data.get(district_id, {}).get("name_uz", "") if lang == "uz" else districts_data.get(district_id, {}).get("name_kk", "")
        msg = f"📍 {district_name}даги маҳаллаларни танланг:" if lang == "uz" else f"📍 {district_name}дағы мәхәллелерди сайлаң:"

    keyboard = get_neighborhoods_keyboard(district_id, lang)
    await callback.message.edit_text(msg, reply_markup=keyboard)


# Орқага қайтиш тугмаси
@dp.callback_query(F.data == "back")
async def go_back(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "uz")
    await callback.message.edit_text("Туманингизни танланг:" if lang == "uz" else "Районыңызды сайлаң:",
                                     reply_markup=get_districts_keyboard(lang))


# Тил танлашга қайтиш
@dp.callback_query(F.data == "back_to_language")
async def back_to_language(callback: types.CallbackQuery):
    await callback.message.edit_text("Тилни танланг / Тилди сайлаң:", reply_markup=get_language_keyboard())


# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

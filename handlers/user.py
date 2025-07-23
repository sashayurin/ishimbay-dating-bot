from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os

router = Router()

ADMIN_ID = int(os.getenv("ADMIN_ID"))
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
PRICE_RUB = int(os.getenv("PRICE_RUB", 149))


class RegisterForm(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Это бот знакомств городов Ишимбай, Салават, Стерлитамак и др. 💌\n"
                         "Давай создадим твою анкету.\nКак тебя зовут?")
    await state.set_state(RegisterForm.name)


@router.message(StateFilter(RegisterForm.name))
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое. Пожалуйста, введи полное имя.")
        return
    await state.update_data(name=name)
    await message.answer("Сколько тебе лет?")
    await state.set_state(RegisterForm.age)


@router.message(StateFilter(RegisterForm.age))
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи число.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Ты парень или девушка?")
    await state.set_state(RegisterForm.gender)


@router.message(StateFilter(RegisterForm.gender))
async def process_gender(message: Message, state: FSMContext):
    gender_input = message.text.strip().lower()

    if gender_input in ["парень", "мужчина"]:
        gender = "Парень"
    elif gender_input in ["девушка", "женщина"]:
        gender = "Девушка"
    else:
        await message.answer("Пожалуйста, напиши 'парень' или 'девушка'.")
        return

    await state.update_data(gender=gender)
    await message.answer("Пришли своё фото.")
    await state.set_state(RegisterForm.photo)


@router.message(StateFilter(RegisterForm.photo), F.photo)
async def process_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    name = data["name"]
    age = data["age"]
    gender = data["gender"]

    await state.update_data(photo_id=photo_id)

    caption = f"<b>Новая анкета</b>\n\nИмя: {name}\nВозраст: {age}\nПол: {gender}\n\nОжидает подтверждения"

    if gender == "Девушка":
        await message.answer(
            f"🎥 Пожалуйста, запиши короткое видео (кружок), где говоришь своё имя и уникальный номер: <code>{message.from_user.id}</code>\n\n"
            "Отправь его менеджеру для подтверждения, что ты не фейк:\n👉 https://t.me/valeria_smm_manager"
        )
        await message.bot.send_photo(ADMIN_ID, photo=photo_id, caption=caption)
        await message.answer("Анкета отправлена администратору. Ожидайте подтверждения ✅")
        await state.clear()
        return

    # Для парней — запрос на оплату
    prices = [LabeledPrice(label="Доступ к анкете", amount=PRICE_RUB * 100)]

    if not PAYMENT_PROVIDER_TOKEN:
        await message.answer("⚠️ Ошибка: платежный токен не настроен. Обратитесь к администратору.")
        return

    # Отправка инвойса для оплаты
    await message.answer_invoice(
        title="Регистрация",
        description="Оплата за размещение анкеты в сервисе знакомств",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        payload="registration_payment"
    )

    await state.update_data(photo_id=photo_id)  # ❗Не сбрасываем state до оплаты!


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Не указано")
    age = data.get("age", "Не указано")
    gender = data.get("gender", "Парень")
    photo_id = data.get("photo_id")

    caption = f"<b>Новая анкета</b>\n\nИмя: {name}\nВозраст: {age}\nПол: {gender}\n\n✅ Оплата подтверждена"

    if photo_id:
        await message.bot.send_photo(ADMIN_ID, photo=photo_id, caption=caption)
    else:
        await message.bot.send_message(ADMIN_ID, caption)

    await message.answer("✅ Оплата прошла успешно! Ваша анкета отправлена на проверку.")
    await state.clear()

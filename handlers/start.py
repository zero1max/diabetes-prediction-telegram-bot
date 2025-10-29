from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from handlers.states import DiabetesForm
from loader import router_user
from diabet import predict_diabetes


@router_user.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! 👋\nKeling, sizning diabet xavfingizni baholaymiz.\n\nNecha marta homilador bo‘lgansiz (0 bo‘lishi ham mumkin)?")
    await state.set_state(DiabetesForm.waiting_pregnancies)

@router_user.message(DiabetesForm.waiting_pregnancies)
async def get_pregnancies(message: types.Message, state: FSMContext):
    await state.update_data(pregnancies=float(message.text)) # type: ignore
    await message.answer("Endi glyukoza darajasini kiriting:")
    await state.set_state(DiabetesForm.waiting_glucose)

@router_user.message(DiabetesForm.waiting_glucose)
async def get_glucose(message: types.Message, state: FSMContext):
    await state.update_data(glucose=float(message.text)) # type: ignore
    await message.answer("Qon bosimingizni kiriting:")
    await state.set_state(DiabetesForm.waiting_blood_pressure)

@router_user.message(DiabetesForm.waiting_blood_pressure)
async def get_bp(message: types.Message, state: FSMContext):
    await state.update_data(blood_pressure=float(message.text)) # type: ignore
    await message.answer("Teri qalinligini kiriting:")
    await state.set_state(DiabetesForm.waiting_skin_thickness)

@router_user.message(DiabetesForm.waiting_skin_thickness)
async def get_skin(message: types.Message, state: FSMContext):
    await state.update_data(skin_thickness=float(message.text)) # type: ignore
    await message.answer("Insulin miqdorini kiriting:")
    await state.set_state(DiabetesForm.waiting_insulin)

@router_user.message(DiabetesForm.waiting_insulin)
async def get_insulin(message: types.Message, state: FSMContext):
    await state.update_data(insulin=float(message.text)) # type: ignore
    await message.answer("BMI (Tana massasi indeksi) ni kiriting:")
    await state.set_state(DiabetesForm.waiting_bmi)

@router_user.message(DiabetesForm.waiting_bmi)
async def get_bmi(message: types.Message, state: FSMContext):
    await state.update_data(bmi=float(message.text)) # type: ignore
    await message.answer("DiabetesPedigreeFunction (irsiyat ko‘rsatkichi) ni kiriting:")
    await state.set_state(DiabetesForm.waiting_diabetes_pedigree)

@router_user.message(DiabetesForm.waiting_diabetes_pedigree)
async def get_dpf(message: types.Message, state: FSMContext):
    await state.update_data(dpf=float(message.text)) # type: ignore
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(DiabetesForm.waiting_age)

@router_user.message(DiabetesForm.waiting_age)
async def get_age(message: types.Message, state: FSMContext):
    """
    Foydalanuvchi yoshini qabul qilib, diabet bashoratini amalga oshiradi.
    
    Args:
        message (types.Message): Aiogramdan kelgan xabar obyekti
        state (FSMContext): Foydalanuvchi holati obyekti
        scaler: Ma'lumotlarni masshtablash uchun scaler obyekti
        model: Oldindan o'qitilgan model
    """
    # State'dan ma'lumotlarni olish
    data = await state.get_data()
    
    # Yoshni qo'shish
    data["age"] = float(message.text) # type: ignore
    
    # predict_diabetes funksiyasini chaqirish
    result, probability = predict_diabetes(
        data["pregnancies"], 
        data["glucose"], 
        data["blood_pressure"],
        data["skin_thickness"], 
        data["insulin"], 
        data["bmi"],
        data["dpf"], 
        data["age"]
    )
    
    # Natijaga qarab xabar tayyorlash
    if result == "Diabet bor":
        text = f"⚠️ Sizda diabet xavfi bor (ehtimollik: {probability}). Shifokorga murojaat qilish tavsiya etiladi."
    else:
        text = f"✅ Sizda diabet xavfi aniqlanmadi (ehtimollik: {probability})."
    
    # Xabarni yuborish
    await message.answer(text)
    
    # Holatni tozalash
    await state.clear()

from aiogram.fsm.state import State, StatesGroup

# State guruhlari yaratish
class DiabetesForm(StatesGroup):
    waiting_pregnancies = State()
    waiting_glucose = State()
    waiting_blood_pressure = State()
    waiting_skin_thickness = State()
    waiting_insulin = State()
    waiting_bmi = State()
    waiting_diabetes_pedigree = State()
    waiting_age = State()
    waiting_confirmation = State()
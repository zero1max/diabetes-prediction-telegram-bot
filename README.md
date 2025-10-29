# Diabetes Prediction Telegram Bot

A Telegram bot that estimates diabetes risk using a Logistic Regression model trained on the Pima Indians Diabetes dataset. Built with aiogram v3 and scikit-learn.

## Features
- Interactive chat flow (Uzbek) to collect health indicators
- ML-based prediction with probability score
- FSM-driven conversation using aiogram v3
- Simple training script to (re)train and persist the model

## Project Structure
```
.
├─ main.py                  # Bot entrypoint (polling)
├─ loader.py                # Bot/dispatcher/router setup and .env loading
├─ diabet.py                # Model training and predict function
├─ diabetes.csv             # Training dataset (Pima Indians Diabetes)
├─ handlers/
│  ├─ __init__.py
│  ├─ start.py             # Conversation flow and prediction
│  └─ states.py            # FSM states
├─ requirements.txt
└─ README.md
```

## Requirements
- Python 3.11+
- A Telegram Bot Token from @BotFather

## Quick Start
1) Clone and enter the project directory
```bash
git clone <your-repo-url>
cd diabetes-prediction-telegram-bot
```

2) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# or cmd
.venv\Scripts\activate.bat
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

4) Configure environment
Create a `.env` file in the project root:
```dotenv
TOKEN=1234567890:your_telegram_bot_token_here
```

5) Train the model (first time)
```bash
python diabet.py
```
This will train a Logistic Regression model and save `model.pkl` and `scaler.pkl` alongside the script.

6) Run the bot
```bash
python main.py
```
Open Telegram and start a chat with your bot. Send /start and follow the prompts.

## How It Works
- `handlers/start.py` collects inputs step-by-step using aiogram FSM (`handlers/states.py`).
- After the last input (age), it calls `predict_diabetes(...)` from `diabet.py`.
- `diabet.py` loads the dataset, scales features with `StandardScaler`, trains `LogisticRegression`, and exposes `predict_diabetes` that uses the fitted scaler and model to return:
  - A label: "Diabet bor" or "Diabet yo‘q"
  - A probability score (0..1) for the positive class

## Important Notes
- By default, importing `diabet.py` will fit the model using `diabetes.csv`. Running `python diabet.py` explicitly is recommended initially to confirm `model.pkl`/`scaler.pkl` are created.
- If you change `diabetes.csv`, run the training step again.
- The bot prompts are in Uzbek.

## Dataset
The project expects `diabetes.csv` in the project root with the following columns:
- Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome

This is the common Pima Indians Diabetes dataset format.

## Troubleshooting
- No response from bot: verify your `TOKEN` in `.env` and that the bot is not blocked.
- Import or aiogram errors: ensure Python 3.11+ and that dependencies are installed.
- Crash on import/train: check `diabetes.csv` is present and has the expected schema.

## Possible Improvements
- Persist and load `model.pkl`/`scaler.pkl` instead of training at import time.
- Add validation and range checks for user inputs.
- Containerize with Docker and add CI.
- Add webhooks deployment guide (instead of polling) for production.

## License
MIT (or your chosen license).

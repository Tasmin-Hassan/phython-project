
@echo off

echo Starting Tasmin AI...

py -m pip install -r requirements.txt

py -m streamlit run app.py

pause

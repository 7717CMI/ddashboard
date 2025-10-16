@echo off
echo Starting NextLoad Dashboard...
echo.
echo The dashboard will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard.
echo.
python -m streamlit run app.py --server.port 8501
pause

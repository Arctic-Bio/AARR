@echo off
echo ========================================
echo Advanced Aerodynamic Simulation System
echo Installation and Launch Script
echo ========================================
echo.

echo Installing required packages...
pip install PySide6>=6.5.0
pip install numpy>=1.21.0
pip install matplotlib>=3.5.0
pip install scipy>=1.7.0
pip install Pillow>=8.3.0
pip install pyqtgraph>=0.13.0

echo.
echo Installation complete!
echo.
echo Launching Aerodynamic Simulation System...
echo.

python main.py

pause
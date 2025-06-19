#!/usr/bin/env python3
"""
Advanced Aerodynamic Simulation System
A comprehensive air resistance and flow visualization tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import AerodynamicSimulationApp
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Aerodynamic Simulation System")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = AerodynamicSimulationApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
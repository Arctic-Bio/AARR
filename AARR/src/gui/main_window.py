"""
Main Application Window
Beautiful GUI for aerodynamic simulation system
"""

import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTabWidget, QSplitter, QGroupBox, QLabel, 
                               QPushButton, QSlider, QSpinBox, QDoubleSpinBox,
                               QComboBox, QTextEdit, QProgressBar, QCheckBox,
                               QGridLayout, QFrame, QScrollArea, QStatusBar)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QPainter, QBrush

import numpy as np
from typing import Dict, Optional
import pyqtgraph as pg

from ..physics.simulation import SimulationManager, SimulationParameters
from ..physics.aerodynamics import ObjectType
from .visualization import FlowVisualizationWidget
from .controls import SimulationControlPanel, ObjectConfigPanel, EnvironmentPanel
from .data_display import DataDisplayWidget, AnalysisWidget

class ModernStyle:
    """Modern dark theme styling"""
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply modern dark theme to application"""
        palette = QPalette()
        
        # Window colors
        palette.setColor(QPalette.Window, QColor(45, 45, 48))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        
        # Base colors
        palette.setColor(QPalette.Base, QColor(35, 35, 38))
        palette.setColor(QPalette.AlternateBase, QColor(60, 60, 63))
        
        # Text colors
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(53, 53, 57))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        
        # Highlight colors
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        app.setPalette(palette)
        
        # Set stylesheet for additional styling
        app.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d30;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #2d2d30;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2a82da;
            }
            QTabBar::tab:hover {
                background-color: #4a4a4a;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0e639c;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5a8a;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: #555;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2a82da;
                border: 1px solid #555;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #3a92ea;
            }
            QComboBox {
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px 8px;
                background-color: #3c3c3c;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            QSpinBox, QDoubleSpinBox {
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px;
                background-color: #3c3c3c;
                color: white;
            }
            TextEdit {
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #1e1e1e;
                color: white;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                background-color: #3c3c3c;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
                border-radius: 2px;
            }
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #555;
                background-color: #3c3c3c;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #2a82da;
                background-color: #2a82da;
                border-radius: 3px;
            }
            QStatusBar {
                background-color: #2d2d30;
                color: white;
                border-top: 1px solid #555;
            }
        """)

class SimulationThread(QThread):
    """Thread for running simulation without blocking GUI"""
    
    data_updated = Signal(dict)
    simulation_finished = Signal()
    
    def __init__(self, simulation_manager):
        super().__init__()
        self.sim_manager = simulation_manager
        self.running = False
        
    def run(self):
        """Run simulation in separate thread"""
        self.running = True
        while self.running and self.sim_manager.is_running:
            if not self.sim_manager.is_paused:
                if not self.sim_manager.step_simulation():
                    break
                
                # Emit data update signal
                data = self.sim_manager.get_current_data()
                self.data_updated.emit(data)
                
            self.msleep(1)  # Small delay
        
        self.simulation_finished.emit()
        self.running = False
    
    def stop(self):
        """Stop the simulation thread"""
        self.running = False
        self.wait()

class AerodynamicSimulationApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.simulation_manager = SimulationManager()
        self.simulation_thread = None
        self.update_timer = QTimer()
        
        self.init_ui()
        self.setup_connections()
        self.apply_styling()
        
        # Set default object
        self.simulation_manager.set_object_geometry(ObjectType.JET, 10.0, 2.0, 1.5)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Advanced Aerodynamic Simulation System AASS v1.1.Q-Q")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Left panel (controls)
        self.create_control_panel(main_splitter)
        
        # Right panel (visualization and data)
        self.create_visualization_panel(main_splitter)
        
        # Set splitter proportions
        main_splitter.setSizes([400, 1200])
        
        # Status bar
        self.create_status_bar()
        
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Control tabs
        control_tabs = QTabWidget()
        control_layout.addWidget(control_tabs)
        
        # Simulation controls
        self.sim_controls = SimulationControlPanel(self.simulation_manager)
        control_tabs.addTab(self.sim_controls, "Simulation")
        
        # Object configuration
        self.object_config = ObjectConfigPanel(self.simulation_manager)
        control_tabs.addTab(self.object_config, "Object")
        
        # Environment settings
        self.environment_panel = EnvironmentPanel(self.simulation_manager)
        control_tabs.addTab(self.environment_panel, "Environment")
        
        parent.addWidget(control_widget)
        
    def create_visualization_panel(self, parent):
        """Create the visualization panel"""
        viz_widget = QWidget()
        viz_layout = QVBoxLayout(viz_widget)
        
        # Visualization tabs
        viz_tabs = QTabWidget()
        viz_layout.addWidget(viz_tabs)
        
        # Flow visualization
        self.flow_viz = FlowVisualizationWidget()
        viz_tabs.addTab(self.flow_viz, "Flow Visualization")
        
        # Data display
        self.data_display = DataDisplayWidget()
        viz_tabs.addTab(self.data_display, "Live Data")
        
        # Analysis
        self.analysis_widget = AnalysisWidget()
        viz_tabs.addTab(self.analysis_widget, "Analysis")
        
        parent.addWidget(viz_widget)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.sim_status_label = QLabel("Ready")
        self.time_label = QLabel("Time: 0.00s")
        self.fps_label = QLabel("FPS: 0")
        
        self.status_bar.addWidget(self.sim_status_label)
        self.status_bar.addPermanentWidget(self.time_label)
        self.status_bar.addPermanentWidget(self.fps_label)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Simulation controls
        self.sim_controls.start_requested.connect(self.start_simulation)
        self.sim_controls.pause_requested.connect(self.pause_simulation)
        self.sim_controls.stop_requested.connect(self.stop_simulation)
        self.sim_controls.reset_requested.connect(self.reset_simulation)
        
        # Object configuration
        self.object_config.geometry_changed.connect(self.update_object_geometry)
        
        # Environment settings
        self.environment_panel.parameters_changed.connect(self.update_simulation_parameters)
        
        # Update timer
        self.update_timer.timeout.connect(self.update_displays)
        self.update_timer.start(50)  # 20 FPS update rate
        
    def apply_styling(self):
        """Apply modern styling to the application"""
        ModernStyle.apply_dark_theme(self.parent() if self.parent() else self)
        
        # Set fonts
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
    def start_simulation(self):
        """Start the simulation"""
        if self.simulation_thread and self.simulation_thread.isRunning():
            return
            
        self.simulation_manager.reset_simulation()
        self.simulation_manager.is_running = True
        
        # Create and start simulation thread
        self.simulation_thread = SimulationThread(self.simulation_manager)
        self.simulation_thread.data_updated.connect(self.on_simulation_data_updated)
        self.simulation_thread.simulation_finished.connect(self.on_simulation_finished)
        self.simulation_thread.start()
        
        self.sim_status_label.setText("Running")
        self.sim_controls.set_running_state(True)
        
    def pause_simulation(self):
        """Pause/resume the simulation"""
        if self.simulation_manager.is_paused:
            self.simulation_manager.resume_simulation()
            self.sim_status_label.setText("Running")
        else:
            self.simulation_manager.pause_simulation()
            self.sim_status_label.setText("Paused")
            
    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_manager.stop_simulation()
        
        if self.simulation_thread:
            self.simulation_thread.stop()
            self.simulation_thread = None
            
        self.sim_status_label.setText("Stopped")
        self.sim_controls.set_running_state(False)
        
        # Force update displays to show final data
        self.update_displays()
        
    def reset_simulation(self):
        """Reset the simulation"""
        self.stop_simulation()
        self.simulation_manager.reset_simulation()
        
        # Clear displays
        self.flow_viz.clear()
        # Removed: self.data_plots.clear()
        self.data_display.clear()
        self.analysis_widget.clear()
        
        self.sim_status_label.setText("Ready")
        self.time_label.setText("Time: 0.00s")
        
    def update_object_geometry(self, obj_type, length, width, height):
        """Update object geometry"""
        self.simulation_manager.set_object_geometry(obj_type, length, width, height)
        
    def update_simulation_parameters(self, params):
        """Update simulation parameters"""
        self.simulation_manager.set_parameters(**params)
        
    def on_simulation_data_updated(self, data):
        """Handle simulation data updates"""
        # This will be called from the simulation thread
        pass
        
    def on_simulation_finished(self):
        """Handle simulation completion"""
        self.sim_status_label.setText("Completed")
        self.sim_controls.set_running_state(False)
        
    def update_displays(self):
        """Update all display widgets"""
        # Removed: self.data_plots.update_data(self.simulation_manager.results)
        
        # Check if we have simulation data
        if not hasattr(self.simulation_manager.results, 'time_history') or not self.simulation_manager.results.time_history:
            return
            
        # Get current data
        current_data = self.simulation_manager.results.get_latest_data()
        
        if current_data:
            # Update time display
            self.time_label.setText(f"Time: {current_data.get('time', 0):.2f}s")
            
            # Update visualization widgets
            self.flow_viz.update_data(current_data)
            self.data_display.update_data(current_data)
            
            # Update analysis (less frequently)
            if len(self.simulation_manager.results.time_history) % 20 == 0:
                analysis_data = self.simulation_manager.get_analysis_data()
                self.analysis_widget.update_data(analysis_data)
                
    def closeEvent(self, event):
        """Handle application close"""
        self.stop_simulation()
        event.accept()
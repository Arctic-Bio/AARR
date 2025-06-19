"""
Data Display Widgets for Real-time and Analysis Data
"""

import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QTextEdit, QGroupBox, QScrollArea,
                               QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
                               QHeaderView, QProgressBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPalette
import json

class DataDisplayWidget(QWidget):
    """Widget for displaying real-time simulation data"""
    
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Create scroll area for data
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Current state group
        self.create_current_state_group(scroll_layout)
        
        # Forces group
        self.create_forces_group(scroll_layout)
        
        # Coefficients group
        self.create_coefficients_group(scroll_layout)
        
        # Flow properties group
        self.create_flow_properties_group(scroll_layout)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
    def create_current_state_group(self, parent_layout):
        """Create current state display group"""
        group = QGroupBox("Current State")
        layout = QGridLayout(group)
        
        # Time
        layout.addWidget(QLabel("Time:"), 0, 0)
        self.time_label = QLabel("0.00 s")
        self.time_label.setStyleSheet("color: #2a82da; font-weight: bold;")
        layout.addWidget(self.time_label, 0, 1)
        
        # Position
        layout.addWidget(QLabel("Position (m):"), 1, 0)
        self.position_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.position_label, 1, 1)
        
        # Velocity
        layout.addWidget(QLabel("Velocity (m/s):"), 2, 0)
        self.velocity_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.velocity_label, 2, 1)
        
        # Speed
        layout.addWidget(QLabel("Speed (m/s):"), 3, 0)
        self.speed_label = QLabel("0.00")
        self.speed_label.setStyleSheet("color: #2a82da; font-weight: bold;")
        layout.addWidget(self.speed_label, 3, 1)
        
        # Acceleration
        layout.addWidget(QLabel("Acceleration (m/s²):"), 4, 0)
        self.acceleration_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.acceleration_label, 4, 1)
        
        parent_layout.addWidget(group)
        
    def create_forces_group(self, parent_layout):
        """Create forces display group"""
        group = QGroupBox("Forces")
        layout = QGridLayout(group)
        
        # Drag force
        layout.addWidget(QLabel("Drag Force (N):"), 0, 0)
        self.drag_force_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.drag_force_label, 0, 1)
        
        layout.addWidget(QLabel("Drag Magnitude (N):"), 1, 0)
        self.drag_mag_label = QLabel("0.00")
        self.drag_mag_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        layout.addWidget(self.drag_mag_label, 1, 1)
        
        # Lift force
        layout.addWidget(QLabel("Lift Force (N):"), 2, 0)
        self.lift_force_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.lift_force_label, 2, 1)
        
        layout.addWidget(QLabel("Lift Magnitude (N):"), 3, 0)
        self.lift_mag_label = QLabel("0.00")
        self.lift_mag_label.setStyleSheet("color: #4ecdc4; font-weight: bold;")
        layout.addWidget(self.lift_mag_label, 3, 1)
        
        # Total force
        layout.addWidget(QLabel("Total Force (N):"), 4, 0)
        self.total_force_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.total_force_label, 4, 1)
        
        layout.addWidget(QLabel("Total Magnitude (N):"), 5, 0)
        self.total_mag_label = QLabel("0.00")
        self.total_mag_label.setStyleSheet("color: #ffe66d; font-weight: bold;")
        layout.addWidget(self.total_mag_label, 5, 1)
        
        parent_layout.addWidget(group)
        
    def create_coefficients_group(self, parent_layout):
        """Create coefficients display group"""
        group = QGroupBox("Aerodynamic Coefficients")
        layout = QGridLayout(group)
        
        # Drag coefficient
        layout.addWidget(QLabel("Drag Coefficient (Cd):"), 0, 0)
        self.cd_label = QLabel("0.000")
        self.cd_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        layout.addWidget(self.cd_label, 0, 1)
        
        # Lift coefficient
        layout.addWidget(QLabel("Lift Coefficient (Cl):"), 1, 0)
        self.cl_label = QLabel("0.000")
        self.cl_label.setStyleSheet("color: #4ecdc4; font-weight: bold;")
        layout.addWidget(self.cl_label, 1, 1)
        
        # Lift-to-drag ratio
        layout.addWidget(QLabel("L/D Ratio:"), 2, 0)
        self.ld_ratio_label = QLabel("0.00")
        self.ld_ratio_label.setStyleSheet("color: #2a82da; font-weight: bold;")
        layout.addWidget(self.ld_ratio_label, 2, 1)
        
        # Reynolds number
        layout.addWidget(QLabel("Reynolds Number:"), 3, 0)
        self.reynolds_label = QLabel("0")
        layout.addWidget(self.reynolds_label, 3, 1)
        
        # Mach number
        layout.addWidget(QLabel("Mach Number:"), 4, 0)
        self.mach_label = QLabel("0.000")
        layout.addWidget(self.mach_label, 4, 1)
        
        parent_layout.addWidget(group)
        
    def create_flow_properties_group(self, parent_layout):
        """Create flow properties display group"""
        group = QGroupBox("Flow Properties")
        layout = QGridLayout(group)
        
        # Dynamic pressure
        layout.addWidget(QLabel("Dynamic Pressure (Pa):"), 0, 0)
        self.dynamic_pressure_label = QLabel("0.00")
        layout.addWidget(self.dynamic_pressure_label, 0, 1)
        
        # Relative velocity
        layout.addWidget(QLabel("Relative Velocity (m/s):"), 1, 0)
        self.rel_velocity_label = QLabel("(0.00, 0.00, 0.00)")
        layout.addWidget(self.rel_velocity_label, 1, 1)
        
        # Relative speed
        layout.addWidget(QLabel("Relative Speed (m/s):"), 2, 0)
        self.rel_speed_label = QLabel("0.00")
        self.rel_speed_label.setStyleSheet("color: #2a82da; font-weight: bold;")
        layout.addWidget(self.rel_speed_label, 2, 1)
        
        # Angle of attack
        layout.addWidget(QLabel("Angle of Attack (°):"), 3, 0)
        self.aoa_label = QLabel("0.0")
        layout.addWidget(self.aoa_label, 3, 1)
        
        parent_layout.addWidget(group)
        
    def update_data(self, data):
        """Update display with new data"""
        self.current_data = data
        
        if not data:
            return
            
        # Update current state
        self.time_label.setText(f"{data.get('time', 0):.2f} s")
        
        if 'position' in data:
            pos = data['position']
            self.position_label.setText(f"({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
            
        if 'velocity' in data:
            vel = data['velocity']
            self.velocity_label.setText(f"({vel[0]:.2f}, {vel[1]:.2f}, {vel[2]:.2f})")
            speed = np.linalg.norm(vel)
            self.speed_label.setText(f"{speed:.2f}")
            
        if 'acceleration' in data:
            acc = data['acceleration']
            self.acceleration_label.setText(f"({acc[0]:.2f}, {acc[1]:.2f}, {acc[2]:.2f})")
            
        # Update forces
        if 'forces' in data:
            forces = data['forces']
            
            if 'drag' in forces:
                drag = forces['drag']
                self.drag_force_label.setText(f"({drag[0]:.2f}, {drag[1]:.2f}, {drag[2]:.2f})")
                drag_mag = np.linalg.norm(drag)
                self.drag_mag_label.setText(f"{drag_mag:.2f}")
                
            if 'lift' in forces:
                lift = forces['lift']
                self.lift_force_label.setText(f"({lift[0]:.2f}, {lift[1]:.2f}, {lift[2]:.2f})")
                lift_mag = np.linalg.norm(lift)
                self.lift_mag_label.setText(f"{lift_mag:.2f}")
                
            if 'total' in forces:
                total = forces['total']
                self.total_force_label.setText(f"({total[0]:.2f}, {total[1]:.2f}, {total[2]:.2f})")
                total_mag = np.linalg.norm(total)
                self.total_mag_label.setText(f"{total_mag:.2f}")
                
            # Update coefficients
            if 'coefficients' in forces:
                coeffs = forces['coefficients']
                
                cd = coeffs.get('cd', 0)
                self.cd_label.setText(f"{cd:.3f}")
                
                cl = coeffs.get('cl', 0)
                self.cl_label.setText(f"{cl:.3f}")
                
                # L/D ratio
                if cd > 1e-6:
                    ld_ratio = cl / cd
                    self.ld_ratio_label.setText(f"{ld_ratio:.2f}")
                else:
                    self.ld_ratio_label.setText("∞")
                    
                reynolds = coeffs.get('reynolds', 0)
                self.reynolds_label.setText(f"{reynolds:.0f}")
                
                mach = coeffs.get('mach', 0)
                self.mach_label.setText(f"{mach:.3f}")
                
        # Update flow properties
        if 'velocity' in data:
            vel = data['velocity']
            speed = np.linalg.norm(vel)
            
            # Dynamic pressure (assuming air density = 1.225 kg/m³)
            dynamic_pressure = 0.5 * 1.225 * speed**2
            self.dynamic_pressure_label.setText(f"{dynamic_pressure:.2f}")
            
            # For now, assume relative velocity equals velocity
            self.rel_velocity_label.setText(f"({vel[0]:.2f}, {vel[1]:.2f}, {vel[2]:.2f})")
            self.rel_speed_label.setText(f"{speed:.2f}")
            
    def clear(self):
        """Clear all data displays"""
        self.time_label.setText("0.00 s")
        self.position_label.setText("(0.00, 0.00, 0.00)")
        self.velocity_label.setText("(0.00, 0.00, 0.00)")
        self.speed_label.setText("0.00")
        self.acceleration_label.setText("(0.00, 0.00, 0.00)")
        
        self.drag_force_label.setText("(0.00, 0.00, 0.00)")
        self.drag_mag_label.setText("0.00")
        self.lift_force_label.setText("(0.00, 0.00, 0.00)")
        self.lift_mag_label.setText("0.00")
        self.total_force_label.setText("(0.00, 0.00, 0.00)")
        self.total_mag_label.setText("0.00")
        
        self.cd_label.setText("0.000")
        self.cl_label.setText("0.000")
        self.ld_ratio_label.setText("0.00")
        self.reynolds_label.setText("0")
        self.mach_label.setText("0.000")
        
        self.dynamic_pressure_label.setText("0.00")
        self.rel_velocity_label.setText("(0.00, 0.00, 0.00)")
        self.rel_speed_label.setText("0.00")
        self.aoa_label.setText("0.0")

class AnalysisWidget(QWidget):
    """Widget for displaying comprehensive analysis data"""
    
    def __init__(self):
        super().__init__()
        self.analysis_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Create tabs for different analysis categories
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Statistics tab
        self.create_statistics_tab(tabs)
        
        # Performance tab
        self.create_performance_tab(tabs)
        
        # Efficiency tab
        self.create_efficiency_tab(tabs)
        
        # Raw data tab
        self.create_raw_data_tab(tabs)
        
    def create_statistics_tab(self, parent):
        """Create statistics analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Time statistics
        time_group = QGroupBox("Time Statistics")
        time_layout = QGridLayout(time_group)
        
        time_layout.addWidget(QLabel("Total Simulation Time:"), 0, 0)
        self.total_time_label = QLabel("0.00 s")
        time_layout.addWidget(self.total_time_label, 0, 1)
        
        time_layout.addWidget(QLabel("Time Steps:"), 1, 0)
        self.time_steps_label = QLabel("0")
        time_layout.addWidget(self.time_steps_label, 1, 1)
        
        time_layout.addWidget(QLabel("Time Step Size:"), 2, 0)
        self.dt_label = QLabel("0.000 s")
        time_layout.addWidget(self.dt_label, 2, 1)
        
        layout.addWidget(time_group)
        
        # Motion statistics
        motion_group = QGroupBox("Motion Statistics")
        motion_layout = QGridLayout(motion_group)
        
        motion_layout.addWidget(QLabel("Maximum Speed:"), 0, 0)
        self.max_speed_label = QLabel("0.00 m/s")
        motion_layout.addWidget(self.max_speed_label, 0, 1)
        
        motion_layout.addWidget(QLabel("Average Speed:"), 1, 0)
        self.avg_speed_label = QLabel("0.00 m/s")
        motion_layout.addWidget(self.avg_speed_label, 1, 1)
        
        motion_layout.addWidget(QLabel("Final Speed:"), 2, 0)
        self.final_speed_label = QLabel("0.00 m/s")
        motion_layout.addWidget(self.final_speed_label, 2, 1)
        
        motion_layout.addWidget(QLabel("Maximum Displacement:"), 3, 0)
        self.max_displacement_label = QLabel("(0.00, 0.00, 0.00) m")
        motion_layout.addWidget(self.max_displacement_label, 3, 1)
        
        layout.addWidget(motion_group)
        layout.addStretch()
        
        parent.addTab(widget, "Statistics")
        
    def create_performance_tab(self, parent):
        """Create performance analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Force statistics
        force_group = QGroupBox("Force Statistics")
        force_layout = QGridLayout(force_group)
        
        force_layout.addWidget(QLabel("Maximum Drag:"), 0, 0)
        self.max_drag_label = QLabel("0.00 N")
        force_layout.addWidget(self.max_drag_label, 0, 1)
        
        force_layout.addWidget(QLabel("Average Drag:"), 1, 0)
        self.avg_drag_label = QLabel("0.00 N")
        force_layout.addWidget(self.avg_drag_label, 1, 1)
        
        force_layout.addWidget(QLabel("Maximum Lift:"), 2, 0)
        self.max_lift_label = QLabel("0.00 N")
        force_layout.addWidget(self.max_lift_label, 2, 1)
        
        force_layout.addWidget(QLabel("Average Lift:"), 3, 0)
        self.avg_lift_label = QLabel("0.00 N")
        force_layout.addWidget(self.avg_lift_label, 3, 1)
        
        layout.addWidget(force_group)
        
        # Energy statistics
        energy_group = QGroupBox("Energy Statistics")
        energy_layout = QGridLayout(energy_group)
        
        energy_layout.addWidget(QLabel("Initial Kinetic Energy:"), 0, 0)
        self.initial_ke_label = QLabel("0.00 J/kg")
        energy_layout.addWidget(self.initial_ke_label, 0, 1)
        
        energy_layout.addWidget(QLabel("Final Kinetic Energy:"), 1, 0)
        self.final_ke_label = QLabel("0.00 J/kg")
        energy_layout.addWidget(self.final_ke_label, 1, 1)
        
        energy_layout.addWidget(QLabel("Energy Loss:"), 2, 0)
        self.energy_loss_label = QLabel("0.00 J/kg")
        energy_layout.addWidget(self.energy_loss_label, 2, 1)
        
        # Progress bar for energy loss
        energy_layout.addWidget(QLabel("Energy Loss %:"), 3, 0)
        self.energy_loss_bar = QProgressBar()
        self.energy_loss_bar.setRange(0, 100)
        energy_layout.addWidget(self.energy_loss_bar, 3, 1)
        
        layout.addWidget(energy_group)
        layout.addStretch()
        
        parent.addTab(widget, "Performance")
        
    def create_efficiency_tab(self, parent):
        """Create efficiency analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Aerodynamic efficiency
        aero_group = QGroupBox("Aerodynamic Efficiency")
        aero_layout = QGridLayout(aero_group)
        
        aero_layout.addWidget(QLabel("Lift-to-Drag Ratio:"), 0, 0)
        self.ld_ratio_eff_label = QLabel("0.00")
        aero_layout.addWidget(self.ld_ratio_eff_label, 0, 1)
        
        aero_layout.addWidget(QLabel("Drag Area:"), 1, 0)
        self.drag_area_label = QLabel("0.00 m²")
        aero_layout.addWidget(self.drag_area_label, 1, 1)
        
        aero_layout.addWidget(QLabel("Fineness Ratio:"), 2, 0)
        self.fineness_ratio_label = QLabel("0.00")
        aero_layout.addWidget(self.fineness_ratio_label, 2, 1)
        
        aero_layout.addWidget(QLabel("Drag Coefficient:"), 3, 0)
        self.cd_eff_label = QLabel("0.000")
        aero_layout.addWidget(self.cd_eff_label, 3, 1)
        
        aero_layout.addWidget(QLabel("Lift Coefficient:"), 4, 0)
        self.cl_eff_label = QLabel("0.000")
        aero_layout.addWidget(self.cl_eff_label, 4, 1)
        
        layout.addWidget(aero_group)
        
        # Efficiency ratings
        rating_group = QGroupBox("Efficiency Ratings")
        rating_layout = QVBoxLayout(rating_group)
        
        # Overall efficiency bar
        rating_layout.addWidget(QLabel("Overall Aerodynamic Efficiency:"))
        self.overall_efficiency_bar = QProgressBar()
        self.overall_efficiency_bar.setRange(0, 100)
        rating_layout.addWidget(self.overall_efficiency_bar)
        
        # Streamlining efficiency
        rating_layout.addWidget(QLabel("Streamlining Efficiency:"))
        self.streamlining_bar = QProgressBar()
        self.streamlining_bar.setRange(0, 100)
        rating_layout.addWidget(self.streamlining_bar)
        
        layout.addWidget(rating_group)
        layout.addStretch()
        
        parent.addTab(widget, "Efficiency")
        
    def create_raw_data_tab(self, parent):
        """Create raw data display tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Text area for raw data
        self.raw_data_text = QTextEdit()
        self.raw_data_text.setReadOnly(True)
        self.raw_data_text.setFont(QFont("Consolas", 9))
        layout.addWidget(self.raw_data_text)
        
        parent.addTab(widget, "Raw Data")
        
    def update_data(self, analysis_data):
        """Update analysis display with new data"""
        self.analysis_data = analysis_data
        
        if not analysis_data:
            return
            
        # Update statistics
        time_stats = analysis_data.get('time_stats', {})
        self.total_time_label.setText(f"{time_stats.get('total_time', 0):.2f} s")
        self.time_steps_label.setText(f"{time_stats.get('time_steps', 0)}")
        self.dt_label.setText(f"{time_stats.get('dt', 0):.3f} s")
        
        motion_stats = analysis_data.get('motion_stats', {})
        self.max_speed_label.setText(f"{motion_stats.get('max_speed', 0):.2f} m/s")
        self.avg_speed_label.setText(f"{motion_stats.get('avg_speed', 0):.2f} m/s")
        self.final_speed_label.setText(f"{motion_stats.get('final_speed', 0):.2f} m/s")
        
        max_pos = motion_stats.get('max_position', [0, 0, 0])
        self.max_displacement_label.setText(f"({max_pos[0]:.2f}, {max_pos[1]:.2f}, {max_pos[2]:.2f}) m")
        
        # Update performance
        force_stats = analysis_data.get('force_stats', {})
        self.max_drag_label.setText(f"{force_stats.get('max_drag', 0):.2f} N")
        self.avg_drag_label.setText(f"{force_stats.get('avg_drag', 0):.2f} N")
        self.max_lift_label.setText(f"{force_stats.get('max_lift', 0):.2f} N")
        self.avg_lift_label.setText(f"{force_stats.get('avg_lift', 0):.2f} N")
        
        energy_stats = analysis_data.get('energy_stats', {})
        self.initial_ke_label.setText(f"{energy_stats.get('initial_ke', 0):.2f} J/kg")
        self.final_ke_label.setText(f"{energy_stats.get('final_ke', 0):.2f} J/kg")
        self.energy_loss_label.setText(f"{energy_stats.get('energy_loss', 0):.2f} J/kg")
        
        # Energy loss percentage
        initial_ke = energy_stats.get('initial_ke', 0)
        if initial_ke > 0:
            energy_loss_pct = (energy_stats.get('energy_loss', 0) / initial_ke) * 100
            self.energy_loss_bar.setValue(int(min(energy_loss_pct, 100)))
        
        # Update efficiency
        eff_stats = analysis_data.get('efficiency_stats', {})
        self.ld_ratio_eff_label.setText(f"{eff_stats.get('lift_to_drag_ratio', 0):.2f}")
        self.drag_area_label.setText(f"{eff_stats.get('drag_area', 0):.2f} m²")
        self.fineness_ratio_label.setText(f"{eff_stats.get('fineness_ratio', 0):.2f}")
        self.cd_eff_label.setText(f"{eff_stats.get('drag_coefficient', 0):.3f}")
        self.cl_eff_label.setText(f"{eff_stats.get('lift_coefficient', 0):.3f}")
        
        # Calculate efficiency ratings
        cd = eff_stats.get('drag_coefficient', 1)
        ld_ratio = eff_stats.get('lift_to_drag_ratio', 0)
        fineness = eff_stats.get('fineness_ratio', 1)
        
        # Overall efficiency (simplified calculation)
        overall_eff = min(100, max(0, (1 / max(cd, 0.01)) * 10))
        self.overall_efficiency_bar.setValue(int(overall_eff))
        
        # Streamlining efficiency
        streamlining_eff = min(100, max(0, fineness * 10))
        self.streamlining_bar.setValue(int(streamlining_eff))
        
        # Update raw data
        self.raw_data_text.setPlainText(json.dumps(analysis_data, indent=2, default=str))
        
    def clear(self):
        """Clear all analysis displays"""
        # Reset all labels to default values
        self.total_time_label.setText("0.00 s")
        self.time_steps_label.setText("0")
        self.dt_label.setText("0.000 s")
        
        self.max_speed_label.setText("0.00 m/s")
        self.avg_speed_label.setText("0.00 m/s")
        self.final_speed_label.setText("0.00 m/s")
        self.max_displacement_label.setText("(0.00, 0.00, 0.00) m")
        
        self.max_drag_label.setText("0.00 N")
        self.avg_drag_label.setText("0.00 N")
        self.max_lift_label.setText("0.00 N")
        self.avg_lift_label.setText("0.00 N")
        
        self.initial_ke_label.setText("0.00 J/kg")
        self.final_ke_label.setText("0.00 J/kg")
        self.energy_loss_label.setText("0.00 J/kg")
        self.energy_loss_bar.setValue(0)
        
        self.ld_ratio_eff_label.setText("0.00")
        self.drag_area_label.setText("0.00 m²")
        self.fineness_ratio_label.setText("0.00")
        self.cd_eff_label.setText("0.000")
        self.cl_eff_label.setText("0.000")
        
        self.overall_efficiency_bar.setValue(0)
        self.streamlining_bar.setValue(0)
        
        self.raw_data_text.clear()
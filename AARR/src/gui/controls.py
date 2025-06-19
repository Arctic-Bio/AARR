"""
Control Panels for Simulation Configuration
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QLabel, QPushButton, QSlider, QSpinBox, 
                               QDoubleSpinBox, QComboBox, QCheckBox, QGridLayout,
                               QMessageBox)
from PySide6.QtCore import Qt, Signal
import numpy as np

from ..physics.aerodynamics import ObjectType
from .geometry_dialog import GeometryImportDialog

class SimulationControlPanel(QWidget):
    """Control panel for simulation start/stop/pause"""
    
    start_requested = Signal()
    pause_requested = Signal()
    stop_requested = Signal()
    reset_requested = Signal()
    
    def __init__(self, simulation_manager):
        super().__init__()
        self.sim_manager = simulation_manager
        self.is_running = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Control buttons group
        control_group = QGroupBox("Simulation Control")
        control_layout = QVBoxLayout(control_group)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        self.reset_btn = QPushButton("Reset")
        
        self.start_btn.clicked.connect(self.start_requested.emit)
        self.pause_btn.clicked.connect(self.pause_requested.emit)
        self.stop_btn.clicked.connect(self.stop_requested.emit)
        self.reset_btn.clicked.connect(self.reset_requested.emit)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.reset_btn)
        
        control_layout.addLayout(button_layout)
        
        # Time control
        time_group = QGroupBox("Time Settings")
        time_layout = QGridLayout(time_group)
        
        time_layout.addWidget(QLabel("Max Time (s):"), 0, 0)
        self.max_time_spin = QDoubleSpinBox()
        self.max_time_spin.setRange(0.1, 100.0)
        self.max_time_spin.setValue(10.0)
        self.max_time_spin.setSingleStep(0.5)
        time_layout.addWidget(self.max_time_spin, 0, 1)
        
        time_layout.addWidget(QLabel("Time Step (s):"), 1, 0)
        self.dt_spin = QDoubleSpinBox()
        self.dt_spin.setRange(0.0001, 0.1)
        self.dt_spin.setValue(0.001)
        self.dt_spin.setSingleStep(0.0001)
        self.dt_spin.setDecimals(4)
        time_layout.addWidget(self.dt_spin, 1, 1)
        
        # Initial state
        initial_group = QGroupBox("Initial Conditions")
        initial_layout = QGridLayout(initial_group)
        
        initial_layout.addWidget(QLabel("Initial Velocity X (m/s):"), 0, 0)
        self.init_vel_x = QDoubleSpinBox()
        self.init_vel_x.setRange(-100, 100)
        self.init_vel_x.setValue(0)
        initial_layout.addWidget(self.init_vel_x, 0, 1)
        
        initial_layout.addWidget(QLabel("Initial Velocity Y (m/s):"), 1, 0)
        self.init_vel_y = QDoubleSpinBox()
        self.init_vel_y.setRange(-100, 100)
        self.init_vel_y.setValue(0)
        initial_layout.addWidget(self.init_vel_y, 1, 1)
        
        initial_layout.addWidget(QLabel("Initial Velocity Z (m/s):"), 2, 0)
        self.init_vel_z = QDoubleSpinBox()
        self.init_vel_z.setRange(-100, 100)
        self.init_vel_z.setValue(0)
        initial_layout.addWidget(self.init_vel_z, 2, 1)
        
        layout.addWidget(control_group)
        layout.addWidget(time_group)
        layout.addWidget(initial_group)
        layout.addStretch()
        
        # Set initial button states
        self.set_running_state(False)
        
    def set_running_state(self, running):
        """Update button states based on simulation state"""
        self.is_running = running
        self.start_btn.setEnabled(not running)
        self.pause_btn.setEnabled(running)
        self.stop_btn.setEnabled(running)
        self.reset_btn.setEnabled(not running)

class ObjectConfigPanel(QWidget):
    """Panel for configuring object properties"""
    
    geometry_changed = Signal(object, float, float, float)  # obj_type, length, width, height
    
    def __init__(self, simulation_manager):
        super().__init__()
        self.sim_manager = simulation_manager
        self.imported_mesh = None
        self.mesh_properties = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Object type selection
        type_group = QGroupBox("Object Type")
        type_layout = QVBoxLayout(type_group)
        
        self.object_type_combo = QComboBox()
        self.object_type_combo.addItems([
            "Jet Aircraft",
            "Sphere",
            "Cylinder", 
            "Cube",
            "Airfoil",
            "Custom",
            "Import 3D Mesh"
        ])
        self.object_type_combo.currentTextChanged.connect(self.on_object_type_changed)
        type_layout.addWidget(self.object_type_combo)
        
        # Import geometry button
        self.import_btn = QPushButton("Import 3D Geometry...")
        self.import_btn.clicked.connect(self.import_geometry)
        self.import_btn.setEnabled(False)
        type_layout.addWidget(self.import_btn)
        
        # Geometry settings
        geometry_group = QGroupBox("Geometry")
        geometry_layout = QGridLayout(geometry_group)
        
        geometry_layout.addWidget(QLabel("Length (m):"), 0, 0)
        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.1, 100.0)
        self.length_spin.setValue(10.0)
        self.length_spin.setSingleStep(0.1)
        self.length_spin.valueChanged.connect(self.on_geometry_changed)
        geometry_layout.addWidget(self.length_spin, 0, 1)
        
        geometry_layout.addWidget(QLabel("Width (m):"), 1, 0)
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.1, 50.0)
        self.width_spin.setValue(2.0)
        self.width_spin.setSingleStep(0.1)
        self.width_spin.valueChanged.connect(self.on_geometry_changed)
        geometry_layout.addWidget(self.width_spin, 1, 1)
        
        geometry_layout.addWidget(QLabel("Height (m):"), 2, 0)
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0.1, 50.0)
        self.height_spin.setValue(1.5)
        self.height_spin.setSingleStep(0.1)
        self.height_spin.valueChanged.connect(self.on_geometry_changed)
        geometry_layout.addWidget(self.height_spin, 2, 1)
        
        # Orientation
        orientation_group = QGroupBox("Orientation")
        orientation_layout = QGridLayout(orientation_group)
        
        orientation_layout.addWidget(QLabel("Angle of Attack (°):"), 0, 0)
        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setRange(-45, 45)
        self.angle_slider.setValue(0)
        self.angle_slider.setTickPosition(QSlider.TicksBelow)
        self.angle_slider.setTickInterval(15)
        self.angle_slider.valueChanged.connect(self.on_angle_changed)
        orientation_layout.addWidget(self.angle_slider, 0, 1)
        
        self.angle_label = QLabel("0°")
        orientation_layout.addWidget(self.angle_label, 0, 2)
        
        # Material properties
        material_group = QGroupBox("Material Properties")
        material_layout = QGridLayout(material_group)
        
        material_layout.addWidget(QLabel("Mass (kg):"), 0, 0)
        self.mass_spin = QDoubleSpinBox()
        self.mass_spin.setRange(0.1, 10000.0)
        self.mass_spin.setValue(1000.0)
        self.mass_spin.setSingleStep(10.0)
        material_layout.addWidget(self.mass_spin, 0, 1)
        
        material_layout.addWidget(QLabel("Surface Roughness:"), 1, 0)
        self.roughness_combo = QComboBox()
        self.roughness_combo.addItems(["Smooth", "Slightly Rough", "Rough", "Very Rough"])
        material_layout.addWidget(self.roughness_combo, 1, 1)
        
        layout.addWidget(type_group)
        layout.addWidget(geometry_group)
        layout.addWidget(orientation_group)
        layout.addWidget(material_group)
        layout.addStretch()
        
    def on_object_type_changed(self, text):
        """Handle object type change"""
        # Enable/disable import button
        self.import_btn.setEnabled(text == "Import 3D Mesh")
        
        # Set default dimensions based on object type
        if text == "Jet Aircraft":
            self.length_spin.setValue(10.0)
            self.width_spin.setValue(2.0)
            self.height_spin.setValue(1.5)
        elif text == "Sphere":
            diameter = 2.0
            self.length_spin.setValue(diameter)
            self.width_spin.setValue(diameter)
            self.height_spin.setValue(diameter)
        elif text == "Cylinder":
            self.length_spin.setValue(5.0)
            self.width_spin.setValue(1.0)
            self.height_spin.setValue(1.0)
        elif text == "Cube":
            side = 2.0
            self.length_spin.setValue(side)
            self.width_spin.setValue(side)
            self.height_spin.setValue(side)
        elif text == "Airfoil":
            self.length_spin.setValue(3.0)
            self.width_spin.setValue(0.3)
            self.height_spin.setValue(0.1)
        elif text == "Import 3D Mesh":
            # Don't change dimensions automatically for imported meshes
            return
            
        self.on_geometry_changed()
        
    def on_geometry_changed(self):
        """Handle geometry change"""
        obj_type_map = {
            "Jet Aircraft": ObjectType.JET,
            "Sphere": ObjectType.SPHERE,
            "Cylinder": ObjectType.CYLINDER,
            "Cube": ObjectType.CUBE,
            "Airfoil": ObjectType.AIRFOIL,
            "Custom": ObjectType.CUSTOM,
            "Import 3D Mesh": ObjectType.CUSTOM
        }
        
        obj_type = obj_type_map[self.object_type_combo.currentText()]
        length = self.length_spin.value()
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        self.geometry_changed.emit(obj_type, length, width, height)
        
    def import_geometry(self):
        """Open geometry import dialog"""
        dialog = GeometryImportDialog(self)
        dialog.geometry_imported.connect(self.on_geometry_imported)
        dialog.exec()
        
    def on_geometry_imported(self, mesh, properties):
        """Handle imported geometry"""
        # Update dimensions based on imported mesh
        dimensions = properties['dimensions']
        self.length_spin.setValue(dimensions[0])
        self.width_spin.setValue(dimensions[1])
        self.height_spin.setValue(dimensions[2])
        
        # Store mesh data for simulation
        self.imported_mesh = mesh
        self.mesh_properties = properties
        
        # Trigger geometry change
        self.on_geometry_changed()
        
        # Show success message
        QMessageBox.information(
            self, 
            "Import Successful", 
            f"Successfully imported 3D geometry:\n\n"
            f"Name: {mesh.name}\n"
            f"Vertices: {len(mesh.vertices):,}\n"
            f"Faces: {len(mesh.faces):,}\n"
            f"Dimensions: {dimensions[0]:.2f} × {dimensions[1]:.2f} × {dimensions[2]:.2f} m"
        )
        
    def on_angle_changed(self, value):
        """Handle angle of attack change"""
        self.angle_label.setText(f"{value}°")
        # Update simulation parameter
        if hasattr(self.sim_manager, 'set_parameters'):
            self.sim_manager.set_parameters(object_angle=value)

class EnvironmentPanel(QWidget):
    """Panel for environmental settings"""
    
    parameters_changed = Signal(dict)
    
    def __init__(self, simulation_manager):
        super().__init__()
        self.sim_manager = simulation_manager
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Wind settings
        wind_group = QGroupBox("Wind Conditions")
        wind_layout = QGridLayout(wind_group)
        
        wind_layout.addWidget(QLabel("Wind Speed (m/s):"), 0, 0)
        self.wind_speed_spin = QDoubleSpinBox()
        self.wind_speed_spin.setRange(0.0, 100.0)
        self.wind_speed_spin.setValue(10.0)
        self.wind_speed_spin.setSingleStep(0.5)
        self.wind_speed_spin.valueChanged.connect(self.on_parameters_changed)
        wind_layout.addWidget(self.wind_speed_spin, 0, 1)
        
        wind_layout.addWidget(QLabel("Wind Direction (°):"), 1, 0)
        self.wind_angle_slider = QSlider(Qt.Horizontal)
        self.wind_angle_slider.setRange(0, 360)
        self.wind_angle_slider.setValue(0)
        self.wind_angle_slider.setTickPosition(QSlider.TicksBelow)
        self.wind_angle_slider.setTickInterval(45)
        self.wind_angle_slider.valueChanged.connect(self.on_wind_angle_changed)
        wind_layout.addWidget(self.wind_angle_slider, 1, 1)
        
        self.wind_angle_label = QLabel("0°")
        wind_layout.addWidget(self.wind_angle_label, 1, 2)
        
        # Atmospheric conditions
        atmo_group = QGroupBox("Atmospheric Conditions")
        atmo_layout = QGridLayout(atmo_group)
        
        atmo_layout.addWidget(QLabel("Air Density (kg/m³):"), 0, 0)
        self.density_spin = QDoubleSpinBox()
        self.density_spin.setRange(0.1, 2.0)
        self.density_spin.setValue(1.225)
        self.density_spin.setSingleStep(0.001)
        self.density_spin.setDecimals(3)
        self.density_spin.valueChanged.connect(self.on_parameters_changed)
        atmo_layout.addWidget(self.density_spin, 0, 1)
        
        atmo_layout.addWidget(QLabel("Temperature (K):"), 1, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(200.0, 350.0)
        self.temperature_spin.setValue(288.15)
        self.temperature_spin.setSingleStep(1.0)
        self.temperature_spin.setDecimals(2)
        self.temperature_spin.valueChanged.connect(self.on_parameters_changed)
        atmo_layout.addWidget(self.temperature_spin, 1, 1)
        
        atmo_layout.addWidget(QLabel("Pressure (Pa):"), 2, 0)
        self.pressure_spin = QDoubleSpinBox()
        self.pressure_spin.setRange(50000, 120000)
        self.pressure_spin.setValue(101325)
        self.pressure_spin.setSingleStep(1000)
        self.pressure_spin.setDecimals(0)
        self.pressure_spin.valueChanged.connect(self.on_parameters_changed)
        atmo_layout.addWidget(self.pressure_spin, 2, 1)
        
        # Advanced settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.turbulence_check = QCheckBox("Enable Turbulence")
        self.turbulence_check.stateChanged.connect(self.on_parameters_changed)
        advanced_layout.addWidget(self.turbulence_check)
        
        turb_layout = QHBoxLayout()
        turb_layout.addWidget(QLabel("Turbulence Intensity:"))
        self.turbulence_spin = QDoubleSpinBox()
        self.turbulence_spin.setRange(0.0, 1.0)
        self.turbulence_spin.setValue(0.1)
        self.turbulence_spin.setSingleStep(0.01)
        self.turbulence_spin.setDecimals(2)
        self.turbulence_spin.valueChanged.connect(self.on_parameters_changed)
        turb_layout.addWidget(self.turbulence_spin)
        advanced_layout.addLayout(turb_layout)
        
        self.gravity_check = QCheckBox("Include Gravity")
        self.gravity_check.setChecked(True)
        self.gravity_check.stateChanged.connect(self.on_parameters_changed)
        advanced_layout.addWidget(self.gravity_check)
        
        layout.addWidget(wind_group)
        layout.addWidget(atmo_group)
        layout.addWidget(advanced_group)
        layout.addStretch()
        
    def on_wind_angle_changed(self, value):
        """Handle wind angle change"""
        self.wind_angle_label.setText(f"{value}°")
        self.on_parameters_changed()
        
    def on_parameters_changed(self):
        """Handle parameter changes"""
        # Calculate wind velocity vector
        wind_speed = self.wind_speed_spin.value()
        wind_angle = self.wind_angle_slider.value()
        wind_angle_rad = np.radians(wind_angle)
        
        wind_velocity = np.array([
            wind_speed * np.cos(wind_angle_rad),
            wind_speed * np.sin(wind_angle_rad),
            0.0
        ])
        
        # Gravity vector
        if self.gravity_check.isChecked():
            gravity = np.array([0.0, -9.81, 0.0])
        else:
            gravity = np.array([0.0, 0.0, 0.0])
        
        params = {
            'wind_velocity': wind_velocity,
            'wind_angle': wind_angle,
            'air_density': self.density_spin.value(),
            'enable_turbulence': self.turbulence_check.isChecked(),
            'turbulence_intensity': self.turbulence_spin.value(),
            'gravity': gravity
        }
        
        self.parameters_changed.emit(params)
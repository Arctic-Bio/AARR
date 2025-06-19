"""
Geometry Import Dialog for 3D Mesh Files
"""

import os
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFileDialog, QLineEdit, QTextEdit,
                               QGroupBox, QGridLayout, QProgressBar, QTabWidget,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QComboBox, QDoubleSpinBox, QCheckBox, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor

import numpy as np
from ..geometry.mesh_loader import MeshLoader, Mesh
from ..physics.aerodynamics import ObjectType

class MeshLoadThread(QThread):
    """Thread for loading mesh files without blocking GUI"""
    
    mesh_loaded = Signal(object)  # Mesh object
    error_occurred = Signal(str)  # Error message
    progress_updated = Signal(int)  # Progress percentage
    
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        
    def run(self):
        """Load mesh in separate thread"""
        try:
            self.progress_updated.emit(10)
            
            # Load the mesh
            mesh = MeshLoader.load_mesh(self.filepath)
            self.progress_updated.emit(50)
            
            if mesh is None:
                self.error_occurred.emit("Failed to load mesh")
                return
            
            self.progress_updated.emit(100)
            self.mesh_loaded.emit(mesh)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class GeometryImportDialog(QDialog):
    """Dialog for importing 3D geometry files"""
    
    geometry_imported = Signal(object, dict)  # mesh, properties
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh = None
        self.mesh_properties = {}
        self.load_thread = None
        
        self.setWindowTitle("Import 3D Geometry")
        self.setModal(True)
        self.resize(800, 600)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # File selection tab
        self.create_file_tab(tabs)
        
        # Mesh properties tab
        self.create_properties_tab(tabs)
        
        # Preview tab
        self.create_preview_tab(tabs)
        
        # Aerodynamic settings tab
        self.create_aerodynamic_tab(tabs)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Load File")
        self.load_btn.clicked.connect(self.load_file)
        button_layout.addWidget(self.load_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self.import_geometry)
        self.import_btn.setEnabled(False)
        button_layout.addWidget(self.import_btn)
        
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def create_file_tab(self, parent):
        """Create file selection tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QGridLayout(file_group)
        
        file_layout.addWidget(QLabel("File Path:"), 0, 0)
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        file_layout.addWidget(self.file_path_edit, 0, 1)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn, 0, 2)
        
        layout.addWidget(file_group)
        
        # Supported formats group
        formats_group = QGroupBox("Supported Formats")
        formats_layout = QVBoxLayout(formats_group)
        
        formats_text = QTextEdit()
        formats_text.setReadOnly(True)
        formats_text.setMaximumHeight(150)
        formats_text.setPlainText(
            "Supported 3D file formats:\n\n"
            "• OBJ (.obj) - Wavefront OBJ files\n"
            "• STL (.stl) - Stereolithography files (ASCII and Binary)\n"
            "• PLY (.ply) - Polygon File Format\n\n"
            "Features:\n"
            "• Automatic mesh analysis and optimization\n"
            "• Aerodynamic property calculation\n"
            "• Real-time preview and validation\n"
            "• Custom scaling and positioning"
        )
        formats_layout.addWidget(formats_text)
        
        layout.addWidget(formats_group)
        layout.addStretch()
        
        parent.addTab(widget, "File Selection")
        
    def create_properties_tab(self, parent):
        """Create mesh properties tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Basic properties
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QGridLayout(basic_group)
        
        basic_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_label = QLabel("No mesh loaded")
        basic_layout.addWidget(self.name_label, 0, 1)
        
        basic_layout.addWidget(QLabel("Vertices:"), 1, 0)
        self.vertices_label = QLabel("0")
        basic_layout.addWidget(self.vertices_label, 1, 1)
        
        basic_layout.addWidget(QLabel("Faces:"), 2, 0)
        self.faces_label = QLabel("0")
        basic_layout.addWidget(self.faces_label, 2, 1)
        
        layout.addWidget(basic_group)
        
        # Dimensions
        dimensions_group = QGroupBox("Dimensions")
        dimensions_layout = QGridLayout(dimensions_group)
        
        dimensions_layout.addWidget(QLabel("Length (X):"), 0, 0)
        self.length_label = QLabel("0.00 m")
        dimensions_layout.addWidget(self.length_label, 0, 1)
        
        dimensions_layout.addWidget(QLabel("Width (Y):"), 1, 0)
        self.width_label = QLabel("0.00 m")
        dimensions_layout.addWidget(self.width_label, 1, 1)
        
        dimensions_layout.addWidget(QLabel("Height (Z):"), 2, 0)
        self.height_label = QLabel("0.00 m")
        dimensions_layout.addWidget(self.height_label, 2, 1)
        
        dimensions_layout.addWidget(QLabel("Volume:"), 3, 0)
        self.volume_label = QLabel("0.00 m³")
        dimensions_layout.addWidget(self.volume_label, 3, 1)
        
        layout.addWidget(dimensions_group)
        
        # Surface properties
        surface_group = QGroupBox("Surface Properties")
        surface_layout = QGridLayout(surface_group)
        
        surface_layout.addWidget(QLabel("Surface Area:"), 0, 0)
        self.surface_area_label = QLabel("0.00 m²")
        surface_layout.addWidget(self.surface_area_label, 0, 1)
        
        surface_layout.addWidget(QLabel("Frontal Area:"), 1, 0)
        self.frontal_area_label = QLabel("0.00 m²")
        surface_layout.addWidget(self.frontal_area_label, 1, 1)
        
        layout.addWidget(surface_group)
        layout.addStretch()
        
        parent.addTab(widget, "Properties")
        
    def create_preview_tab(self, parent):
        """Create mesh preview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Preview area (placeholder for 3D visualization)
        preview_group = QGroupBox("Mesh Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_label = QLabel("No mesh loaded")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #555;
                border-radius: 10px;
                background-color: #1e1e1e;
                color: #888;
                font-size: 14px;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        
        layout.addWidget(preview_group)
        
        # Mesh statistics
        stats_group = QGroupBox("Mesh Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_table = QTableWidget(0, 2)
        self.stats_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setMaximumHeight(150)
        stats_layout.addWidget(self.stats_table)
        
        layout.addWidget(stats_group)
        
        parent.addTab(widget, "Preview")
        
    def create_aerodynamic_tab(self, parent):
        """Create aerodynamic settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scaling and positioning
        transform_group = QGroupBox("Transform")
        transform_layout = QGridLayout(transform_group)
        
        transform_layout.addWidget(QLabel("Scale Factor:"), 0, 0)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.001, 1000.0)
        self.scale_spin.setValue(1.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.setDecimals(3)
        transform_layout.addWidget(self.scale_spin, 0, 1)
        
        transform_layout.addWidget(QLabel("Center Mesh:"), 1, 0)
        self.center_check = QCheckBox()
        self.center_check.setChecked(True)
        transform_layout.addWidget(self.center_check, 1, 1)
        
        layout.addWidget(transform_group)
        
        # Aerodynamic properties
        aero_group = QGroupBox("Aerodynamic Properties")
        aero_layout = QGridLayout(aero_group)
        
        aero_layout.addWidget(QLabel("Object Type:"), 0, 0)
        self.object_type_combo = QComboBox()
        self.object_type_combo.addItems([
            "Custom Geometry",
            "Aircraft-like",
            "Bluff Body",
            "Streamlined Body"
        ])
        aero_layout.addWidget(self.object_type_combo, 0, 1)
        
        aero_layout.addWidget(QLabel("Reference Area:"), 1, 0)
        self.ref_area_combo = QComboBox()
        self.ref_area_combo.addItems([
            "Auto (Frontal Area)",
            "Auto (Surface Area)",
            "Custom Value"
        ])
        aero_layout.addWidget(self.ref_area_combo, 1, 1)
        
        aero_layout.addWidget(QLabel("Custom Ref. Area:"), 2, 0)
        self.custom_area_spin = QDoubleSpinBox()
        self.custom_area_spin.setRange(0.001, 10000.0)
        self.custom_area_spin.setValue(1.0)
        self.custom_area_spin.setSuffix(" m²")
        self.custom_area_spin.setEnabled(False)
        aero_layout.addWidget(self.custom_area_spin, 2, 1)
        
        # Connect reference area combo to enable/disable custom area
        self.ref_area_combo.currentTextChanged.connect(
            lambda text: self.custom_area_spin.setEnabled("Custom" in text)
        )
        
        layout.addWidget(aero_group)
        
        # Advanced settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.optimize_check = QCheckBox("Optimize mesh for simulation")
        self.optimize_check.setChecked(True)
        advanced_layout.addWidget(self.optimize_check)
        
        self.validate_check = QCheckBox("Validate mesh integrity")
        self.validate_check.setChecked(True)
        advanced_layout.addWidget(self.validate_check)
        
        layout.addWidget(advanced_group)
        layout.addStretch()
        
        parent.addTab(widget, "Aerodynamics")
        
    def browse_file(self):
        """Browse for geometry file"""
        supported_formats = MeshLoader.get_supported_formats()
        filter_str = "3D Mesh Files ("
        filter_str += " ".join([f"*{fmt}" for fmt in supported_formats])
        filter_str += ");;"
        
        # Add individual format filters
        format_names = {
            '.obj': 'Wavefront OBJ',
            '.stl': 'STL Files',
            '.ply': 'PLY Files'
        }
        
        for fmt in supported_formats:
            name = format_names.get(fmt, f'{fmt.upper()} Files')
            filter_str += f"{name} (*{fmt});;"
        
        filter_str += "All Files (*.*)"
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select 3D Geometry File",
            "",
            filter_str
        )
        
        if filepath:
            self.file_path_edit.setText(filepath)
            self.load_btn.setEnabled(True)
            
    def load_file(self):
        """Load the selected file"""
        filepath = self.file_path_edit.text()
        if not filepath or not os.path.exists(filepath):
            QMessageBox.warning(self, "Error", "Please select a valid file.")
            return
            
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.load_btn.setEnabled(False)
        
        # Start loading thread
        self.load_thread = MeshLoadThread(filepath)
        self.load_thread.mesh_loaded.connect(self.on_mesh_loaded)
        self.load_thread.error_occurred.connect(self.on_load_error)
        self.load_thread.progress_updated.connect(self.progress_bar.setValue)
        self.load_thread.start()
        
    def on_mesh_loaded(self, mesh):
        """Handle successful mesh loading"""
        self.mesh = mesh
        self.update_mesh_info()
        
        self.progress_bar.setVisible(False)
        self.load_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", "Mesh loaded successfully!")
        
    def on_load_error(self, error_msg):
        """Handle mesh loading error"""
        self.progress_bar.setVisible(False)
        self.load_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Error", f"Failed to load mesh:\n{error_msg}")
        
    def update_mesh_info(self):
        """Update mesh information display"""
        if not self.mesh:
            return
            
        # Update basic properties
        self.name_label.setText(self.mesh.name)
        self.vertices_label.setText(f"{len(self.mesh.vertices):,}")
        self.faces_label.setText(f"{len(self.mesh.faces):,}")
        
        # Update dimensions
        dimensions = self.mesh.get_dimensions()
        self.length_label.setText(f"{dimensions[0]:.3f} m")
        self.width_label.setText(f"{dimensions[1]:.3f} m")
        self.height_label.setText(f"{dimensions[2]:.3f} m")
        
        volume = self.mesh.get_volume()
        self.volume_label.setText(f"{volume:.6f} m³")
        
        # Update surface properties
        surface_area = self.mesh.get_surface_area()
        self.surface_area_label.setText(f"{surface_area:.3f} m²")
        
        frontal_area = self.mesh.get_frontal_area()
        self.frontal_area_label.setText(f"{frontal_area:.3f} m²")
        
        # Update preview
        self.update_preview()
        
        # Update statistics table
        self.update_statistics()
        
    def update_preview(self):
        """Update mesh preview (simplified wireframe)"""
        if not self.mesh:
            return
            
        # Create a simple 2D projection preview
        self.preview_label.setText(
            f"Mesh Preview\n\n"
            f"Name: {self.mesh.name}\n"
            f"Vertices: {len(self.mesh.vertices):,}\n"
            f"Faces: {len(self.mesh.faces):,}\n\n"
            f"Dimensions:\n"
            f"L×W×H = {self.mesh.get_dimensions()[0]:.2f}×"
            f"{self.mesh.get_dimensions()[1]:.2f}×"
            f"{self.mesh.get_dimensions()[2]:.2f} m"
        )
        
    def update_statistics(self):
        """Update mesh statistics table"""
        if not self.mesh:
            return
            
        stats = [
            ("Vertices", f"{len(self.mesh.vertices):,}"),
            ("Faces", f"{len(self.mesh.faces):,}"),
            ("Surface Area", f"{self.mesh.get_surface_area():.3f} m²"),
            ("Volume", f"{self.mesh.get_volume():.6f} m³"),
            ("Frontal Area", f"{self.mesh.get_frontal_area():.3f} m²"),
            ("Bounding Box", f"{self.mesh.get_dimensions()[0]:.2f} × {self.mesh.get_dimensions()[1]:.2f} × {self.mesh.get_dimensions()[2]:.2f} m"),
            ("Center", f"({self.mesh.get_center()[0]:.2f}, {self.mesh.get_center()[1]:.2f}, {self.mesh.get_center()[2]:.2f})"),
        ]
        
        self.stats_table.setRowCount(len(stats))
        
        for i, (prop, value) in enumerate(stats):
            self.stats_table.setItem(i, 0, QTableWidgetItem(prop))
            self.stats_table.setItem(i, 1, QTableWidgetItem(value))
            
    def import_geometry(self):
        """Import the geometry with current settings"""
        if not self.mesh:
            QMessageBox.warning(self, "Error", "No mesh loaded.")
            return
            
        # Apply transformations
        mesh = self.mesh
        
        # Scale mesh
        scale_factor = self.scale_spin.value()
        if scale_factor != 1.0:
            mesh.vertices *= scale_factor
            
        # Center mesh
        if self.center_check.isChecked():
            center = mesh.get_center()
            mesh.vertices -= center
            
        # Prepare properties
        properties = {
            'object_type': ObjectType.CUSTOM,
            'mesh_file': self.file_path_edit.text(),
            'scale_factor': scale_factor,
            'centered': self.center_check.isChecked(),
            'aerodynamic_type': self.object_type_combo.currentText(),
            'reference_area_type': self.ref_area_combo.currentText(),
            'custom_reference_area': self.custom_area_spin.value(),
            'optimize_mesh': self.optimize_check.isChecked(),
            'validate_mesh': self.validate_check.isChecked(),
            'dimensions': mesh.get_dimensions(),
            'surface_area': mesh.get_surface_area(),
            'frontal_area': mesh.get_frontal_area(),
            'volume': mesh.get_volume()
        }
        
        # Emit signal with mesh and properties
        self.geometry_imported.emit(mesh, properties)
        self.accept()
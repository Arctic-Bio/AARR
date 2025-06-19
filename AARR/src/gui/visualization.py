"""
Visualization Widgets for Flow and Data Display
"""

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

##SAFE

class FlowVisualizationWidget(QWidget):
    """Widget for visualizing flow fields and streamlines"""
    
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Visualization:"))
        self.viz_combo = QComboBox()
        self.viz_combo.addItems([
            "Streamlines",
            "Velocity Field", 
            "Pressure Field",
            "Velocity Magnitude",
            "Combined View"
        ])
        self.viz_combo.currentTextChanged.connect(self.update_visualization)
        control_layout.addWidget(self.viz_combo)
        
        self.show_object_check = QCheckBox("Show Object")
        self.show_object_check.setChecked(True)
        self.show_object_check.stateChanged.connect(self.update_visualization)
        control_layout.addWidget(self.show_object_check)
        
        self.show_vectors_check = QCheckBox("Show Velocity Vectors")
        self.show_vectors_check.stateChanged.connect(self.update_visualization)
        control_layout.addWidget(self.show_vectors_check)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Matplotlib canvas
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #2d2d30;")
        layout.addWidget(self.canvas)
        
        # Set dark theme for matplotlib
        plt.style.use('dark_background')
        self.figure.patch.set_facecolor('#2d2d30')
        
    def update_data(self, data):
        """Update with new simulation data"""
        self.current_data = data
        self.update_visualization()
        
    def update_visualization(self):
        """Update the visualization"""
        if not self.current_data or 'flow_field' not in self.current_data:
            return
            
        flow_field = self.current_data['flow_field']
        if not flow_field:
            return
            
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        viz_type = self.viz_combo.currentText()
        
        if viz_type == "Streamlines":
            self._plot_streamlines(ax, flow_field)
        elif viz_type == "Velocity Field":
            self._plot_velocity_field(ax, flow_field)
        elif viz_type == "Pressure Field":
            self._plot_pressure_field(ax, flow_field)
        elif viz_type == "Velocity Magnitude":
            self._plot_velocity_magnitude(ax, flow_field)
        elif viz_type == "Combined View":
            self._plot_combined_view(ax, flow_field)
            
        if self.show_object_check.isChecked():
            self._draw_object(ax)
            
        ax.set_aspect('equal')
        ax.set_xlabel('X Position (m)', color='white')
        ax.set_ylabel('Y Position (m)', color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#1e1e1e')
        
        self.canvas.draw()
        
    def _plot_streamlines(self, ax, flow_field):
        """Plot streamlines"""
        X, Y = flow_field['x'], flow_field['y']
        U, V = flow_field['u'], flow_field['v']
        
        # Plot streamlines
        ax.streamplot(X, Y, U, V, color='cyan', density=2, linewidth=1, arrowsize=1.5)
        
        # Plot individual streamlines if available
        if 'streamlines_x' in flow_field and 'streamlines_y' in flow_field:
            for sx, sy in zip(flow_field['streamlines_x'], flow_field['streamlines_y']):
                ax.plot(sx, sy, 'yellow', linewidth=1.5, alpha=0.8)
                
        ax.set_title('Flow Streamlines', color='white', fontsize=14)
        
    def _plot_velocity_field(self, ax, flow_field):
        """Plot velocity field as vectors"""
        X, Y = flow_field['x'], flow_field['y']
        U, V = flow_field['u'], flow_field['v']
        
        # Subsample for cleaner visualization
        skip = 5
        ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
                 U[::skip, ::skip], V[::skip, ::skip],
                 scale=200, color='lime', alpha=0.7)
                 
        ax.set_title('Velocity Field', color='white', fontsize=14)
        
    def _plot_pressure_field(self, ax, flow_field):
        """Plot pressure field as contours"""
        X, Y = flow_field['x'], flow_field['y']
        pressure = flow_field['pressure']
        
        # Create contour plot
        contour = ax.contourf(X, Y, pressure, levels=20, cmap='RdYlBu_r', alpha=0.8)
        
        # Add colorbar
        cbar = self.figure.colorbar(contour, ax=ax)
        cbar.set_label('Pressure (Pa)', color='white')
        cbar.ax.tick_params(colors='white')
        
        # Add contour lines
        ax.contour(X, Y, pressure, levels=10, colors='white', alpha=0.5, linewidths=0.5)
        
        ax.set_title('Pressure Field', color='white', fontsize=14)
        
    def _plot_velocity_magnitude(self, ax, flow_field):
        """Plot velocity magnitude"""
        X, Y = flow_field['x'], flow_field['y']
        vel_mag = flow_field['velocity_magnitude']
        
        # Create filled contour plot
        contour = ax.contourf(X, Y, vel_mag, levels=20, cmap='plasma', alpha=0.8)
        
        # Add colorbar
        cbar = self.figure.colorbar(contour, ax=ax)
        cbar.set_label('Velocity Magnitude (m/s)', color='white')
        cbar.ax.tick_params(colors='white')
        
        ax.set_title('Velocity Magnitude', color='white', fontsize=14)
        
    def _plot_combined_view(self, ax, flow_field):
        """Plot combined visualization"""
        X, Y = flow_field['x'], flow_field['y']
        U, V = flow_field['u'], flow_field['v']
        vel_mag = flow_field['velocity_magnitude']
        
        # Background: velocity magnitude
        contour = ax.contourf(X, Y, vel_mag, levels=15, cmap='plasma', alpha=0.6)
        
        # Overlay: streamlines
        ax.streamplot(X, Y, U, V, color='white', density=1.5, linewidth=1, arrowsize=1)
        
        # Colorbar
        cbar = self.figure.colorbar(contour, ax=ax)
        cbar.set_label('Velocity Magnitude (m/s)', color='white')
        cbar.ax.tick_params(colors='white')
        
        ax.set_title('Combined Flow Visualization', color='white', fontsize=14)
        
    def _draw_object(self, ax):
        """Draw the object in the flow field"""
        # Simple representation - can be enhanced based on object type
        # For now, draw a simple ellipse representing the object
        obj_width = 2.0  # This should come from geometry data
        obj_height = 1.0
        
        ellipse = patches.Ellipse((0, 0), obj_width, obj_height, 
                                 facecolor='red', edgecolor='darkred', 
                                 alpha=0.8, linewidth=2)
        ax.add_patch(ellipse)
        
    def clear(self):
        """Clear the visualization"""
        self.figure.clear()
        self.canvas.draw()

class DataPlotWidget(QWidget):
    """Widget for plotting simulation data over time"""
    
    def __init__(self):
        super().__init__()
        self.results = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Plot Type:"))
        self.plot_combo = QComboBox()
        self.plot_combo.addItems([
            "Velocity vs Time",
            "Forces vs Time",
            "Position vs Time",
            "Energy vs Time",
            "Coefficients vs Time",
            "Trajectory (2D)",
            "Phase Space"
        ])
        self.plot_combo.currentTextChanged.connect(self.update_plot)
        control_layout.addWidget(self.plot_combo)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # PyQtGraph plot widget with enhanced styling
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e1e')
        
        # Enhanced axis styling
        left_axis = self.plot_widget.getAxis('left')
        bottom_axis = self.plot_widget.getAxis('bottom')
        
        # Set axis colors and styling
        axis_pen = pg.mkPen(color='white', width=2)
        left_axis.setPen(axis_pen)
        bottom_axis.setPen(axis_pen)
        left_axis.setTextPen('white')
        bottom_axis.setTextPen('white')
        
        # Set tick styling
        left_axis.setStyle(tickTextOffset=10)
        bottom_axis.setStyle(tickTextOffset=10)
        
        # Enable antialiasing for smoother lines
        self.plot_widget.setAntialiasing(True)
        
        # Set default grid
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        layout.addWidget(self.plot_widget)
        
    def update_data(self, results):
        """Update with new simulation results"""
        self.results = results
        self.update_plot()
        
    def update_plot(self):
        """Update the plot"""
        if not self.results:
            self.plot_widget.clear()
            self.plot_widget.setTitle("No simulation data - Start simulation to see plots", color='white', size='12pt')
            return
            
        # Check if we have any data at all
        if (not hasattr(self.results, 'time_history') or 
            not self.results.time_history or 
            len(self.results.time_history) == 0):
            # Show empty plot message
            self.plot_widget.clear()
            self.plot_widget.setTitle("No data available - Start simulation to see plots", color='white', size='12pt')
            return
            
        self.plot_widget.clear()
        plot_type = self.plot_combo.currentText()
        
        try:
            if plot_type == "Velocity vs Time":
                self._plot_velocity_time()
            elif plot_type == "Forces vs Time":
                self._plot_forces_time()
            elif plot_type == "Position vs Time":
                self._plot_position_time()
            elif plot_type == "Energy vs Time":
                self._plot_energy_time()
            elif plot_type == "Coefficients vs Time":
                self._plot_coefficients_time()
            elif plot_type == "Trajectory (2D)":
                self._plot_trajectory_2d()
            elif plot_type == "Phase Space":
                self._plot_phase_space()
                
            # Enable auto-range and grid for better visibility
            self.plot_widget.enableAutoRange()
            self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
            
        except Exception as e:
            print(f"Error plotting {plot_type}: {e}")
            import traceback
            traceback.print_exc()
            self.plot_widget.setTitle(f"Error plotting {plot_type}: {str(e)}", color='red', size='12pt')
            
    def _plot_velocity_time(self):
        """Plot velocity components vs time"""
        if not hasattr(self.results, 'velocity_history') or not self.results.velocity_history:
            self.plot_widget.setTitle("No velocity data available", color='yellow', size='12pt')
            return
            
        times = np.array(self.results.time_history)
        velocities = np.array(self.results.velocity_history)
        
        if len(velocities) == 0 or len(times) == 0:
            self.plot_widget.setTitle("No velocity data available", color='yellow', size='12pt')
            return
        
        # Ensure data consistency
        min_len = min(len(times), len(velocities))
        times = times[:min_len]
        velocities = velocities[:min_len]
        
        # Clear any existing legend
        self.plot_widget.clear()
        
        if velocities.ndim == 1:
            # Handle 1D velocity data
            self.plot_widget.plot(times, velocities, pen=pg.mkPen(color='white', width=3), name='Velocity')
        else:
            # Handle 3D velocity data
            if velocities.shape[1] >= 3:
                # Use brighter, thicker lines for better visibility
                self.plot_widget.plot(times, velocities[:, 0], pen=pg.mkPen(color='red', width=2), name='Vx')
                self.plot_widget.plot(times, velocities[:, 1], pen=pg.mkPen(color='lime', width=2), name='Vy')
                self.plot_widget.plot(times, velocities[:, 2], pen=pg.mkPen(color='cyan', width=2), name='Vz')
                
                # Plot velocity magnitude with thicker white line
                vel_mag = np.linalg.norm(velocities, axis=1)
                self.plot_widget.plot(times, vel_mag, pen=pg.mkPen(color='white', width=3), name='|V|')
        
        self.plot_widget.setLabel('left', 'Velocity (m/s)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Time (s)', color='white', size='12pt')
        self.plot_widget.setTitle('Velocity vs Time', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_forces_time(self):
        """Plot forces vs time"""
        if not hasattr(self.results, 'force_history') or not self.results.force_history:
            self.plot_widget.setTitle("No force data available", color='yellow', size='12pt')
            return
            
        times = np.array(self.results.time_history)
        
        if len(times) == 0:
            self.plot_widget.setTitle("No time data available", color='yellow', size='12pt')
            return
            
        drag_forces = []
        lift_forces = []
        total_forces = []
        
        for forces in self.results.force_history:
            if isinstance(forces, dict):
                drag_forces.append(np.linalg.norm(forces.get('drag', [0, 0, 0])))
                lift_forces.append(np.linalg.norm(forces.get('lift', [0, 0, 0])))
                total_forces.append(np.linalg.norm(forces.get('total', [0, 0, 0])))
            else:
                # Handle case where forces might be stored differently
                drag_forces.append(0)
                lift_forces.append(0)
                total_forces.append(0)
        
        # Ensure data consistency
        min_len = min(len(times), len(drag_forces))
        times = times[:min_len]
        drag_forces = np.array(drag_forces[:min_len])
        lift_forces = np.array(lift_forces[:min_len])
        total_forces = np.array(total_forces[:min_len])
        
        if min_len > 0:
            # Use brighter colors and thicker lines
            self.plot_widget.plot(times, drag_forces, pen=pg.mkPen(color='red', width=2), name='Drag')
            self.plot_widget.plot(times, lift_forces, pen=pg.mkPen(color='lime', width=2), name='Lift')
            self.plot_widget.plot(times, total_forces, pen=pg.mkPen(color='white', width=3), name='Total')
            
            # Add side force if available
            side_forces = []
            for forces in self.results.force_history[:min_len]:
                if isinstance(forces, dict):
                    side_forces.append(np.linalg.norm(forces.get('side_force', [0, 0, 0])))
                else:
                    side_forces.append(0)
            
            if any(f > 0.001 for f in side_forces):  # Only plot if there's significant side force
                self.plot_widget.plot(times, side_forces, pen=pg.mkPen(color='cyan', width=2), name='Side')
        
        self.plot_widget.setLabel('left', 'Force (N)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Time (s)', color='white', size='12pt')
        self.plot_widget.setTitle('Forces vs Time', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_position_time(self):
        """Plot position vs time"""
        if not hasattr(self.results, 'position_history') or not self.results.position_history:
            self.plot_widget.setTitle("No position data available", color='yellow', size='12pt')
            return
            
        times = np.array(self.results.time_history)
        positions = np.array(self.results.position_history)
        
        if len(positions) == 0 or len(times) == 0:
            self.plot_widget.setTitle("No position data available", color='yellow', size='12pt')
            return
        
        # Ensure data consistency
        min_len = min(len(times), len(positions))
        times = times[:min_len]
        positions = positions[:min_len]
        
        if positions.ndim == 1:
            # Handle 1D position data
            self.plot_widget.plot(times, positions, pen=pg.mkPen(color='white', width=3), name='Position')
        else:
            # Handle 3D position data
            if positions.shape[1] >= 3:
                self.plot_widget.plot(times, positions[:, 0], pen=pg.mkPen(color='red', width=2), name='X')
                self.plot_widget.plot(times, positions[:, 1], pen=pg.mkPen(color='lime', width=2), name='Y')
                self.plot_widget.plot(times, positions[:, 2], pen=pg.mkPen(color='cyan', width=2), name='Z')
        
        self.plot_widget.setLabel('left', 'Position (m)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Time (s)', color='white', size='12pt')
        self.plot_widget.setTitle('Position vs Time', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_energy_time(self):
        """Plot energy vs time"""
        if not hasattr(self.results, 'velocity_history') or not self.results.velocity_history:
            self.plot_widget.setTitle("No velocity data available for energy calculation", color='yellow', size='12pt')
            return
            
        times = np.array(self.results.time_history)
        velocities = np.array(self.results.velocity_history)
        positions = np.array(self.results.position_history)
        
        if len(velocities) == 0 or len(times) == 0:
            self.plot_widget.setTitle("No data available for energy calculation", color='yellow', size='12pt')
            return
            
        # Ensure data consistency
        min_len = min(len(times), len(velocities), len(positions))
        times = times[:min_len]
        velocities = velocities[:min_len]
        positions = positions[:min_len]
        
        # Calculate energies (assuming unit mass)
        if velocities.ndim == 1:
            speeds = np.abs(velocities)
        else:
            speeds = np.linalg.norm(velocities, axis=1)
            
        kinetic_energy = 0.5 * speeds**2
        
        # Calculate potential energy (assuming gravity in Y direction)
        if positions.ndim == 1:
            potential_energy = 9.81 * positions
        else:
            potential_energy = 9.81 * positions[:, 1]  # mgh, assuming g = 9.81
            
        total_energy = kinetic_energy + potential_energy
        
        # Plot with better visibility
        self.plot_widget.plot(times, kinetic_energy, pen=pg.mkPen(color='red', width=2), name='Kinetic')
        self.plot_widget.plot(times, potential_energy, pen=pg.mkPen(color='lime', width=2), name='Potential')
        self.plot_widget.plot(times, total_energy, pen=pg.mkPen(color='white', width=3), name='Total')
        
        self.plot_widget.setLabel('left', 'Energy (J/kg)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Time (s)', color='white', size='12pt')
        self.plot_widget.setTitle('Energy vs Time', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_coefficients_time(self):
        """Plot aerodynamic coefficients vs time"""
        if not hasattr(self.results, 'force_history') or not self.results.force_history:
            self.plot_widget.setTitle("No force data available for coefficients", color='yellow', size='12pt')
            return
            
        times = np.array(self.results.time_history)
        
        if len(times) == 0:
            self.plot_widget.setTitle("No time data available", color='yellow', size='12pt')
            return
            
        cd_values = []
        cl_values = []
        reynolds_values = []
        
        for forces in self.results.force_history:
            if isinstance(forces, dict):
                coeffs = forces.get('coefficients', {})
                cd_values.append(coeffs.get('cd', 0))
                cl_values.append(coeffs.get('cl', 0))
                reynolds_values.append(coeffs.get('reynolds', 0))
            else:
                cd_values.append(0)
                cl_values.append(0)
                reynolds_values.append(0)
        
        # Ensure data consistency
        min_len = min(len(times), len(cd_values))
        times = times[:min_len]
        cd_values = np.array(cd_values[:min_len])
        cl_values = np.array(cl_values[:min_len])
        reynolds_values = np.array(reynolds_values[:min_len])
        
        if min_len > 0:
            # Plot coefficients with better visibility
            self.plot_widget.plot(times, cd_values, pen=pg.mkPen(color='red', width=2), name='Cd (Drag)')
            self.plot_widget.plot(times, cl_values, pen=pg.mkPen(color='lime', width=2), name='Cl (Lift)')
            
            # Only plot Reynolds number if it varies significantly
            if np.std(reynolds_values) > 100:  # Only if there's significant variation
                # Normalize Reynolds number for plotting (divide by 1000 for readability)
                reynolds_normalized = reynolds_values / 1000
                self.plot_widget.plot(times, reynolds_normalized, pen=pg.mkPen(color='cyan', width=2), name='Re/1000')
        
        self.plot_widget.setLabel('left', 'Coefficient', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Time (s)', color='white', size='12pt')
        self.plot_widget.setTitle('Aerodynamic Coefficients vs Time', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_trajectory_2d(self):
        """Plot 2D trajectory"""
        if not hasattr(self.results, 'position_history') or not self.results.position_history:
            self.plot_widget.setTitle("No position data available for trajectory", color='yellow', size='12pt')
            return
            
        positions = np.array(self.results.position_history)
        
        if len(positions) == 0:
            self.plot_widget.setTitle("No position data available for trajectory", color='yellow', size='12pt')
            return
        
        if positions.ndim == 1 or positions.shape[1] < 2:
            self.plot_widget.setTitle("Insufficient position data for 2D trajectory", color='yellow', size='12pt')
            return
            
        # Plot trajectory with thicker line
        self.plot_widget.plot(positions[:, 0], positions[:, 1], pen=pg.mkPen(color='white', width=3))
        
        # Add start and end markers with better visibility
        if len(positions) > 0:
            self.plot_widget.plot([positions[0, 0]], [positions[0, 1]], 
                                pen=None, symbol='o', symbolBrush='lime', symbolSize=12, name='Start')
        if len(positions) > 1:
            self.plot_widget.plot([positions[-1, 0]], [positions[-1, 1]], 
                                pen=None, symbol='s', symbolBrush='red', symbolSize=12, name='End')
        
        # Add direction arrows if trajectory is long enough
        if len(positions) > 10:
            # Sample some points along the trajectory for arrows
            step = max(1, len(positions) // 10)
            for i in range(step, len(positions), step):
                if i < len(positions) - 1:
                    dx = positions[i+1, 0] - positions[i, 0]
                    dy = positions[i+1, 1] - positions[i, 1]
                    if abs(dx) > 1e-6 or abs(dy) > 1e-6:  # Only draw if there's movement
                        arrow = pg.ArrowItem(angle=np.degrees(np.arctan2(dy, dx)), 
                                           headLen=20, tailLen=20, pen='cyan', brush='cyan')
                        arrow.setPos(positions[i, 0], positions[i, 1])
                        self.plot_widget.addItem(arrow)
        
        self.plot_widget.setLabel('left', 'Y Position (m)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'X Position (m)', color='white', size='12pt')
        self.plot_widget.setTitle('2D Trajectory', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def _plot_phase_space(self):
        """Plot phase space (position vs velocity)"""
        if not hasattr(self.results, 'position_history') or not self.results.position_history:
            self.plot_widget.setTitle("No position data available for phase space", color='yellow', size='12pt')
            return
            
        if not hasattr(self.results, 'velocity_history') or not self.results.velocity_history:
            self.plot_widget.setTitle("No velocity data available for phase space", color='yellow', size='12pt')
            return
            
        positions = np.array(self.results.position_history)
        velocities = np.array(self.results.velocity_history)
        
        if len(positions) == 0 or len(velocities) == 0:
            self.plot_widget.setTitle("No data available for phase space", color='yellow', size='12pt')
            return
        
        # Ensure data consistency
        min_len = min(len(positions), len(velocities))
        positions = positions[:min_len]
        velocities = velocities[:min_len]
        
        if positions.ndim == 1 or velocities.ndim == 1:
            self.plot_widget.setTitle("Insufficient dimensional data for phase space", color='yellow', size='12pt')
            return
            
        if positions.shape[1] < 2 or velocities.shape[1] < 2:
            self.plot_widget.setTitle("Insufficient dimensional data for phase space", color='yellow', size='12pt')
            return
            
        # Plot X position vs X velocity and Y position vs Y velocity
        self.plot_widget.plot(positions[:, 0], velocities[:, 0], pen=pg.mkPen(color='red', width=2), name='X phase')
        self.plot_widget.plot(positions[:, 1], velocities[:, 1], pen=pg.mkPen(color='lime', width=2), name='Y phase')
        
        # Add start and end markers
        if len(positions) > 0:
            self.plot_widget.plot([positions[0, 0]], [velocities[0, 0]], 
                                pen=None, symbol='o', symbolBrush='cyan', symbolSize=10, name='X Start')
            self.plot_widget.plot([positions[0, 1]], [velocities[0, 1]], 
                                pen=None, symbol='o', symbolBrush='yellow', symbolSize=10, name='Y Start')
        
        self.plot_widget.setLabel('left', 'Velocity (m/s)', color='white', size='12pt')
        self.plot_widget.setLabel('bottom', 'Position (m)', color='white', size='12pt')
        self.plot_widget.setTitle('Phase Space', color='white', size='14pt')
        
        # Add legend with better styling
        legend = self.plot_widget.addLegend()
        legend.setLabelTextColor('white')
        
    def clear(self):
        """Clear the plot"""
        self.plot_widget.clear()
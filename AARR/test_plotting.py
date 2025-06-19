#!/usr/bin/env python3
"""
Test script to verify plotting functionality
"""

import sys
import os
sys.path.append('src')

import numpy as np
from PySide6.QtWidgets import QApplication
from src.gui.visualization import DataPlotWidget
from src.physics.simulation import SimulationManager, SimulationResults, ObjectType

def test_plotting():
    """Test the plotting functionality"""
    app = QApplication(sys.argv)
    
    # Create a plot widget
    plot_widget = DataPlotWidget()
    plot_widget.show()
    plot_widget.resize(800, 600)
    
    # Create some test data
    results = SimulationResults()
    
    # Generate test data
    times = np.linspace(0, 5, 100)
    for t in times:
        results.time_history.append(t)
        
        # Position: parabolic trajectory
        x = 10 * t
        y = 5 * t - 0.5 * 9.81 * t**2
        z = 0
        results.position_history.append(np.array([x, y, z]))
        
        # Velocity: derivative of position
        vx = 10
        vy = 5 - 9.81 * t
        vz = 0
        results.velocity_history.append(np.array([vx, vy, vz]))
        
        # Acceleration: constant gravity
        results.acceleration_history.append(np.array([0, -9.81, 0]))
        
        # Forces: drag and gravity
        speed = np.sqrt(vx**2 + vy**2)
        drag_force = -0.5 * 1.225 * 0.1 * speed**2 * np.array([vx, vy, 0]) / speed if speed > 0 else np.array([0, 0, 0])
        gravity_force = np.array([0, -9.81, 0])
        total_force = drag_force + gravity_force
        
        forces = {
            'drag': drag_force,
            'lift': np.array([0, 0, 0]),
            'side_force': np.array([0, 0, 0]),
            'total': total_force,
            'coefficients': {
                'cd': 0.5,
                'cl': 0.1,
                'reynolds': 10000 + t * 1000
            }
        }
        results.force_history.append(forces)
    
    # Update the plot widget with test data
    plot_widget.update_data(results)
    
    print("Test data created:")
    print(f"Time points: {len(results.time_history)}")
    print(f"Position points: {len(results.position_history)}")
    print(f"Velocity points: {len(results.velocity_history)}")
    print(f"Force points: {len(results.force_history)}")
    print(f"Sample position: {results.position_history[0]}")
    print(f"Sample velocity: {results.velocity_history[0]}")
    print(f"Sample forces: {list(results.force_history[0].keys())}")
    
    # Show the widget
    plot_widget.setWindowTitle("Aerodynamic Simulation - Data Plots Test")
    
    return app.exec()

if __name__ == "__main__":
    test_plotting()
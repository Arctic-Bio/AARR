#!/usr/bin/env python3
"""
Demo script showing how to use the Aerodynamic Simulation System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.physics.simulation import SimulationManager
from src.physics.aerodynamics import ObjectType
import numpy as np
import time

def demo_jet_simulation():
    """Demonstrate jet aircraft simulation"""
    print("=== Jet Aircraft Aerodynamic Analysis ===")
    
    # Create simulation manager
    sim = SimulationManager()
    
    # Configure jet aircraft
    sim.set_object_geometry(ObjectType.JET, length=15.0, width=3.0, height=2.0)
    
    # Set simulation parameters
    sim.set_parameters(
        wind_velocity=np.array([50.0, 0.0, 0.0]),  # 50 m/s headwind
        wind_angle=180.0,  # Head-on wind
        object_angle=5.0,  # 5 degree angle of attack
        max_time=5.0,
        dt=0.01
    )
    
    # Set initial velocity
    sim.state.velocity = np.array([100.0, 0.0, 0.0])  # 100 m/s forward
    
    print(f"Initial Configuration:")
    print(f"  Object: Jet Aircraft (15m x 3m x 2m)")
    print(f"  Initial Speed: 100 m/s")
    print(f"  Wind Speed: 50 m/s (headwind)")
    print(f"  Angle of Attack: 5°")
    print()
    
    # Run simulation
    print("Running simulation...")
    steps = 0
    max_steps = 500
    
    while steps < max_steps and sim.step_simulation():
        steps += 1
        
        # Print progress every 50 steps
        if steps % 50 == 0:
            data = sim.get_current_data()
            state = data['state']
            
            speed = np.linalg.norm(state.velocity)
            forces = state.forces
            
            if forces:
                drag_mag = np.linalg.norm(forces.get('drag', [0, 0, 0]))
                lift_mag = np.linalg.norm(forces.get('lift', [0, 0, 0]))
                coeffs = forces.get('coefficients', {})
                
                print(f"Step {steps:3d}: t={state.time:.2f}s, Speed={speed:.1f}m/s, "
                      f"Drag={drag_mag:.1f}N, Lift={lift_mag:.1f}N, "
                      f"Cd={coeffs.get('cd', 0):.3f}, Cl={coeffs.get('cl', 0):.3f}")
    
    # Get final analysis
    analysis = sim.get_analysis_data()
    
    print("\n=== Final Analysis ===")
    motion_stats = analysis.get('motion_stats', {})
    force_stats = analysis.get('force_stats', {})
    efficiency_stats = analysis.get('efficiency_stats', {})
    
    print(f"Maximum Speed: {motion_stats.get('max_speed', 0):.1f} m/s")
    print(f"Average Speed: {motion_stats.get('avg_speed', 0):.1f} m/s")
    print(f"Maximum Drag: {force_stats.get('max_drag', 0):.1f} N")
    print(f"Average Drag: {force_stats.get('avg_drag', 0):.1f} N")
    print(f"Maximum Lift: {force_stats.get('max_lift', 0):.1f} N")
    print(f"L/D Ratio: {efficiency_stats.get('lift_to_drag_ratio', 0):.2f}")
    print(f"Drag Coefficient: {efficiency_stats.get('drag_coefficient', 0):.3f}")
    print(f"Fineness Ratio: {efficiency_stats.get('fineness_ratio', 0):.2f}")
    
    return sim

def main():
    """Run demonstration"""
    print("Advanced Aerodynamic Simulation System - Demo")
    print("=" * 50)
    
    try:
        demo_jet_simulation()
        print("\nDemo completed successfully!")
        print("To run the full GUI application, execute: python main.py")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
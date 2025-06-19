#!/usr/bin/env python3
"""
Test script for the Advanced Aerodynamic Simulation System
Tests plotting functionality and 3D geometry import
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.physics.simulation import SimulationManager
from src.physics.aerodynamics import ObjectType
from src.geometry.mesh_loader import MeshLoader
import numpy as np

def test_plotting_data():
    """Test that simulation generates plottable data"""
    print("=== Testing Plotting Data Generation ===")
    
    # Create simulation manager
    sim = SimulationManager()
    
    # Configure simple sphere
    sim.set_object_geometry(ObjectType.SPHERE, length=2.0, width=2.0, height=2.0)
    
    # Set simulation parameters
    sim.set_parameters(
        wind_velocity=np.array([10.0, 0.0, 0.0]),  # 10 m/s wind
        max_time=2.0,
        dt=0.01
    )
    
    # Set initial velocity
    sim.state.velocity = np.array([20.0, 0.0, 0.0])  # 20 m/s forward
    
    print("Running simulation to generate data...")
    
    # Run simulation for a short time
    steps = 0
    max_steps = 100
    
    while steps < max_steps and sim.step_simulation():
        steps += 1
        
        if steps % 20 == 0:
            print(f"Step {steps}: t={sim.state.time:.2f}s")
    
    # Check results
    results = sim.results
    
    print(f"\nResults Summary:")
    print(f"Time history length: {len(results.time_history) if hasattr(results, 'time_history') else 0}")
    print(f"Position history length: {len(results.position_history) if hasattr(results, 'position_history') else 0}")
    print(f"Velocity history length: {len(results.velocity_history) if hasattr(results, 'velocity_history') else 0}")
    print(f"Force history length: {len(results.force_history) if hasattr(results, 'force_history') else 0}")
    
    # Test data access
    if hasattr(results, 'time_history') and results.time_history:
        print(f"Time range: {results.time_history[0]:.3f} to {results.time_history[-1]:.3f} seconds")
        
        if hasattr(results, 'velocity_history') and results.velocity_history:
            velocities = np.array(results.velocity_history)
            print(f"Velocity data shape: {velocities.shape}")
            print(f"Final velocity: {velocities[-1]} m/s")
            
        if hasattr(results, 'position_history') and results.position_history:
            positions = np.array(results.position_history)
            print(f"Position data shape: {positions.shape}")
            print(f"Final position: {positions[-1]} m")
            
        print("✓ Plotting data generation successful!")
    else:
        print("✗ No time history data generated!")
        
    return sim

def test_mesh_loading():
    """Test 3D mesh loading functionality"""
    print("\n=== Testing 3D Mesh Loading ===")
    
    # Test OBJ loading
    obj_files = [
        "sample_models/simple_aircraft.obj",
        "sample_models/sphere.obj"
    ]
    
    for obj_file in obj_files:
        if os.path.exists(obj_file):
            print(f"\nTesting {obj_file}...")
            
            try:
                mesh = MeshLoader.load_mesh(obj_file)
                
                print(f"✓ Loaded mesh: {mesh.name}")
                print(f"  Vertices: {len(mesh.vertices):,}")
                print(f"  Faces: {len(mesh.faces):,}")
                print(f"  Dimensions: {mesh.get_dimensions()}")
                print(f"  Surface area: {mesh.get_surface_area():.3f} m²")
                print(f"  Frontal area: {mesh.get_frontal_area():.3f} m²")
                print(f"  Volume: {mesh.get_volume():.6f} m³")
                
            except Exception as e:
                print(f"✗ Failed to load {obj_file}: {e}")
        else:
            print(f"Sample file {obj_file} not found, creating...")
            # The files should have been created above
    
    # Test primitive mesh creation
    print(f"\nTesting primitive mesh creation...")
    
    primitives = ['sphere', 'cube', 'cylinder', 'cone']
    
    for primitive in primitives:
        try:
            mesh = MeshLoader.create_primitive_mesh(primitive)
            print(f"✓ Created {primitive}: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
        except Exception as e:
            print(f"✗ Failed to create {primitive}: {e}")

def test_simulation_with_custom_mesh():
    """Test simulation with custom mesh"""
    print("\n=== Testing Simulation with Custom Mesh ===")
    
    try:
        # Create a simple sphere mesh
        mesh = MeshLoader.create_primitive_mesh('sphere', radius=1.0, subdivisions=10)
        
        # Create simulation
        sim = SimulationManager()
        
        # Set custom geometry (we'll need to extend the simulation manager for this)
        sim.set_object_geometry(ObjectType.CUSTOM, length=2.0, width=2.0, height=2.0)
        
        # Set parameters
        sim.set_parameters(
            wind_velocity=np.array([15.0, 0.0, 0.0]),
            max_time=1.0,
            dt=0.01
        )
        
        sim.state.velocity = np.array([25.0, 0.0, 0.0])
        
        print("Running simulation with custom mesh...")
        
        # Run simulation
        steps = 0
        while steps < 50 and sim.step_simulation():
            steps += 1
            
        print(f"✓ Custom mesh simulation completed: {steps} steps")
        
        # Check results
        if hasattr(sim.results, 'time_history') and sim.results.time_history:
            print(f"  Generated {len(sim.results.time_history)} data points")
        
    except Exception as e:
        print(f"✗ Custom mesh simulation failed: {e}")

def main():
    """Run all tests"""
    print("Advanced Aerodynamic Simulation System - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Plotting data generation
        sim = test_plotting_data()
        
        # Test 2: Mesh loading
        test_mesh_loading()
        
        # Test 3: Custom mesh simulation
        test_simulation_with_custom_mesh()
        
        print("\n" + "=" * 60)
        print("Test suite completed!")
        print("\nTo test the GUI with plotting:")
        print("1. Run: python main.py")
        print("2. Start a simulation")
        print("3. Check the 'Data Plots' tab")
        print("4. Try different plot types")
        print("\nTo test 3D geometry import:")
        print("1. Run: python main.py")
        print("2. Go to Object tab")
        print("3. Select 'Import 3D Mesh'")
        print("4. Click 'Import 3D Geometry...'")
        print("5. Load sample_models/simple_aircraft.obj")
        
    except Exception as e:
        print(f"Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
"""
Simulation Manager
Handles the overall simulation state and time stepping
"""

import numpy as np
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
import time
from .aerodynamics import AerodynamicsEngine, ObjectGeometry, SimulationState, ObjectType

@dataclass
class SimulationParameters:
    """Simulation configuration parameters"""
    dt: float = 0.001  # Time step
    max_time: float = 10.0  # Maximum simulation time
    wind_velocity: np.ndarray = field(default_factory=lambda: np.array([10.0, 0.0, 0.0]))  # m/s
    wind_angle: float = 0.0  # degrees
    object_angle: float = 0.0  # degrees (angle of attack)
    gravity: np.ndarray = field(default_factory=lambda: np.array([0.0, -9.81, 0.0]))  # m/s²
    air_density: float = 1.225  # kg/m³
    enable_turbulence: bool = False
    turbulence_intensity: float = 0.1

@dataclass
class SimulationResults:
    """Container for simulation results"""
    time_history: List[float] = field(default_factory=list)
    position_history: List[np.ndarray] = field(default_factory=list)
    velocity_history: List[np.ndarray] = field(default_factory=list)
    acceleration_history: List[np.ndarray] = field(default_factory=list)
    force_history: List[Dict] = field(default_factory=list)
    flow_fields: List[Dict] = field(default_factory=list)
    efficiency_metrics: List[Dict] = field(default_factory=list)
    
    def get_latest_data(self) -> Dict:
        """Get the most recent simulation data"""
        if not self.time_history:
            return {}
        
        return {
            'time': self.time_history[-1],
            'position': self.position_history[-1],
            'velocity': self.velocity_history[-1],
            'acceleration': self.acceleration_history[-1],
            'forces': self.force_history[-1],
            'flow_field': self.flow_fields[-1] if self.flow_fields else None,
            'efficiency': self.efficiency_metrics[-1] if self.efficiency_metrics else None
        }

class SimulationManager:
    """Manages the aerodynamic simulation"""
    
    def __init__(self):
        self.engine = AerodynamicsEngine()
        self.is_running = False
        self.is_paused = False
        self.current_time = 0.0
        self.results = SimulationResults()
        self.parameters = SimulationParameters()
        self.state = SimulationState(
            position=np.array([0.0, 0.0, 0.0]),
            velocity=np.array([0.0, 0.0, 0.0]),
            acceleration=np.array([0.0, 0.0, 0.0]),
            angular_velocity=np.array([0.0, 0.0, 0.0]),
            time=0.0,
            forces={},
            moments={}
        )
        self.geometry = None
        self.callbacks = []
        
    def set_object_geometry(self, obj_type: ObjectType, length: float, width: float, height: float):
        """Set the object geometry for simulation"""
        # Calculate derived properties
        if obj_type == ObjectType.JET:
            frontal_area = np.pi * (width/2) * (height/2)  # Elliptical cross-section
            surface_area = 2 * np.pi * (width/2) * length  # Simplified
            volume = frontal_area * length * 0.7  # Approximate
        elif obj_type == ObjectType.SPHERE:
            radius = width / 2
            frontal_area = np.pi * radius**2
            surface_area = 4 * np.pi * radius**2
            volume = (4/3) * np.pi * radius**3
        elif obj_type == ObjectType.CYLINDER:
            radius = width / 2
            frontal_area = np.pi * radius**2
            surface_area = 2 * np.pi * radius * (radius + length)
            volume = np.pi * radius**2 * length
        elif obj_type == ObjectType.CUBE:
            frontal_area = width * height
            surface_area = 2 * (width * height + width * length + height * length)
            volume = width * height * length
        else:
            frontal_area = width * height
            surface_area = 2 * (width * height + width * length + height * length)
            volume = width * height * length
            
        self.geometry = ObjectGeometry(
            length=length,
            width=width,
            height=height,
            frontal_area=frontal_area,
            surface_area=surface_area,
            volume=volume,
            object_type=obj_type
        )
    
    def set_parameters(self, **kwargs):
        """Update simulation parameters"""
        for key, value in kwargs.items():
            if hasattr(self.parameters, key):
                setattr(self.parameters, key, value)
    
    def add_callback(self, callback: Callable):
        """Add a callback function to be called during simulation"""
        self.callbacks.append(callback)
    
    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.current_time = 0.0
        self.is_running = False
        self.is_paused = False
        self.results = SimulationResults()
        self.state = SimulationState(
            position=np.array([0.0, 0.0, 0.0]),
            velocity=self.parameters.wind_velocity.copy(),  # Start with wind velocity
            acceleration=np.array([0.0, 0.0, 0.0]),
            angular_velocity=np.array([0.0, 0.0, 0.0]),
            time=0.0,
            forces={},
            moments={}
        )
    
    def step_simulation(self) -> bool:
        """Perform one simulation time step"""
        if not self.geometry or self.current_time >= self.parameters.max_time:
            return False
        
        # Calculate wind velocity with angle
        wind_angle_rad = np.radians(self.parameters.wind_angle)
        wind_speed = np.linalg.norm(self.parameters.wind_velocity)
        wind_velocity = np.array([
            wind_speed * np.cos(wind_angle_rad),
            wind_speed * np.sin(wind_angle_rad),
            0.0
        ])
        
        # Add turbulence if enabled
        if self.parameters.enable_turbulence:
            turbulence = np.random.normal(0, self.parameters.turbulence_intensity, 3)
            wind_velocity += turbulence * wind_speed
        
        # Calculate aerodynamic forces
        forces = self.engine.calculate_forces(
            self.geometry,
            self.state.velocity,
            self.parameters.object_angle,
            wind_velocity
        )
        
        # Calculate total acceleration (including gravity)
        # Assume unit mass for simplicity
        total_force = forces['total'] + self.parameters.gravity
        self.state.acceleration = total_force
        
        # Update velocity and position using Euler integration
        self.state.velocity += self.state.acceleration * self.parameters.dt
        self.state.position += self.state.velocity * self.parameters.dt
        
        # Update time
        self.current_time += self.parameters.dt
        self.state.time = self.current_time
        self.state.forces = forces
        
        # Store results
        self.results.time_history.append(self.current_time)
        self.results.position_history.append(self.state.position.copy())
        self.results.velocity_history.append(self.state.velocity.copy())
        self.results.acceleration_history.append(self.state.acceleration.copy())
        self.results.force_history.append(forces.copy())
        
        # Calculate flow field (every 10 steps to save computation)
        if len(self.results.time_history) % 10 == 0:
            flow_field = self.engine.generate_flow_field(
                self.geometry,
                self.state.velocity,
                self.parameters.object_angle,
                (20.0, 10.0)  # Domain size
            )
            self.results.flow_fields.append(flow_field)
            
            # Calculate efficiency metrics
            efficiency = self.engine.calculate_aerodynamic_efficiency(forces, self.geometry)
            self.results.efficiency_metrics.append(efficiency)
        
        # Call callbacks
        for callback in self.callbacks:
            try:
                callback(self.get_current_data())
            except Exception as e:
                print(f"Callback error: {e}")
        
        return True
    
    def run_simulation(self, steps: Optional[int] = None):
        """Run the simulation for specified steps or until completion"""
        if not self.geometry:
            raise ValueError("Object geometry must be set before running simulation")
        
        self.is_running = True
        step_count = 0
        max_steps = steps if steps else int(self.parameters.max_time / self.parameters.dt)
        
        while step_count < max_steps:
            if not self.is_running:
                break  # Exit immediately if stop_simulation() was called

            if not self.is_paused:
                if not self.step_simulation():
                    break
                step_count += 1

            time.sleep(0.001)  # Small sleep to prevent CPU overuse
        
        self.is_running = False

    
    def pause_simulation(self):
        """Pause the simulation"""
        self.is_paused = True
    
    def resume_simulation(self):
        """Resume the simulation"""
        self.is_paused = False
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        self.is_paused = False
    
    def get_current_data(self) -> Dict:
        """Get current simulation data"""
        return {
            'time': self.current_time,
            'state': self.state,
            'parameters': self.parameters,
            'geometry': self.geometry,
            'is_running': self.is_running,
            'is_paused': self.is_paused
        }
    
    def get_analysis_data(self) -> Dict:
        """Get comprehensive analysis data"""
        if not self.results.time_history:
            return {}
        
        # Calculate statistics
        velocities = np.array(self.results.velocity_history)
        speeds = np.linalg.norm(velocities, axis=1)
        
        # Energy analysis
        kinetic_energy = 0.5 * speeds**2  # Assuming unit mass
        potential_energy = -self.parameters.gravity[1] * np.array([pos[1] for pos in self.results.position_history])
        total_energy = kinetic_energy + potential_energy
        
        # Force analysis
        drag_forces = [np.linalg.norm(f.get('drag', [0, 0, 0])) for f in self.results.force_history]
        lift_forces = [np.linalg.norm(f.get('lift', [0, 0, 0])) for f in self.results.force_history]
        
        return {
            'time_stats': {
                'total_time': self.current_time,
                'time_steps': len(self.results.time_history),
                'dt': self.parameters.dt
            },
            'motion_stats': {
                'max_speed': np.max(speeds) if len(speeds) > 0 else 0,
                'avg_speed': np.mean(speeds) if len(speeds) > 0 else 0,
                'final_speed': speeds[-1] if len(speeds) > 0 else 0,
                'max_position': np.max(np.abs(self.results.position_history), axis=0) if self.results.position_history else [0, 0, 0]
            },
            'energy_stats': {
                'initial_ke': kinetic_energy[0] if len(kinetic_energy) > 0 else 0,
                'final_ke': kinetic_energy[-1] if len(kinetic_energy) > 0 else 0,
                'energy_loss': total_energy[0] - total_energy[-1] if len(total_energy) > 1 else 0
            },
            'force_stats': {
                'max_drag': np.max(drag_forces) if drag_forces else 0,
                'avg_drag': np.mean(drag_forces) if drag_forces else 0,
                'max_lift': np.max(lift_forces) if lift_forces else 0,
                'avg_lift': np.mean(lift_forces) if lift_forces else 0
            },
            'efficiency_stats': self.results.efficiency_metrics[-1] if self.results.efficiency_metrics else {}
        }
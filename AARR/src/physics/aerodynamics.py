"""
Advanced Aerodynamics Physics Engine
Handles air flow simulation, drag calculations, and aerodynamic analysis
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math

class ObjectType(Enum):
    JET = "jet"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    CUBE = "cube"
    AIRFOIL = "airfoil"
    CUSTOM = "custom"

@dataclass
class AirProperties:
    """Air properties for simulation"""
    density: float = 1.225  # kg/m³ at sea level
    viscosity: float = 1.81e-5  # Pa·s
    temperature: float = 288.15  # K (15°C)
    pressure: float = 101325  # Pa
    speed_of_sound: float = 343  # m/s

@dataclass
class ObjectGeometry:
    """Object geometry properties"""
    length: float
    width: float
    height: float
    frontal_area: float
    surface_area: float
    volume: float
    object_type: ObjectType
    mesh: Optional[object] = None  # Custom mesh data
    mesh_file: Optional[str] = None  # Path to mesh file

@dataclass
class SimulationState:
    """Current simulation state"""
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    angular_velocity: np.ndarray
    time: float
    forces: Dict[str, np.ndarray]
    moments: Dict[str, np.ndarray]

class AerodynamicsEngine:
    """Advanced aerodynamics simulation engine"""
    
    def __init__(self):
        self.air_props = AirProperties()
        self.dt = 0.001  # Time step
        self.grid_size = (100, 100)  # Flow field grid
        self.flow_field = None
        self.pressure_field = None
        self.velocity_field = None
        
    def calculate_reynolds_number(self, velocity: float, characteristic_length: float) -> float:
        """Calculate Reynolds number"""
        return (self.air_props.density * velocity * characteristic_length) / self.air_props.viscosity
    
    def calculate_mach_number(self, velocity: float) -> float:
        """Calculate Mach number"""
        return velocity / self.air_props.speed_of_sound
    
    def get_drag_coefficient(self, obj_type: ObjectType, reynolds: float, mach: float, angle: float) -> float:
        """Calculate drag coefficient based on object type and flow conditions"""
        angle_rad = math.radians(angle)
        
        if obj_type == ObjectType.JET:
            # Jet aircraft drag coefficient (simplified)
            base_cd = 0.02  # Very low drag for streamlined jet
            # Angle of attack effect
            induced_drag = 0.1 * (angle_rad ** 2)
            # Mach number effects
            if mach > 0.8:
                wave_drag = 0.05 * ((mach - 0.8) ** 2)
            else:
                wave_drag = 0
            return base_cd + induced_drag + wave_drag
            
        elif obj_type == ObjectType.SPHERE:
            # Sphere drag coefficient
            if reynolds < 1:
                return 24 / reynolds  # Stokes flow
            elif reynolds < 1000:
                return 24 / reynolds * (1 + 0.15 * (reynolds ** 0.687))
            else:
                return 0.44  # Turbulent flow
                
        elif obj_type == ObjectType.CYLINDER:
            # Cylinder drag coefficient
            if reynolds < 1:
                return 8 * math.pi / reynolds
            elif reynolds < 40:
                return 1.0
            elif reynolds < 1000:
                return 1.2
            else:
                return 0.3
                
        elif obj_type == ObjectType.CUBE:
            # Cube drag coefficient
            return 1.05 + 0.2 * abs(math.sin(2 * angle_rad))
            
        elif obj_type == ObjectType.AIRFOIL:
            # Airfoil drag coefficient
            base_cd = 0.01
            induced_drag = 0.05 * (angle_rad ** 2)
            return base_cd + induced_drag
            
        return 0.5  # Default
    
    def calculate_lift_coefficient(self, obj_type: ObjectType, angle: float, reynolds: float) -> float:
        """Calculate lift coefficient"""
        angle_rad = math.radians(angle)
        
        if obj_type == ObjectType.JET:
            # Simplified jet lift
            return 0.8 * math.sin(2 * angle_rad) * (1 - abs(angle_rad) / math.pi)
        elif obj_type == ObjectType.AIRFOIL:
            # Airfoil lift (simplified)
            return 2 * math.pi * angle_rad * (1 - abs(angle_rad) / (math.pi/4))
        else:
            # Minimal lift for non-lifting bodies
            return 0.1 * math.sin(2 * angle_rad)
    
    def calculate_forces(self, geometry: ObjectGeometry, velocity: np.ndarray, 
                        angle: float, wind_velocity: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate all aerodynamic forces"""
        # Relative velocity (object velocity relative to air)
        relative_velocity = velocity - wind_velocity
        speed = np.linalg.norm(relative_velocity)
        
        if speed < 1e-6:
            return {
                'drag': np.zeros(3),
                'lift': np.zeros(3),
                'side_force': np.zeros(3),
                'total': np.zeros(3)
            }
        
        # Unit vector in direction of relative velocity
        velocity_unit = relative_velocity / speed
        
        # Calculate coefficients
        reynolds = self.calculate_reynolds_number(speed, geometry.length)
        mach = self.calculate_mach_number(speed)
        cd = self.get_drag_coefficient(geometry.object_type, reynolds, mach, angle)
        cl = self.calculate_lift_coefficient(geometry.object_type, angle, reynolds)
        
        # Dynamic pressure
        q = 0.5 * self.air_props.density * speed ** 2
        
        # Drag force (opposite to velocity direction)
        drag_magnitude = cd * geometry.frontal_area * q
        drag_force = -drag_magnitude * velocity_unit
        
        # Lift force (perpendicular to velocity, in the lift direction)
        # Simplified: assume lift is in the y-direction
        lift_magnitude = cl * geometry.frontal_area * q
        if abs(velocity_unit[0]) > 0.1:  # Avoid division by zero
            lift_direction = np.array([0, 1, 0])  # Simplified lift direction
        else:
            lift_direction = np.array([1, 0, 0])
        lift_force = lift_magnitude * lift_direction
        
        # Side force (simplified)
        side_force = np.zeros(3)
        
        total_force = drag_force + lift_force + side_force
        
        return {
            'drag': drag_force,
            'lift': lift_force,
            'side_force': side_force,
            'total': total_force,
            'coefficients': {'cd': cd, 'cl': cl, 'reynolds': reynolds, 'mach': mach}
        }
    
    def generate_flow_field(self, geometry: ObjectGeometry, velocity: np.ndarray, 
                           angle: float, domain_size: Tuple[float, float]) -> Dict:
        """Generate flow field around object"""
        x_max, y_max = domain_size
        x = np.linspace(-x_max/2, x_max/2, self.grid_size[0])
        y = np.linspace(-y_max/2, y_max/2, self.grid_size[1])
        X, Y = np.meshgrid(x, y)
        
        # Simplified flow field calculation
        # This is a basic potential flow approximation
        speed = np.linalg.norm(velocity[:2])  # 2D projection
        
        # Object center (assume at origin)
        obj_x, obj_y = 0, 0
        obj_radius = max(geometry.width, geometry.height) / 2
        
        # Distance from object center
        R = np.sqrt((X - obj_x)**2 + (Y - obj_y)**2)
        
        # Avoid singularity at object center
        R = np.maximum(R, obj_radius)
        
        # Potential flow around cylinder (simplified)
        # Stream function for flow around cylinder
        theta = np.arctan2(Y - obj_y, X - obj_x)
        
        # Velocity components (potential flow)
        u = speed * (1 - (obj_radius/R)**2 * np.cos(2*theta))
        v = -speed * (obj_radius/R)**2 * np.sin(2*theta)
        
        # Pressure field (Bernoulli's equation)
        velocity_magnitude = np.sqrt(u**2 + v**2)
        pressure = self.air_props.pressure + 0.5 * self.air_props.density * (speed**2 - velocity_magnitude**2)
        
        # Streamlines
        streamlines_x = []
        streamlines_y = []
        
        # Generate streamlines
        for start_y in np.linspace(-y_max/3, y_max/3, 10):
            if abs(start_y) > obj_radius * 1.5:  # Avoid object
                sx, sy = self._trace_streamline(x, y, u, v, -x_max/2, start_y, x_max)
                streamlines_x.append(sx)
                streamlines_y.append(sy)
        
        return {
            'x': X,
            'y': Y,
            'u': u,
            'v': v,
            'pressure': pressure,
            'velocity_magnitude': velocity_magnitude,
            'streamlines_x': streamlines_x,
            'streamlines_y': streamlines_y
        }
    
    def _trace_streamline(self, x_grid, y_grid, u, v, start_x, start_y, max_x):
        """Trace a streamline through the flow field"""
        dt = 0.01
        max_steps = 1000
        
        sx = [start_x]
        sy = [start_y]
        
        current_x, current_y = start_x, start_y
        
        for _ in range(max_steps):
            if current_x > max_x or current_x < -max_x:
                break
                
            # Interpolate velocity at current position
            try:
                # Simple nearest neighbor interpolation
                i = np.argmin(np.abs(x_grid - current_x))
                j = np.argmin(np.abs(y_grid - current_y))
                
                if 0 <= i < len(u[0]) and 0 <= j < len(u):
                    vel_x = u[j, i]
                    vel_y = v[j, i]
                    
                    # Update position
                    current_x += vel_x * dt
                    current_y += vel_y * dt
                    
                    sx.append(current_x)
                    sy.append(current_y)
                else:
                    break
            except:
                break
        
        return sx, sy
    
    def calculate_aerodynamic_efficiency(self, forces: Dict, geometry: ObjectGeometry) -> Dict:
        """Calculate aerodynamic efficiency metrics"""
        drag_force = np.linalg.norm(forces['drag'])
        lift_force = np.linalg.norm(forces['lift'])
        
        # Lift-to-drag ratio
        if drag_force > 1e-6:
            lift_to_drag = lift_force / drag_force
        else:
            lift_to_drag = float('inf')
        
        # Drag area
        drag_area = geometry.frontal_area
        
        # Fineness ratio (for streamlined objects)
        fineness_ratio = geometry.length / max(geometry.width, geometry.height)
        
        return {
            'lift_to_drag_ratio': lift_to_drag,
            'drag_area': drag_area,
            'fineness_ratio': fineness_ratio,
            'drag_coefficient': forces.get('coefficients', {}).get('cd', 0),
            'lift_coefficient': forces.get('coefficients', {}).get('cl', 0)
        }
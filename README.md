# Advanced Aerodynamic Simulation System

A comprehensive aerodynamic simulation system with a beautiful GUI for analyzing air resistance, flow visualization, and aerodynamic performance of various objects including jets, spheres, cylinders, and custom shapes.

## Features

### 🚀 Advanced Physics Engine
- **Real-time aerodynamic calculations** with drag and lift forces
- **Reynolds number and Mach number** computations
- **Multiple object types**: Jets, spheres, cylinders, cubes, airfoils, and custom shapes
- **Angle of attack effects** with user-controllable orientation
- **Wind direction and speed** simulation from any angle
- **Turbulence modeling** with adjustable intensity
- **Atmospheric conditions** (density, temperature, pressure)

### 🎨 Beautiful Modern GUI
- **Dark theme interface** optimized for Windows
- **Real-time data visualization** with multiple plot types
- **Flow field visualization** with streamlines and pressure fields
- **Interactive controls** for all simulation parameters
- **Comprehensive data display** with live updates
- **Professional analysis tools** with efficiency metrics

### 📊 Advanced Data Output
- **Real-time monitoring**: Position, velocity, acceleration, forces
- **Aerodynamic coefficients**: Drag (Cd), Lift (Cl), L/D ratio
- **Flow properties**: Reynolds number, Mach number, dynamic pressure
- **Energy analysis**: Kinetic, potential, and energy loss calculations
- **Performance metrics**: Maximum/average forces, speeds, displacements
- **Efficiency ratings**: Aerodynamic efficiency, streamlining effectiveness
- **Statistical analysis**: Complete simulation statistics and trends
- **Live plotting**: Real-time data visualization with multiple plot types
- **Data persistence**: Plots remain available after simulation stops

### 🌊 Flow Visualization
- **Streamline visualization** showing air flow patterns
- **Velocity field vectors** with magnitude and direction
- **Pressure field contours** with color-coded intensity
- **Combined visualizations** for comprehensive analysis
- **Object representation** in the flow field
- **Real-time updates** during simulation

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (optimized for Windows)

### Quick Install
```bash
# Clone or download the repository
cd Areo

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Development Install
```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

## Usage

### Starting the Application
```bash
python main.py
```

### Basic Workflow
1. **Configure Object**: Select object type (Jet, Sphere, etc.) and set dimensions
2. **Set Environment**: Configure wind speed, direction, and atmospheric conditions
3. **Run Simulation**: Click Start to begin real-time simulation
4. **Analyze Results**: View live data, plots, and flow visualizations
5. **Export Data**: Save results for further analysis

### Object Types
- **Jet Aircraft**: Streamlined aircraft with low drag coefficient
- **Sphere**: Classic sphere with Reynolds number-dependent drag
- **Cylinder**: Cylindrical object with orientation effects
- **Cube**: Bluff body with high drag characteristics
- **Airfoil**: Wing-like shape with lift generation
- **Custom**: User-defined geometry
- **Import 3D Mesh**: Load custom 3D models from OBJ, STL, PLY files

### 🎯 3D Geometry Import
- **Multiple file formats**: OBJ, STL, PLY support
- **Automatic mesh analysis**: Surface area, volume, frontal area calculation
- **Mesh optimization**: Automatic validation and optimization
- **Custom scaling**: Resize imported models to any scale
- **Aerodynamic properties**: Automatic calculation of drag/lift characteristics
- **Real-time preview**: Mesh statistics and properties display
- **Sample models**: Included aircraft and sphere models for testing

### Visualization Modes
- **Streamlines**: Air flow paths around the object
- **Velocity Field**: Vector field showing air velocity
- **Pressure Field**: Pressure distribution with contours
- **Velocity Magnitude**: Speed visualization with color mapping
- **Combined View**: Multiple visualizations overlaid

### Plot Types
- **Velocity vs Time**: Real-time velocity components and magnitude
- **Forces vs Time**: Drag, lift, and total force evolution
- **Position vs Time**: Object trajectory components
- **Energy vs Time**: Kinetic, potential, and total energy
- **Coefficients vs Time**: Aerodynamic coefficients (Cd, Cl)
- **Trajectory (2D)**: 2D path visualization with start/end markers
- **Phase Space**: Position vs velocity phase plots

## Technical Details

### Physics Model
The simulation uses advanced aerodynamic principles:
- **Navier-Stokes approximations** for flow field calculation
- **Empirical drag models** based on object geometry and Reynolds number
- **Lift calculations** using angle of attack and airfoil theory
- **Compressibility effects** for high-speed flows (Mach number)
- **Turbulence modeling** with statistical fluctuations

### Numerical Methods
- **Euler integration** for time stepping
- **Potential flow theory** for flow field visualization
- **Finite difference approximations** for spatial derivatives
- **Adaptive time stepping** for stability

### Performance
- **Real-time simulation** at 60+ FPS
- **Efficient algorithms** optimized for interactive use
- **Multi-threaded computation** for smooth GUI responsiveness
- **Memory-efficient** data structures for long simulations

## Data Export

The system provides comprehensive data output:

### Real-time Data
- Position, velocity, acceleration vectors
- Force components (drag, lift, total)
- Aerodynamic coefficients (Cd, Cl, L/D)
- Flow properties (Reynolds, Mach, dynamic pressure)

### Analysis Data
- Statistical summaries (max, min, average values)
- Energy analysis (kinetic, potential, losses)
- Efficiency metrics (aerodynamic performance)
- Time-series data for all parameters

### Visualization Data
- Flow field grids (velocity, pressure)
- Streamline coordinates
- Contour data for plotting
- Object geometry information

## Examples

### Jet Aircraft Analysis
```python
# Configure a jet aircraft
object_type = "Jet Aircraft"
length = 15.0  # meters
width = 3.0    # meters  
height = 2.0   # meters
angle_of_attack = 5.0  # degrees

# Set wind conditions
wind_speed = 50.0  # m/s
wind_angle = 180.0  # head-on wind

# Expected results:
# - Low drag coefficient (~0.02-0.05)
# - Significant lift at angle of attack
# - High L/D ratio for efficiency
```

### Sphere Drop Test
```python
# Configure a sphere
object_type = "Sphere"
diameter = 1.0  # meters
mass = 10.0     # kg

# Set conditions
wind_speed = 0.0    # still air
gravity = True      # include gravity

# Expected results:
# - Terminal velocity calculation
# - Reynolds number transition effects
# - Classic sphere drag curve
```

### Custom 3D Geometry Import
```python
# Using the GUI:
# 1. Select "Import 3D Mesh" from Object Type dropdown
# 2. Click "Import 3D Geometry..." button
# 3. Choose your OBJ, STL, or PLY file
# 4. Configure scaling and aerodynamic properties
# 5. Import and run simulation

# Supported file formats:
# - OBJ: Wavefront OBJ files with vertices and faces
# - STL: Stereolithography files (ASCII and Binary)
# - PLY: Polygon File Format

# Sample models included:
# - sample_models/simple_aircraft.obj
# - sample_models/sphere.obj
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **GUI Not Appearing**: Check PySide6 installation
3. **Slow Performance**: Reduce time step or grid resolution
4. **Memory Issues**: Clear data periodically for long simulations
5. **Plots Not Showing**: Data plots update automatically during and after simulation
6. **3D Import Fails**: Ensure mesh files are valid and not corrupted
7. **Large Mesh Files**: Consider mesh optimization for files with >10k vertices

### Performance Tips
- Use appropriate time steps (0.001-0.01 seconds)
- Limit simulation duration for real-time analysis
- Close unused visualization tabs
- Monitor system resources during long runs

## Contributing

We welcome contributions! Please see our contributing guidelines:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Aerodynamic theory based on classical fluid mechanics
- GUI framework powered by PySide6
- Visualization using matplotlib and pyqtgraph
- Numerical computations with NumPy and SciPy

## Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description
4. Contact the development team

---

**Advanced Aerodynamic Simulation System v1.0**  
*Professional-grade aerodynamic analysis with beautiful visualization*

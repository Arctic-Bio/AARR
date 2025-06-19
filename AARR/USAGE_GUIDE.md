# Advanced Aerodynamic Simulation System - Usage Guide

## Quick Start

### 1. Running the Application
```bash
# Install dependencies
pip install PySide6 numpy matplotlib scipy pyqtgraph

# Run the application
python main.py

# Or use the batch file
install_and_run.bat
```

### 2. Basic Simulation
1. **Start the application**
2. **Configure object** in the "Object" tab
3. **Set environment** in the "Environment" tab  
4. **Click "Start"** in the "Simulation" tab
5. **View results** in the visualization tabs

## Data Plotting Features

### Real-time Plotting
- **Automatic updates**: Plots update during simulation
- **Data persistence**: Plots remain after simulation stops
- **Multiple plot types**: Switch between different visualizations
- **Error handling**: Clear error messages for data issues

### Available Plot Types

#### 1. Velocity vs Time
- Shows X, Y, Z velocity components
- Displays velocity magnitude
- Real-time updates during simulation

#### 2. Forces vs Time  
- Drag force magnitude
- Lift force magnitude
- Total force magnitude
- Aerodynamic coefficients

#### 3. Position vs Time
- X, Y, Z position components
- Object trajectory over time
- Useful for projectile motion

#### 4. Energy vs Time
- Kinetic energy
- Potential energy  
- Total energy
- Energy loss analysis

#### 5. Coefficients vs Time
- Drag coefficient (Cd)
- Lift coefficient (Cl)
- Reynolds number evolution

#### 6. Trajectory (2D)
- 2D path visualization
- Start and end markers
- Useful for ballistic analysis

#### 7. Phase Space
- Position vs velocity plots
- System dynamics visualization
- Stability analysis

### Troubleshooting Plots
- **No data showing**: Start a simulation first
- **Empty plots**: Check simulation parameters
- **Error messages**: Verify object configuration

## 3D Geometry Import

### Supported File Formats

#### OBJ Files (.obj)
- Wavefront OBJ format
- Supports vertices, faces, normals
- Text-based, human-readable
- Best for complex models

#### STL Files (.stl)
- Stereolithography format
- Binary and ASCII variants
- Common in 3D printing
- Good for solid objects

#### PLY Files (.ply)
- Polygon File Format
- Supports vertex colors
- Research-oriented format
- Good for scanned data

### Import Process

#### Step 1: Select Import Mode
1. Go to **Object** tab
2. Select **"Import 3D Mesh"** from dropdown
3. Click **"Import 3D Geometry..."** button

#### Step 2: File Selection
1. Browse for your 3D file
2. Supported formats shown in dialog
3. Preview file information

#### Step 3: Mesh Properties
- **Vertices**: Number of mesh points
- **Faces**: Number of triangular faces
- **Dimensions**: Length × Width × Height
- **Surface Area**: Total mesh surface
- **Volume**: Enclosed volume
- **Frontal Area**: Cross-sectional area

#### Step 4: Transform Settings
- **Scale Factor**: Resize the mesh (0.001 to 1000)
- **Center Mesh**: Automatically center at origin
- **Object Type**: Aerodynamic classification
- **Reference Area**: For coefficient calculations

#### Step 5: Aerodynamic Settings
- **Custom Geometry**: General aerodynamic properties
- **Aircraft-like**: Streamlined body characteristics
- **Bluff Body**: High-drag object properties
- **Streamlined Body**: Low-drag characteristics

#### Step 6: Advanced Options
- **Optimize mesh**: Improve mesh quality
- **Validate mesh**: Check for errors
- **Custom reference area**: Override automatic calculation

### Sample Models

#### Simple Aircraft (simple_aircraft.obj)
- Basic aircraft shape
- 18 vertices, 32 faces
- Good for testing aerodynamics
- Includes fuselage and wings

#### Sphere (sphere.obj)
- Icosphere approximation
- 12 vertices, 20 faces
- Perfect for validation
- Known aerodynamic properties

### Creating Your Own Models

#### Using Blender
1. Create or import your model
2. Ensure proper scale (meters)
3. Export as OBJ with these settings:
   - Include: Vertices, Faces
   - Forward: -Z Forward
   - Up: Y Up

#### Using CAD Software
1. Design your model
2. Export as STL or OBJ
3. Check units (should be meters)
4. Verify mesh quality

#### Mesh Quality Guidelines
- **Vertex count**: 100-10,000 for good performance
- **Face count**: 200-20,000 triangles
- **Watertight**: Closed surfaces for volume calculation
- **Manifold**: No holes or non-manifold edges
- **Scale**: Real-world dimensions in meters

### Aerodynamic Analysis

#### Automatic Calculations
- **Frontal Area**: Cross-section perpendicular to flow
- **Surface Area**: Total mesh surface
- **Volume**: Enclosed volume (if watertight)
- **Drag Coefficient**: Based on shape and Reynolds number
- **Lift Coefficient**: For lifting surfaces

#### Custom Properties
- **Reference Area**: Override automatic calculation
- **Aerodynamic Type**: Affects coefficient calculations
- **Scale Factor**: Resize without changing file

## Advanced Features

### Mesh Optimization
- **Automatic validation**: Checks for common issues
- **Error reporting**: Clear messages for problems
- **Performance optimization**: Reduces complexity if needed

### Real-time Preview
- **Mesh statistics**: Comprehensive property display
- **Dimension display**: Accurate measurements
- **Error detection**: Validation results

### Integration with Simulation
- **Seamless workflow**: Import and simulate immediately
- **Automatic configuration**: Sets appropriate parameters
- **Performance monitoring**: Tracks simulation speed

## Best Practices

### For Plotting
1. **Run sufficient simulation time** for meaningful data
2. **Use appropriate time steps** (0.001-0.01 seconds)
3. **Monitor data quality** during simulation
4. **Save important results** before resetting

### For 3D Import
1. **Validate meshes** before import
2. **Use appropriate scale** (real-world meters)
3. **Check mesh quality** for performance
4. **Test with sample models** first

### For Performance
1. **Limit mesh complexity** for real-time simulation
2. **Use appropriate time steps** for stability
3. **Monitor memory usage** for long simulations
4. **Close unused visualization tabs**

## Example Workflows

### Analyzing a Custom Aircraft
1. **Create/obtain** aircraft OBJ file
2. **Import geometry** with aircraft-like properties
3. **Set wind conditions** (headwind, crosswind)
4. **Configure angle of attack**
5. **Run simulation** and analyze forces
6. **Plot coefficients** vs time
7. **Analyze L/D ratio** for efficiency

### Projectile Motion Study
1. **Import sphere** or custom projectile
2. **Set initial velocity** and angle
3. **Enable gravity** in environment
4. **Run simulation** until impact
5. **Plot trajectory** in 2D
6. **Analyze energy** conservation
7. **Study drag effects** on range

### Comparative Analysis
1. **Import multiple geometries**
2. **Run identical conditions** for each
3. **Compare drag coefficients**
4. **Analyze efficiency metrics**
5. **Plot comparative results**
6. **Document findings**

## Troubleshooting

### Import Issues
- **File not found**: Check file path and permissions
- **Unsupported format**: Use OBJ, STL, or PLY
- **Corrupted mesh**: Validate in 3D software first
- **Too large**: Reduce mesh complexity

### Simulation Issues
- **No data**: Check object configuration
- **Poor performance**: Reduce mesh complexity
- **Unstable results**: Decrease time step
- **Memory errors**: Restart application

### Plotting Issues
- **Empty plots**: Ensure simulation has run
- **Missing data**: Check simulation parameters
- **Error messages**: Verify object geometry
- **Performance**: Close unused plot tabs

## Support

For additional help:
1. **Check sample models** for reference
2. **Run test script**: `python test_system.py`
3. **Verify installation**: All dependencies installed
4. **Check documentation**: README.md for details

---

**Advanced Aerodynamic Simulation System v1.0**  
*Professional 3D aerodynamic analysis with custom geometry support*
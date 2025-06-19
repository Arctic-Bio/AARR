"""
3D Mesh Loader for Various File Formats
Supports OBJ, STL, PLY, and other common 3D formats
"""

import numpy as np
import os
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
import struct
import re

@dataclass
class Mesh:
    """3D Mesh data structure"""
    vertices: np.ndarray  # Nx3 array of vertex positions
    faces: np.ndarray     # Mx3 array of face indices
    normals: Optional[np.ndarray] = None  # Nx3 array of vertex normals
    texcoords: Optional[np.ndarray] = None  # Nx2 array of texture coordinates
    name: str = "Unnamed"
    
    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get bounding box of the mesh"""
        if len(self.vertices) == 0:
            return np.zeros(3), np.zeros(3)
        return np.min(self.vertices, axis=0), np.max(self.vertices, axis=0)
    
    def get_dimensions(self) -> np.ndarray:
        """Get dimensions (length, width, height) of the mesh"""
        min_bounds, max_bounds = self.get_bounds()
        return max_bounds - min_bounds
    
    def get_center(self) -> np.ndarray:
        """Get center point of the mesh"""
        min_bounds, max_bounds = self.get_bounds()
        return (min_bounds + max_bounds) / 2
    
    def get_volume(self) -> float:
        """Calculate approximate volume using bounding box"""
        dimensions = self.get_dimensions()
        return np.prod(dimensions)
    
    def get_surface_area(self) -> float:
        """Calculate approximate surface area"""
        if len(self.faces) == 0:
            return 0.0
        
        area = 0.0
        for face in self.faces:
            if len(face) >= 3:
                # Triangle area using cross product
                v1 = self.vertices[face[1]] - self.vertices[face[0]]
                v2 = self.vertices[face[2]] - self.vertices[face[0]]
                area += 0.5 * np.linalg.norm(np.cross(v1, v2))
        
        return area
    
    def get_frontal_area(self, direction: np.ndarray = np.array([1, 0, 0])) -> float:
        """Calculate frontal area in given direction"""
        # Project vertices onto plane perpendicular to direction
        direction = direction / np.linalg.norm(direction)
        
        # Create orthogonal basis
        if abs(direction[0]) < 0.9:
            u = np.cross(direction, np.array([1, 0, 0]))
        else:
            u = np.cross(direction, np.array([0, 1, 0]))
        u = u / np.linalg.norm(u)
        v = np.cross(direction, u)
        
        # Project vertices
        projected = np.column_stack([
            np.dot(self.vertices, u),
            np.dot(self.vertices, v)
        ])
        
        # Calculate 2D bounding box area
        min_proj = np.min(projected, axis=0)
        max_proj = np.max(projected, axis=0)
        
        return (max_proj[0] - min_proj[0]) * (max_proj[1] - min_proj[1])

class MeshLoader:
    """Loader for various 3D mesh file formats"""
    
    @staticmethod
    def load_mesh(filepath: str) -> Optional[Mesh]:
        """Load mesh from file based on extension"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.obj':
            return MeshLoader.load_obj(filepath)
        elif ext == '.stl':
            return MeshLoader.load_stl(filepath)
        elif ext == '.ply':
            return MeshLoader.load_ply(filepath)
        elif ext in ['.off', '.3ds', '.dae', '.x3d']:
            # For advanced formats, we'll provide basic support
            return MeshLoader.load_generic(filepath)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    @staticmethod
    def load_obj(filepath: str) -> Mesh:
        """Load Wavefront OBJ file"""
        vertices = []
        faces = []
        normals = []
        texcoords = []
        
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                if parts[0] == 'v':  # Vertex
                    vertices.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vn':  # Vertex normal
                    normals.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vt':  # Texture coordinate
                    texcoords.append([float(x) for x in parts[1:3]])
                elif parts[0] == 'f':  # Face
                    face_vertices = []
                    for vertex_data in parts[1:]:
                        # Handle different face formats: v, v/vt, v/vt/vn, v//vn
                        vertex_indices = vertex_data.split('/')
                        vertex_idx = int(vertex_indices[0]) - 1  # OBJ uses 1-based indexing
                        face_vertices.append(vertex_idx)
                    
                    # Convert to triangles if necessary
                    if len(face_vertices) == 3:
                        faces.append(face_vertices)
                    elif len(face_vertices) == 4:
                        # Split quad into two triangles
                        faces.append([face_vertices[0], face_vertices[1], face_vertices[2]])
                        faces.append([face_vertices[0], face_vertices[2], face_vertices[3]])
        
        mesh = Mesh(
            vertices=np.array(vertices) if vertices else np.empty((0, 3)),
            faces=np.array(faces) if faces else np.empty((0, 3), dtype=int),
            normals=np.array(normals) if normals else None,
            texcoords=np.array(texcoords) if texcoords else None,
            name=os.path.basename(filepath)
        )
        
        return mesh
    
    @staticmethod
    def load_stl(filepath: str) -> Mesh:
        """Load STL file (both ASCII and binary)"""
        with open(filepath, 'rb') as file:
            # Check if binary or ASCII
            header = file.read(80)
            if b'solid' in header[:5]:
                # Might be ASCII, check further
                file.seek(0)
                try:
                    content = file.read().decode('utf-8')
                    if 'facet normal' in content:
                        return MeshLoader._load_stl_ascii(filepath)
                except:
                    pass
            
            # Binary STL
            return MeshLoader._load_stl_binary(filepath)
    
    @staticmethod
    def _load_stl_ascii(filepath: str) -> Mesh:
        """Load ASCII STL file"""
        vertices = []
        faces = []
        
        with open(filepath, 'r') as file:
            vertex_count = 0
            current_face = []
            
            for line in file:
                line = line.strip()
                if line.startswith('vertex'):
                    coords = [float(x) for x in line.split()[1:4]]
                    vertices.append(coords)
                    current_face.append(vertex_count)
                    vertex_count += 1
                    
                    if len(current_face) == 3:
                        faces.append(current_face)
                        current_face = []
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name=os.path.basename(filepath)
        )
    
    @staticmethod
    def _load_stl_binary(filepath: str) -> Mesh:
        """Load binary STL file"""
        vertices = []
        faces = []
        
        with open(filepath, 'rb') as file:
            # Skip header
            file.seek(80)
            
            # Read number of triangles
            num_triangles = struct.unpack('<I', file.read(4))[0]
            
            vertex_count = 0
            for i in range(num_triangles):
                # Skip normal vector (3 floats)
                file.read(12)
                
                # Read 3 vertices (9 floats)
                face_vertices = []
                for j in range(3):
                    vertex = struct.unpack('<fff', file.read(12))
                    vertices.append(vertex)
                    face_vertices.append(vertex_count)
                    vertex_count += 1
                
                faces.append(face_vertices)
                
                # Skip attribute byte count
                file.read(2)
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name=os.path.basename(filepath)
        )
    
    @staticmethod
    def load_ply(filepath: str) -> Mesh:
        """Load PLY file (basic support)"""
        vertices = []
        faces = []
        
        with open(filepath, 'r') as file:
            # Read header
            line = file.readline().strip()
            if line != 'ply':
                raise ValueError("Not a valid PLY file")
            
            vertex_count = 0
            face_count = 0
            
            # Parse header
            while True:
                line = file.readline().strip()
                if line == 'end_header':
                    break
                elif line.startswith('element vertex'):
                    vertex_count = int(line.split()[-1])
                elif line.startswith('element face'):
                    face_count = int(line.split()[-1])
            
            # Read vertices
            for i in range(vertex_count):
                line = file.readline().strip()
                coords = [float(x) for x in line.split()[:3]]
                vertices.append(coords)
            
            # Read faces
            for i in range(face_count):
                line = file.readline().strip()
                parts = line.split()
                num_vertices = int(parts[0])
                face_indices = [int(parts[j+1]) for j in range(min(3, num_vertices))]
                if len(face_indices) == 3:
                    faces.append(face_indices)
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name=os.path.basename(filepath)
        )
    
    @staticmethod
    def load_generic(filepath: str) -> Mesh:
        """Basic loader for other formats (placeholder)"""
        # This is a placeholder for more advanced formats
        # In a full implementation, you'd use libraries like Open3D or trimesh
        raise NotImplementedError(f"Generic loader not implemented for {filepath}")
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """Get list of supported file formats"""
        return ['.obj', '.stl', '.ply']
    
    @staticmethod
    def create_primitive_mesh(primitive_type: str, **kwargs) -> Mesh:
        """Create primitive mesh shapes"""
        if primitive_type == 'sphere':
            return MeshLoader._create_sphere(**kwargs)
        elif primitive_type == 'cube':
            return MeshLoader._create_cube(**kwargs)
        elif primitive_type == 'cylinder':
            return MeshLoader._create_cylinder(**kwargs)
        elif primitive_type == 'cone':
            return MeshLoader._create_cone(**kwargs)
        else:
            raise ValueError(f"Unknown primitive type: {primitive_type}")
    
    @staticmethod
    def _create_sphere(radius: float = 1.0, subdivisions: int = 20) -> Mesh:
        """Create sphere mesh"""
        vertices = []
        faces = []
        
        # Generate vertices using spherical coordinates
        for i in range(subdivisions + 1):
            theta = np.pi * i / subdivisions  # 0 to pi
            for j in range(subdivisions * 2):
                phi = 2 * np.pi * j / (subdivisions * 2)  # 0 to 2pi
                
                x = radius * np.sin(theta) * np.cos(phi)
                y = radius * np.cos(theta)
                z = radius * np.sin(theta) * np.sin(phi)
                
                vertices.append([x, y, z])
        
        # Generate faces
        for i in range(subdivisions):
            for j in range(subdivisions * 2):
                # Current quad vertices
                v1 = i * (subdivisions * 2) + j
                v2 = i * (subdivisions * 2) + (j + 1) % (subdivisions * 2)
                v3 = (i + 1) * (subdivisions * 2) + j
                v4 = (i + 1) * (subdivisions * 2) + (j + 1) % (subdivisions * 2)
                
                # Skip degenerate triangles at poles
                if i > 0:
                    faces.append([v1, v2, v3])
                if i < subdivisions - 1:
                    faces.append([v2, v4, v3])
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name="Sphere"
        )
    
    @staticmethod
    def _create_cube(size: float = 1.0) -> Mesh:
        """Create cube mesh"""
        s = size / 2
        vertices = np.array([
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # Bottom face
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # Top face
        ])
        
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Bottom
            [4, 7, 6], [4, 6, 5],  # Top
            [0, 4, 5], [0, 5, 1],  # Front
            [2, 6, 7], [2, 7, 3],  # Back
            [0, 3, 7], [0, 7, 4],  # Left
            [1, 5, 6], [1, 6, 2]   # Right
        ])
        
        return Mesh(vertices=vertices, faces=faces, name="Cube")
    
    @staticmethod
    def _create_cylinder(radius: float = 1.0, height: float = 2.0, subdivisions: int = 16) -> Mesh:
        """Create cylinder mesh"""
        vertices = []
        faces = []
        
        # Bottom center
        vertices.append([0, -height/2, 0])
        # Top center
        vertices.append([0, height/2, 0])
        
        # Bottom circle vertices
        for i in range(subdivisions):
            angle = 2 * np.pi * i / subdivisions
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append([x, -height/2, z])
        
        # Top circle vertices
        for i in range(subdivisions):
            angle = 2 * np.pi * i / subdivisions
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append([x, height/2, z])
        
        # Bottom faces
        for i in range(subdivisions):
            next_i = (i + 1) % subdivisions
            faces.append([0, 2 + next_i, 2 + i])
        
        # Top faces
        for i in range(subdivisions):
            next_i = (i + 1) % subdivisions
            faces.append([1, 2 + subdivisions + i, 2 + subdivisions + next_i])
        
        # Side faces
        for i in range(subdivisions):
            next_i = (i + 1) % subdivisions
            v1 = 2 + i
            v2 = 2 + next_i
            v3 = 2 + subdivisions + i
            v4 = 2 + subdivisions + next_i
            
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name="Cylinder"
        )
    
    @staticmethod
    def _create_cone(radius: float = 1.0, height: float = 2.0, subdivisions: int = 16) -> Mesh:
        """Create cone mesh"""
        vertices = []
        faces = []
        
        # Apex
        vertices.append([0, height/2, 0])
        # Base center
        vertices.append([0, -height/2, 0])
        
        # Base circle vertices
        for i in range(subdivisions):
            angle = 2 * np.pi * i / subdivisions
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            vertices.append([x, -height/2, z])
        
        # Base faces
        for i in range(subdivisions):
            next_i = (i + 1) % subdivisions
            faces.append([1, 2 + next_i, 2 + i])
        
        # Side faces
        for i in range(subdivisions):
            next_i = (i + 1) % subdivisions
            faces.append([0, 2 + i, 2 + next_i])
        
        return Mesh(
            vertices=np.array(vertices),
            faces=np.array(faces),
            name="Cone"
        )
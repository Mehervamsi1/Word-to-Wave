import bpy

# Select the object you want to generate a script for
obj = bpy.context.active_object

# Print object name
print(f"Creating object: {obj.name}")

# Print object location, rotation, and scale
print(f"Object location: {obj.location}")
print(f"Object rotation: {obj.rotation_euler}")
print(f"Object scale: {obj.scale}")

# Print mesh data
if obj.type == 'MESH':
    mesh = obj.data
    print(f"Mesh name: {mesh.name}")
    
    for vert in mesh.vertices:
        print(f"Vertex: {vert.co}")

    for edge in mesh.edges:
        print(f"Edge: {edge.vertices}")

    for poly in mesh.polygons:
        print(f"Polygon: {poly.vertices}")

# Print material data
for mat in obj.data.materials:
    print(f"Material: {mat.name}")

# Generate script
script = f"""
import bpy

# Add object
bpy.ops.mesh.primitive_cube_add(size=2)
obj = bpy.context.active_object
obj.name = "{obj.name}"

# Set location, rotation, and scale
obj.location = {tuple(obj.location)}
obj.rotation_euler = {tuple(obj.rotation_euler)}
obj.scale = {tuple(obj.scale)}

# Mesh data
mesh = obj.data
mesh.name = "{mesh.name}"
"""

# Add vertices
script += "\n# Vertices\n"
for vert in mesh.vertices:
    script += f"mesh.vertices.add(1)\nmesh.vertices[-1].co = {tuple(vert.co)}\n"

# Add edges
script += "\n# Edges\n"
for edge in mesh.edges:
    script += f"mesh.edges.add(1)\nmesh.edges[-1].vertices = {tuple(edge.vertices)}\n"

# Add polygons
script += "\n# Polygons\n"
for poly in mesh.polygons:
    script += f"mesh.polygons.add(1)\nmesh.polygons[-1].vertices = {tuple(poly.vertices)}\n"

# Add materials
script += "\n# Materials\n"
for mat in obj.data.materials:
    script += f'material = bpy.data.materials.new("{mat.name}")\nobj.data.materials.append(material)\n'

print(script)

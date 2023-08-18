import UniPy as up
import pygame
import math

class cube:
    def __init__(self):
        self.z = 0
        self.angle_x = 0
        self.angle_y = 45
        self.color = [255, 255, 0]
        self.light = up.GetModule("vector").vector()
    
    def rotate_point(self, x, y, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        new_x = x * c - y * s
        new_y = x * s + y * c
        return new_x, new_y

    def draw(self):
        half_width = self.this.width / 2
        half_height = self.this.height / 2
    
        # Calculate scale factor based on z-coordinate
        scale_factor = 1 + self.z / 1000.0  # You can adjust the divisor to control the scaling speed
    
        # Define cube's vertices with adjusted z-coordinate
        vertices = [
            (self.this.x - half_width * scale_factor, self.this.y - half_height * scale_factor, self.z - half_width * scale_factor),
            (self.this.x + half_width * scale_factor, self.this.y - half_height * scale_factor, self.z - half_width * scale_factor),
            (self.this.x + half_width * scale_factor, self.this.y + half_height * scale_factor, self.z - half_width * scale_factor),
            (self.this.x - half_width * scale_factor, self.this.y + half_height * scale_factor, self.z - half_width * scale_factor),
            (self.this.x - half_width * scale_factor, self.this.y - half_height * scale_factor, self.z + half_width * scale_factor),
            (self.this.x + half_width * scale_factor, self.this.y - half_height * scale_factor, self.z + half_width * scale_factor),
            (self.this.x + half_width * scale_factor, self.this.y + half_height * scale_factor, self.z + half_width * scale_factor),
            (self.this.x - half_width * scale_factor, self.this.y + half_height * scale_factor, self.z + half_width * scale_factor)
        ]
    
        rotated_vertices = []
        for vertex in vertices:
            # Rotate around X and Y axes
            rotated_x, rotated_z = self.rotate_point(vertex[0] - self.this.x, vertex[2] - self.z, self.angle_y)
            rotated_y, rotated_z = self.rotate_point(vertex[1] - self.this.y, rotated_z, self.angle_x)
            rotated_vertices.append((rotated_x + self.this.x, rotated_y + self.this.y, rotated_z + self.z))
    
        # Define cube's faces
        faces = [
            (0, 1, 2, 3),  # Front face
            (4, 5, 6, 7),  # Back face
            (0, 4, 7, 3),  # Left face
            (1, 5, 6, 2),  # Right face
            (0, 1, 5, 4),  # Top face
            (3, 2, 6, 7)   # Bottom face
        ]
    
        light_direction = (self.light.x - self.this.x, self.light.y - self.this.y, self.light.z - self.z)
        light_length = math.sqrt(light_direction[0] ** 2 + light_direction[1] ** 2 + light_direction[2] ** 2)
        normalized_light = (light_direction[0] / light_length, light_direction[1] / light_length, light_direction[2] / light_length)
    
        # Draw shaded faces
        sorted_faces = sorted(faces, key=lambda face: sum(rotated_vertices[vertex][2] for vertex in face), reverse=True)
        for face in sorted_faces:
            normal = (
                (rotated_vertices[face[1]][1] - rotated_vertices[face[0]][1]) * (rotated_vertices[face[2]][2] - rotated_vertices[face[0]][2])
                - (rotated_vertices[face[1]][2] - rotated_vertices[face[0]][2]) * (rotated_vertices[face[2]][1] - rotated_vertices[face[0]][1]),
                (rotated_vertices[face[1]][2] - rotated_vertices[face[0]][2]) * (rotated_vertices[face[2]][0] - rotated_vertices[face[0]][0])
                - (rotated_vertices[face[1]][0] - rotated_vertices[face[0]][0]) * (rotated_vertices[face[2]][2] - rotated_vertices[face[0]][2]),
                (rotated_vertices[face[1]][0] - rotated_vertices[face[0]][0]) * (rotated_vertices[face[2]][1] - rotated_vertices[face[0]][1])
                - (rotated_vertices[face[1]][1] - rotated_vertices[face[0]][1]) * (rotated_vertices[face[2]][0] - rotated_vertices[face[0]][0])
            )
            normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
            normalized_normal = (normal[0] / normal_length, normal[1] / normal_length, normal[2] / normal_length)
            brightness = max(0.3, min(normalized_normal[0] * normalized_light[0] + normalized_normal[1] * normalized_light[1] + normalized_normal[2] * normalized_light[2], 1))
    
            # Ensure color components are within the valid range (0 to 255)
            face_color = (
                min(int(self.color[0] * brightness), 255),
                min(int(self.color[1] * brightness), 255),
                min(int(self.color[2] * brightness), 255)
            )
    
            # Adjust vertices' z-coordinates based on z
            adjusted_vertices = [(vertex[0], vertex[1], vertex[2] + self.z - vertices[0][2]) for vertex in rotated_vertices]
    
            # Use adjusted_vertices for calculating projected_vertices
            projected_vertices = [(vertex[0], vertex[1], vertex[2] - self.z) for vertex in [adjusted_vertices[v] for v in face]]
    
            pygame.draw.polygon(up.st.winApp, face_color, [vertex[:2] for vertex in projected_vertices])
    
    def Update(self):
        self.draw()
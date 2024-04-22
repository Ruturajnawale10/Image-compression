from PIL import Image, ImageDraw
import random

def create_blank_image(resolution=(100000, 100000)):
    image = Image.new('1', resolution, color='white')
    return image
    
def create_irregular_blob(draw, x, y, radius, min_coverage=0.25):
    image_width, image_height = draw.im.size
    
    # Calculate the minimum area required for the blob
    min_blob_area = min_coverage * (image_width * image_height)
    
    # Define the minimum and maximum number of points to create the polygon
    min_points = 3
    max_points = 6
    
    # Calculate the maximum possible radius for the blob
    max_radius = min(image_width - x, x, image_height - y, y)
    
    # Randomly choose the number of points within the range [min_points, max_points]
    num_points = random.randint(min_points, max_points)
    
    # Generate random points within the radius
    points = [(random.randint(x - radius, x + radius), random.randint(y - radius, y + radius)) for _ in range(num_points)]
    
    # Calculate the area covered by the polygon
    blob_area = _calculate_polygon_area(points)
    
    # If the calculated area is less than the minimum required, adjust the radius
    randomized_blob_area = random.randint(min_blob_area, (image_width * image_height)* 0.8)
    while blob_area < randomized_blob_area:
        radius += 1
        points = [(random.randint(x - radius, x + radius), random.randint(y - radius, y + radius)) for _ in range(num_points)]
        blob_area = _calculate_polygon_area(points)
    
    # Draw the polygon with the adjusted points
    draw.polygon(points, fill='black')

def _calculate_polygon_area(points):
    # Calculate the area of a polygon using the shoelace formula
    n = len(points)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2


def create_microscope_image(image):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    
    # Calculate the minimum area required for the black region
    min_black_area = random.randint(0.25 * (image_width * image_height), 0.60 * (image_width * image_height))
    
    # Generate a bounding box for the irregular blob within the image
    min_x = image_width // 4
    max_x = image_width - min_x
    min_y = image_height // 4
    max_y = image_height - min_y
    
    # Randomly choose the position and size of the irregular blob
    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)
    
    # Calculate the maximum possible radius for the irregular blob
    max_radius = min(image_width - x, x, image_height - y, y)
    
    # Randomly choose a radius within the range [0, max_radius]
    radius = random.randint(0, max_radius)
    
    # Calculate the actual area covered by the irregular blob
    blob_area = 3.14 * (radius ** 2)
    
    # If the calculated area is less than the minimum required, adjust the radius
    while blob_area < min_black_area:
        radius += 1
        blob_area = 3.14 * (radius ** 2)
    
    # Create the irregular blob shape and fill with black color
    create_irregular_blob(draw, x, y, radius)
    
    return image, x, y, radius

def create_dye_image(image, x, y, radius):
    draw = ImageDraw.Draw(image)
    
    for _ in range(random.randint(10, 500)):  # Increase the number of veins
        # Generate random points within and around the blob
        x1_random = random.randint(x - radius, x + radius)
        y1_random = random.randint(y - radius, y + radius)
        x2_random = random.randint(x - radius, x + radius)
        y2_random = random.randint(y - radius, y + radius)
        
        # Conditionally draw horizontal lines 90% of the time representing veins
        if random.random() < 0.90:
            start_point = (x1_random, y1_random)
            end_point = (x2_random, y1_random)
            draw.line([start_point, end_point], fill='black', width=random.randint(1, 8))
        else:
            # Draw vertical or diagonal lines for the remaining 10% of the time
            start_point = (x1_random, y1_random)
            end_point = (x2_random, y2_random)
            draw.line([start_point, end_point], fill='black', width=random.randint(5, 8))
        
    for _ in range(random.randint(10, 100)):  # Increase the number of illuminated regions
        # Generate random points within and around the blob
        center = (random.randint(x - radius, x + radius), random.randint(y - radius, y + radius))
        # Randomly generate the size of the illuminated region
        size = random.randint(1, 5)
        # Draw filled circle or irregular polygon filled with black color
        draw.ellipse([center[0] - size, center[1] - size, center[0] + size, center[1] + size], fill='black')
        
    return image

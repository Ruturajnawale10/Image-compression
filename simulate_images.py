from PIL import Image, ImageDraw
import random

def create_simulated_images(resolution=(100000, 100000)):
    image = Image.new('RGB', resolution, 'white')
    return image

def save_image(image, filename):
    image.save(filename)
    
def create_microsope_image(image):
    draw = ImageDraw.Draw(image)
    image_area = image.size[0] * image.size[1]
    blob_area = random.randint(image_area * 0.25, image_area * 0.40)
    print("Parasite covers: ", str(
        (blob_area/image_area)*100)[:5], "%" + " of the image")
    radius = int((blob_area / 3.14) ** 0.5)
    x = random.randint(radius, image.size[0] - radius)
    y = random.randint(radius, image.size[1] - radius)
    draw.ellipse((x - radius, y - radius, x +
                 radius, y + radius), fill='black')
    return image, x, y, radius
    
def create_dye_image(image, x, y, radius):
    draw = ImageDraw.Draw(image)
    number_of_dots = random.randint(10000, 30000)
    
    # As per document 0.1% of blobs are cancerous so I will randomly select 1 blob to be cancerous and add more dots to it.
    is_blob_cancerous = random.randint(0, 1000)
    # is_blob_cancerous = 1
    if is_blob_cancerous == 1:
        number_of_dots = random.randint(50000, 100000)
    for i in range(number_of_dots):
        x_dot = random.randint(x - radius, x + radius)
        y_dot = random.randint(y - radius, y + radius)
        draw.point((x_dot, y_dot), fill='black')

    # Randomly drawing black dots outside of the blob
    number_of_dots = random.randint(1000, 2000)
    for i in range(number_of_dots):
        x_dot = random.randint(0, image.size[0])
        y_dot = random.randint(0, image.size[1])
        draw.point((x_dot, y_dot), fill='black')

    return image

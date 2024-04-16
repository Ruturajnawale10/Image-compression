from simulate_images import create_simulated_images, save_image, create_microsope_image, create_dye_image

from image_compression import convert_to_quad_tree, compress, save
from find_overlap import find_overlap_naive_approach, find_overlap_quad_tree_approach, get_quad_tree, return_global_black_pixels, reset_index
import time
from PIL import Image
import numpy as np

#create base image
size_of_image = 1000
base_image = create_simulated_images((size_of_image, size_of_image))

# Create microscope image
microscope_image, x, y, radius = create_microsope_image(base_image)

# Create dye image
base_image = create_simulated_images((size_of_image, size_of_image))
dye_image = create_dye_image(base_image, x, y, radius)

#save images
save_image(microscope_image, 'microscope_image.bmp')
save_image(dye_image, 'dye_image.bmp')

# Convert microscope image to quad tree for compression
microscope_image = np.array(microscope_image)
microscope_tree = convert_to_quad_tree(microscope_image, 0, 0, size_of_image-1, size_of_image-1)

# Convert dye image to quad tree
dye_image = np.array(dye_image)
dye_tree = convert_to_quad_tree(dye_image, 0, 0, size_of_image-1, size_of_image-1)

# Compress microscope image
microscope_compressed = compress(microscope_tree)

# Compress dye image
dye_compressed = compress(dye_tree)

# Save compressed images
save(microscope_compressed, 'microscope')
save(dye_compressed, 'dye')

# Naive Approach
# Calculate if parasite have cancer or not 

# Get start time
start_time = time.time()

# Open microscope image
microscope_image = Image.open('microscope_image.bmp')
microscope_image = np.array(microscope_image)
# Open dye image
dye_image = Image.open('dye_image.bmp')
dye_image = np.array(dye_image)
# Get overlap
microscope_black_pixels, overlaped_black_pixels = find_overlap_naive_approach(
    microscope_image, dye_image)

# Get end time
end_time = time.time()

# Print results
print('Naive approach')
print('Overlap: ' + str((overlaped_black_pixels /
      microscope_black_pixels)*100)[:5] + '%')
if (overlaped_black_pixels/microscope_black_pixels)*100 > 10:
    print('Parasite have cancer')
else:
    print('Parasite do not have cancer')

# Print time
print('Time: ' + str(end_time - start_time)[:5] + 's')

# Quad Tree Approach
# Calculate if parasite have cancer or not

# Get start time
start_time = time.time()

# Open compressed microscope image
with open('compressed_microscope.txt') as compressed_file:
    microscope_data = compressed_file.read()

# Open compressed dye image
with open('compressed_dye.txt') as compressed_file:
    dye_data = compressed_file.read()


# get_quad_tree microscope image
microscope_tree = get_quad_tree(microscope_data, 0, 0, size_of_image, size_of_image, True)
black_pixels = return_global_black_pixels()
# get_quad_tree dye image
reset_index()
dye_tree = get_quad_tree(dye_data, 0, 0, size_of_image, size_of_image)

# Get overlap
overlaped_black_pixels = find_overlap_quad_tree_approach(microscope_tree, dye_tree)
print(overlaped_black_pixels, black_pixels)

# Get end time
end_time = time.time()

# Print results
print('Quad Tree Approach')
print('Overlap: ' + str((overlaped_black_pixels/black_pixels)*100)[:5] + '%')
if (overlaped_black_pixels/black_pixels)*100 > 10:
    print('Parasite have cancer')
else:
    print('Parasite do not have cancer')

# Print time
print('Time: ' + str(end_time - start_time)[:5] + 's')
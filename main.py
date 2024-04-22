from reconstruct_images import create_image_from_quad_tree, create_image_from_rle
from simulate_images import create_blank_image, create_microscope_image, create_dye_image

from image_compression import convert_to_quad_tree, compress_quad_tree_str, save, compress_rle
from find_overlap import find_overlap_naive_approach, find_overlap_fast_approach, get_quad_tree, return_global_black_pixels
import time
from PIL import Image
import numpy as np
import pickle
from utils import print_results
import threading

# Function to convert microscope image to quad tree and compress it
def convert_and_compress_microscope(microscope_image, image_width, image_height):
    microscope_image = np.array(microscope_image)
    print("Converting microscope to quad tree...")
    microscope_tree = convert_to_quad_tree(microscope_image, 0, 0, image_width-1, image_height-1)
    print("Quad tree created successfully.")
    
    # Compress microscope image
    print("Compressing microscope image...")
    microscope_compressed = compress_quad_tree_str(microscope_tree)
    print("Compressed microscope image successfully")
    
    # Save compressed microscope images
    print("Saving compressed microscope quadtree data...")
    save(microscope_compressed, 'microscope')
    print("Saved compressed microscope quadtree data successfully.")
    
# Function to compress dye image using run length encoding
def compress_dye_image(dye_image):
    print("Compressing dye image...")
    dye_compressed_rle = compress_rle(dye_image)
    print("Dye image compressed successfully.")
    
    # Store the compressed rle data to a binary file
    print("Saving compressed dye rle data...")
    with open('compressed_data.pkl', 'wb') as f:
        pickle.dump(dye_compressed_rle, f)
    print("Saved compressed dye rle data successfully.")    

# Function to reconstruct microscope image from quad tree and save it
def reconstruct_and_save_microscope(microscope_tree, image_width, image_height):
    print("Reconstructing microscope image from quad tree and saving...")
    # microscope image reconstruction
    # Create a blank image
    simulated_image = np.ones((image_height, image_width), dtype=np.uint8) * 255  # Initialize with white pixels
    
    # Traverse the quad tree and create simulated image
    create_image_from_quad_tree(microscope_tree, simulated_image)
    
    # Save the simulated image
    # Open the simulated image
    simulated_image = Image.fromarray(simulated_image)
    
    # Save the image in BigTIFF format
    simulated_image.save('reconstructed_microscope_image_bigtiff.tif', compression='tiff_deflate')
    print("Reconstructed microscope image saved successfully")

# Function to reconstruct dye image from rle data and save it
def reconstruct_and_save_dye(dye_data, image_width, image_height):
    print("Reconstructing dye image from rle data and saving...")
    create_image_from_rle(dye_data, image_width, image_height).save('reconstructed_dye_image_rle_bigtiff.tif', compression='tiff_deflate')
    print("Reconstructed dye image saved successfully.")
    
code_start_time = time.time()

#create base image
image_width = 10000
image_height = 10000

print("Creating simulated images...")
# Create microscope image
blank_image = create_blank_image((image_width, image_height))
microscope_image, x, y, radius = create_microscope_image(blank_image)

# Create dye image
blank_image = create_blank_image((image_width, image_height))
dye_image = create_dye_image(blank_image, x, y, radius)
dye_image = np.array(dye_image)

print("Images simulation complete with dimensions: ", image_width, "x", image_height)

# Create threads for parallel execution of compression tasks
microscope_thread = threading.Thread(target=convert_and_compress_microscope, args=(microscope_image, image_width, image_height))
dye_thread = threading.Thread(target=compress_dye_image, args=(dye_image,))

# Start the threads
microscope_thread.start()
dye_thread.start()

# Wait for threads to complete
microscope_thread.join()
dye_thread.join()

# Open compressed microscope image
with open('compressed_microscope.txt') as compressed_file:
    microscope_data = compressed_file.read()

# Load the compressed dye data from the binary file
with open('compressed_data.pkl', 'rb') as f:
    dye_data = pickle.load(f)

print("All Compressions Done.")

# get_quad_tree microscope image
print("Extacting compressed microscope data to create quad tree")
microscope_tree = get_quad_tree(microscope_data, 0, 0, image_width, image_height, True)
black_pixels = return_global_black_pixels()

print("Quad tree reconstructed successfully.")

# Create threads for parallel execution of reconstruction tasks
microscope_reconstruction_thread = threading.Thread(target=reconstruct_and_save_microscope, args=(microscope_tree, image_width, image_height))
dye_reconstruction_thread = threading.Thread(target=reconstruct_and_save_dye, args=(dye_data, image_width, image_height))

# Start the threads
microscope_reconstruction_thread.start()
dye_reconstruction_thread.start()

# Wait for threads to complete
microscope_reconstruction_thread.join()
dye_reconstruction_thread.join()

print("-"*25)

# Calculate if parasite have cancer or not 
# Open microscope image
microscope_image = Image.open('reconstructed_microscope_image_bigtiff.tif')
microscope_image = np.array(microscope_image)

# Open dye image
dye_image = Image.open('reconstructed_dye_image_rle_bigtiff.tif')
dye_image = np.array(dye_image)

# Naive Approach using Nested Loops to find overlap
print("Finding if parasite has cancer with naive approach of using nested loops to find overlap...")
# Get start time
start_time = time.time()
# Get overlap between microscope and dye images
microscope_black_pixels, overlaped_black_pixels = find_overlap_naive_approach(
    microscope_image, dye_image)

# Get end time
end_time = time.time()

# Print results
print('Naive approach results')
print_results(overlaped_black_pixels, microscope_black_pixels, start_time, end_time)
print("-"*25)

# Faster Execution Approach using NumPy's vectorized operations to find overlap
# Get start time
print("Finding if parasite has cancer with fast approach of using NumPy's vectorized operations to find overlap...")
start_time = time.time()

# Get overlap between microscope and dye images
microscope_black_pixels, overlaped_black_pixels = find_overlap_fast_approach(
    microscope_image, dye_image)

# Get end time
end_time = time.time()

# Print results
print('Fast approach results')
print_results(overlaped_black_pixels, microscope_black_pixels, start_time, end_time)

code_end_time = time.time()

print("-"*50)
print("Total code Execution Time: ", str(code_end_time - code_start_time)[:5], "s")
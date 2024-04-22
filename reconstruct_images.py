from PIL import Image

# Function to create simulated image from quad tree
def create_image_from_quad_tree(tree, image):
    if tree is None:
        return

    # Base case: Leaf node
    if tree.val == 1:  # Black region
        # Set corresponding pixels in the image to black
        for i in range(tree.start_row, tree.end_row + 1):
            for j in range(tree.start_col, tree.end_col + 1):
                if i < len(image) and j < len(image[0]):
                    image[i][j] = 0  # Set pixel to black (0)

    elif tree.val == 0:  # White region
        # No action needed as white regions are already white in the image
        pass

    else:  # Mixed region
        # Recursively process child nodes
        create_image_from_quad_tree(tree.top_left, image)
        create_image_from_quad_tree(tree.top_right, image)
        create_image_from_quad_tree(tree.bottom_left, image)
        create_image_from_quad_tree(tree.bottom_right, image)
 
def decompress_row(row):
    decompressed_row = []
    for pixel_value, run_length in row:
        decompressed_row.extend([pixel_value] * run_length)
    return decompressed_row

def create_image_from_rle(compressed_data, width, height, chunk_size=1000):
    # Create an empty image
    image = Image.new('1', (width, height))
    image_data = image.load()

    # Process the image data in chunks
    for y in range(0, height, chunk_size):
        chunk_height = min(chunk_size, height - y)
        decompressed_data_chunk = [decompress_row(row) for row in compressed_data[y:y+chunk_height]]
        # Convert the chunk of decompressed data to a 1D list
        flat_data = [pixel for row in decompressed_data_chunk for pixel in row]
        # Write the chunk to the image
        for i, pixel in enumerate(flat_data):
            x = i % width
            image_data[x, y + i // width] = int(pixel)

    return image
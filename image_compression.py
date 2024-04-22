# Data Structure for Quad Tree Node

class QuadTree:
    def __init__(self, start_row, start_col, end_row, end_col, val, top_left=None, top_right=None, bottom_left=None, bottom_right=None):
        '''
        start_row: starting row of the image
        start_col: starting column of the image
        end_row: ending row of the image
        end_col: ending column of the image
        val: val of the node(1 for black, 0 for white, -1 for presence of both black and white)
        top_left: top left child of the node
        top_right: top right child of the node
        bottom_left: bottom left child of the node
        bottom_right: bottom right child of the node
        '''
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.val = val
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

# Converting image to Quad Tree


def convert_to_quad_tree(image, start_row, start_col, end_row, end_col):
    '''
    Input: image, start_row, start_col, end_row, end_col
    Output: Quad Tree
    '''
    if start_row > end_row or start_col > end_col:
        return None

    black_exists = False
    white_exists = False

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if black_exists and white_exists:
                break
            elif not black_exists and image[row][col] == False:
                black_exists = True
            elif not white_exists and image[row][col] == True:
                white_exists = True

    if black_exists and not white_exists:
        return QuadTree(start_row, start_col, end_row, end_col, 1)
    elif white_exists and not black_exists:
        return QuadTree(start_row, start_col, end_row, end_col, 0)
    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2
    return QuadTree(start_row, start_col, end_row, end_col, -1,
                    convert_to_quad_tree(
                        image, start_row, start_col, mid_row, mid_col),
                    convert_to_quad_tree(
                        image, start_row, mid_col + 1, mid_row, end_col),
                    convert_to_quad_tree(
                        image, mid_row + 1, start_col, end_row, mid_col),
                    convert_to_quad_tree(image, mid_row + 1, mid_col + 1, end_row, end_col))

# Algorithm to compress the tree into a string


def compress_quad_tree_str(tree):
    '''
    Input: Quad Tree
    Output: Compressed string
    '''
    if tree == None:
        return '3'
    if tree.val == -1:
        compressed_data = '2'
        compressed_data += compress_quad_tree_str(tree.top_left)
        compressed_data += compress_quad_tree_str(tree.top_right)
        compressed_data += compress_quad_tree_str(tree.bottom_left)
        compressed_data += compress_quad_tree_str(tree.bottom_right)
        return compressed_data
    if tree.val == 1:
        return '1'
    if tree.val == 0:
        return '0'
    
def rle_compress(image):
    compressed_data = []
    current_pixel = None
    count = 0

    for row in image:
        for pixel in row:
            pixel_value = 1 if pixel else 0
            if pixel_value == current_pixel:
                count += 1
            else:
                if current_pixel is not None:
                    compressed_data.append((current_pixel, count))
                current_pixel = pixel_value
                count = 1

    compressed_data.append((current_pixel, count))

    return str(compressed_data)

def compress_rle(image):
    compressed_data = []
    for row in image:
        compressed_row = []
        current_pixel = row[0]
        run_length = 1
        for pixel in row[1:]:
            if pixel == current_pixel:
                run_length += 1
            else:
                compressed_row.append((current_pixel, run_length))
                current_pixel = pixel
                run_length = 1
        # Append the last run in the row
        compressed_row.append((current_pixel, run_length))
        compressed_data.append(compressed_row)
    return compressed_data

# Function to save the compressed data into a file

def save(compressed_data, file_type):
    '''
    Input: Compressed string, file_type
    Output: File name'''
    file_name = 'compressed_'+file_type + '.txt'

    compressed_file = open(file_name, 'w')
    compressed_file.write(compressed_data)
    compressed_file.close()
    return file_name

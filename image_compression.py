# Data Structure for Quad Tree Node

class QuadTree:
    def __init__(self, start_row, start_col, end_row, end_col, color, top_left=None, top_right=None, bottom_left=None, bottom_right=None):
        '''
        start_row: starting row of the image
        start_col: starting column of the image
        end_row: ending row of the image
        end_col: ending column of the image
        color: color of the node
        top_left: top left child of the node
        top_right: top right child of the node
        bottom_left: bottom left child of the node
        bottom_right: bottom right child of the node
        '''
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.color = color
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
            elif not black_exists and image[row][col][0] == 0:
                black_exists = True
            elif not white_exists and image[row][col][0] == 255:
                white_exists = True

    if black_exists and not white_exists:
        return QuadTree(start_row, start_col, end_row, end_col, 'black')
    elif white_exists and not black_exists:
        return QuadTree(start_row, start_col, end_row, end_col, 'white')
    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2
    return QuadTree(start_row, start_col, end_row, end_col, 'mixed',
                    convert_to_quad_tree(
                        image, start_row, start_col, mid_row, mid_col),
                    convert_to_quad_tree(
                        image, start_row, mid_col + 1, mid_row, end_col),
                    convert_to_quad_tree(
                        image, mid_row + 1, start_col, end_row, mid_col),
                    convert_to_quad_tree(image, mid_row + 1, mid_col + 1, end_row, end_col))

# Algorithm to compress the tree into a string


def compress(tree):
    '''
    Input: Quad Tree
    Output: Compressed string
    '''
    if tree == None:
        return '3'
    if tree.color == "black":
        return '0'
    if tree.color == 'white':
        return '1'
    else:
        compressed_data = '2'
        compressed_data += compress(tree.top_left)
        compressed_data += compress(tree.top_right)
        compressed_data += compress(tree.bottom_left)
        compressed_data += compress(tree.bottom_right)
        return compressed_data

# Functo save the compressed data into a file


def save(compressed_data, file_type):
    '''
    Input: Compressed string, file_type
    Output: File name'''
    file_name = 'compressed_'+file_type + '.txt'

    compressed_file = open(file_name, 'w')
    compressed_file.write(compressed_data)
    compressed_file.close()
    return file_name

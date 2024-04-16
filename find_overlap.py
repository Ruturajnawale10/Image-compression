from image_compression import QuadTree

def find_overlap_naive_approach(microscope_image, dye_image):
    # Get black pixels in microscope image
    microscope_black_pixels = 0
    for i in range(len(microscope_image)):
        for j in range(len(microscope_image[0])):
            if microscope_image[i][j][0] == 0:
                microscope_black_pixels += 1

    # Get overlaped black pixels
    overlaped_black_pixels = 0
    for i in range(len(microscope_image)):
        for j in range(len(microscope_image[0])):
            if microscope_image[i][j][0] == 0 and dye_image[i][j][0] == 0:
                overlaped_black_pixels += 1

    return microscope_black_pixels, overlaped_black_pixels

index = 0
black_pixels = 0

def get_quad_tree(compressed_data, start_row, start_col, end_row, end_col, is_microscope=False):
    '''
    Input: Compressed string, start_row, start_col, end_row, end_col, is_microscope
    Output: Quad Tree
    '''
    global index
    if is_microscope:
        # To optimize the algorithm, we will count the black pixels in the microscope image when we are get_quad_treeing the tree
        global black_pixels
    if index >= len(compressed_data):
        return None
    color = compressed_data[index]
    if color == '0':
        if is_microscope:
            black_pixels += (end_row - start_row + 1) * \
                (end_col - start_col + 1)
        return QuadTree(start_row, start_col, end_row, end_col, 'black')
    if color == '1':
        return QuadTree(start_row, start_col, end_row, end_col, 'white')
    if color == '2':
        new_node = QuadTree(start_row, start_col, end_row, end_col, 'mixed')
        index += 1
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        new_node.top_left = get_quad_tree(
            compressed_data, start_row, start_col, mid_row, mid_col, is_microscope)
        index += 1
        new_node.top_right = get_quad_tree(
            compressed_data, start_row, mid_col + 1, mid_row, end_col, is_microscope)
        index += 1
        new_node.bottom_left = get_quad_tree(
            compressed_data, mid_row + 1, start_col, end_row, mid_col, is_microscope)
        index += 1
        new_node.bottom_right = get_quad_tree(
            compressed_data, mid_row + 1, mid_col + 1, end_row, end_col, is_microscope)
        return new_node

    if color == '3':
        return None

# Algoritm to find black pixels in a Quad Tree


def find_black_pixels(tree):
    '''
    Input: Quad Tree
    Output: Number of black pixels in the Quad Tree
    '''
    if tree == None:
        return 0
    if tree.color == 'white':
        return 0
    if tree.color == 'black':
        return (tree.end_row - tree.start_row + 1) * (tree.end_col - tree.start_col + 1)
    return find_black_pixels(tree.top_left) + find_black_pixels(tree.top_right) + find_black_pixels(tree.bottom_left) + find_black_pixels(tree.bottom_right)

# Faster algorithm to find overlap between microscope image and dye image


def find_overlap_quad_tree_approach(microscope_tree, dye_tree):
    '''
    Input: Quad Tree of microscope image, Quad Tree of dye image
    Output: Number of black pixels in the overlap region
    '''
    overlap_black_count = 0
    if microscope_tree == None or dye_tree == None:
        return 0
    if microscope_tree.color == 'white':
        return 0
    if microscope_tree.color == 'black':
        if dye_tree.color == 'black' or dye_tree.color == 'mixed':
            overlap_black_count += find_black_pixels(dye_tree)
    else:
        overlap_black_count += find_overlap_quad_tree_approach(
            microscope_tree.top_left, dye_tree.top_left)
        overlap_black_count += find_overlap_quad_tree_approach(
            microscope_tree.top_right, dye_tree.top_right)
        overlap_black_count += find_overlap_quad_tree_approach(
            microscope_tree.bottom_left, dye_tree.bottom_left)
        overlap_black_count += find_overlap_quad_tree_approach(
            microscope_tree.bottom_right, dye_tree.bottom_right)

    return overlap_black_count

# Helper function to return the number of black pixels in the microscope image


def return_global_black_pixels():
    return black_pixels

# Helper function to reset the global index variable


def reset_index():
    global index
    index = 0

#  Helper function to traverse the Quad Tree (Not needed for the coding challege but useful for debugging)


def traverse(tree):
    '''
    Input: Quad Tree
    Output: None
    '''
    if tree == None:
        return
    print(tree.color, tree.start_row, tree.start_col, tree.end_row, tree.end_col)
    traverse(tree.top_left)
    traverse(tree.top_right)
    traverse(tree.bottom_left)
    traverse(tree.bottom_right)

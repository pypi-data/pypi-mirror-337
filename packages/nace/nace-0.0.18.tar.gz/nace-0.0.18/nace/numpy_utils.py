
"""
Handy routines to manipulate a ndarray.

"""
import os
import numpy as np
import tempfile
import matplotlib.pyplot as plt

try:
    import cv2 # pip install opencv-python
    is_cv2_installed = True
except ImportError as e:
    is_cv2_installed = False

def convert_chr_to_rgb(ch:str, rgb_shape:tuple):
    decimal_ascii = ord(ch)
    fig, ax = plt.subplots()
    fig2 = plt.figure(figsize=(.6, .15), dpi=300)
    plt.text(0.05, 0.05, ch)
    filename = str(decimal_ascii).rjust(3,"0")+".png"
    full_filename = os.path.join(tempfile.gettempdir(), filename)
    plt.savefig(full_filename)
    plt.close(fig2)
    plt.close()


    if is_cv2_installed:
        images_cv = cv2.imread(full_filename)
        rgb = np.array(images_cv, dtype=np.int64)
        assert rgb.shape == rgb_shape

    return rgb


def convert_string_list_to_cells(string_list:list[str], cell_shape_rc=(45, 180, 3), numpy_seed=None):
    char_to_rgb_mapping = {}
    rgb_to_char_mapping = {}
    rgb_shape = cell_shape_rc
    height=len(string_list)
    width=len(string_list[0])
    for i in range(height):
        assert width==len(string_list[i]) # all lines should be the same length
    raw_rgb_array = np.zeros((height * cell_shape_rc[0], width * cell_shape_rc[1], cell_shape_rc[2]), dtype=np.int64)
    if numpy_seed is not None:
        np.random.seed(numpy_seed)

    for r,line in enumerate(string_list):
        for c, ch in enumerate(line):

            if ch not in char_to_rgb_mapping:
                rgb_cell = convert_chr_to_rgb(ch,rgb_shape)
                # rgb_cell = np.random.randint(255, size=rgb_shape)
                char_to_rgb_mapping[ch] = rgb_cell
                rgb_to_char_mapping[rgb_cell.data.tobytes()] = ch

            patch = char_to_rgb_mapping[ch]
            # overwite patch
            raw_rgb_array[r * cell_shape_rc[0]:(r + 1) * cell_shape_rc[0], c * cell_shape_rc[1]:(c + 1) * cell_shape_rc[1], 0:cell_shape_rc[2]] = patch

    return char_to_rgb_mapping, rgb_to_char_mapping, raw_rgb_array


def convert_char_list_of_lists_to_cells(char_list_of_lists:list, cell_shape_rc=(60, 60, 3), numpy_seed=None ):
    # [['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    #  ['o', ' ', ' ', ' ', 'o', ' ', ' ', ' ', 'f', ' ', ' ', 'o'],
    #  ['o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o'],
    #  ['o', ' ', ' ', ' ', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    #  ['o', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o'],
    #  ['o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'u', ' ', ' ', 'o'],
    #  ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']]
    char_to_rgb_mapping = {}
    rgb_to_char_mapping = {}
    rgb_shape = cell_shape_rc
    height=len(char_list_of_lists)
    width=len(char_list_of_lists[0])
    raw_rgb_array = np.zeros((height * cell_shape_rc[0], width * cell_shape_rc[1], cell_shape_rc[2]), dtype=np.int64)
    if numpy_seed is not None:
        np.random.seed(numpy_seed)

    for r,line_list in enumerate(char_list_of_lists):
        for c, ch in enumerate(line_list):
            if ch not in char_to_rgb_mapping:
                rgb_cell = np.random.randint(255, size=rgb_shape)
                char_to_rgb_mapping[ch] = rgb_cell
                rgb_to_char_mapping[rgb_cell.data.tobytes()] = ch

            patch = char_to_rgb_mapping[ch]
            # overwite patch
            raw_rgb_array[r * cell_shape_rc[0]:(r + 1) * cell_shape_rc[0], c * cell_shape_rc[1]:(c + 1) * cell_shape_rc[1], 0:cell_shape_rc[2]] = patch

    return char_to_rgb_mapping, rgb_to_char_mapping, raw_rgb_array
import numpy as np

def chunk_txt(file_path, chunk_size=50):
    """
    Simple function to read a text file and split it into chunks of a given size.
    """
    with open(file_path, 'r') as file:
        data = file.read().split()


    chunks = np.array_split(data, chunk_size)

    return chunks
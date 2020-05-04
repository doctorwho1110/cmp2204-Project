import os
import math

def divide_into_chunks(file, fileName, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    c = os.path.getsize(file)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    cnt = 1
    with open(file, 'rb') as infile:
        divided_file = infile.read(int(CHUNK_SIZE))
        while divided_file:
            name = directory + "/" + fileName.split('.')[0] + "" + str(cnt)
            with open(name, 'wb+') as div:
                div.write(divided_file)
            cnt += 1
            divided_file = infile.read(int(CHUNK_SIZE))
import os

# Deletes all files in the images directory
def delete():
    for root, _, files in os.walk("./static/images"):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
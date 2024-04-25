import os

def delete():
    for root, _, files in os.walk("./static/images"):
        for file in files:
            #Construct the full filepath
            file_path = os.path.join(root, file)
            #Delete the file
            os.remove(file_path)
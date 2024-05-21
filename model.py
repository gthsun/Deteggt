#Import statements
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import json
import supervision as sv
import cv2
import os
from clear import delete

#Returns a list containing all the files stored in the inputted directory
def list_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

directory_path = "./static/images"
file_list = list_files(directory_path) #Creates a list of every image in the images folder (should only be 1)
#print(file_list)

if file_list:
    custom_configuration = InferenceConfiguration(confidence_threshold=0.5)
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="YOUR-API-KEY"
    )

    with CLIENT.use_configuration(custom_configuration):
        result = CLIENT.infer(file_list[0], model_id="ovos-de-parasitas-azoug/6") #The model is run from Roboflow
    #result = CLIENT.infer(file_list[0], model_id="roundworm-egg-detection-project/1")

    count = len(result['predictions']) #Obtain the model's count of the number of eggs detected
    if count > 1:
        final_string = str(count) + " eggs identified"
    elif count == 1:
        final_string = "1 egg identified"
    else:
        final_string = "It appears that no eggs were detected"

    labels = [item['class'] for item in result['predictions']] #Labels for the bounding boxes
    
    detections = sv.Detections.from_inference(result) #Convert the model results into a unified format
    label_annotator = sv.LabelAnnotator() #Label annotations
    bounding_box_annotator = sv.BoundingBoxAnnotator() #Bounding boxes
    image = cv2.imread(file_list[0]) #Takes in the image
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections) #Puts bounding boxes
    #annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels) #Puts labels

    delete() #Delete image(s) in image directory

    #Save annotated image in image directory
    annotated_image_path = os.path.join(directory_path, 'annotated_image.jpg') 
    cv2.imwrite(annotated_image_path, annotated_image)

else:
    final_string = "No files found for processing."
print(final_string)





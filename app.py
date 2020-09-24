import time
import edgeiq
from helpers import *
import json
import os
from interest_item import InterestItem
"""
This application measures the distance between two or more 
objects of interest, as specified in the config.json file.
"""

def load_json(filepath):
    # this function was borrowed from: 
    # https://alwaysai.co/blog/speed-up-development-with-a-json-configuration-file
    # check that the file exists and return the loaded json data
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))

    with open(filepath) as data:
        return json.load(data)

def main():
    # load the config file
    config = load_json("config.json")

    # The main items to detect
    KEY_ITEMS = []

    # if you would like to test an additional model, add one to the list below:
    MODELS = config.get("models")

    # include any labels that you wish to detect from any models (listed above in 'models') here in this list
    INTEREST_LABELS = []

    # load all the models (creates a new object detector for each model)
    detectors = []
    for model in MODELS:

        # start up a first object detection model
        obj_detect = edgeiq.ObjectDetection(model)
        obj_detect.load(engine=edgeiq.Engine.DNN)

        # track the generated object detection items by storing them in detectors
        detectors.append(obj_detect)

        # print the details of each model to the console
        print("Model:\n{}\n".format(obj_detect.model_id))
        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Labels:\n{}\n".format(obj_detect.labels))

    for item in config.get("interest_items"):
        KEY_ITEMS.append(InterestItem(item.get("width"), 
            item.get("height"), item.get("name"), 
            item.get("interest_labels")))
        
        for label in item.get("interest_labels"):
            INTEREST_LABELS.append(label)

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                predictions_to_markup = []
                text = [""]
                KEY_PRED = []

                # gather data from the all the detectors 
                for i in range(0, len(detectors)):
                    results = detectors[i].detect_objects(
                        frame, confidence_level=.2)

                    # append each prediction
                    predictions = results.predictions
                    if len(predictions) > 1:
                        for prediction in predictions:
                            if (prediction.label.strip() in INTEREST_LABELS):
                                KEY_PRED.append(prediction)
                           
                            predictions_to_markup.append(prediction)       

                # mark up the frame with the predictions for the contraband objects
                frame = edgeiq.markup_image(
                        frame, predictions_to_markup, show_labels=True,
                        show_confidences=False, colors=obj_detect.colors)
                
                # mark up the frame and get the text of the distance calculations
                (frame, text) = draw_distances(frame, KEY_ITEMS, KEY_PRED)
                
                # send the frame and text to the streamer
                streamer.send_data(frame, text)
                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        print("Program Ending")


if __name__ == "__main__":
    main()

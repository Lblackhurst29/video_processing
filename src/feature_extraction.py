import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications import ResNet50

def extract_features(frame, model):
    # Preprocess the frame and extract features using the ResNet50 model
    frame = cv2.resize(frame, (224, 224))
    frame = preprocess_input(frame)
    features = model.predict(np.array([frame]))
    return features.flatten()
    
def create_resnet50_model():
    # Load the ResNet50 model without the top layer and freeze the weights
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    model.trainable = False
    return model

import cv2

# Open the video file
cap = cv2.VideoCapture('video.mp4')

# Define the threshold value
threshold_value = 100

# Loop through the frames of the video
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to the grayscale image
    ret, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop through the contours and find the largest one
    max_contour = None
    max_contour_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_contour_area:
            max_contour = contour
            max_contour_area = area
    
    # Draw the largest contour on the original frame
    if max_contour is not None:
        cv2.drawContours(frame, [max_contour], 0, (0, 255, 0), 3)
    
    # Display the original frame with the largest contour
    cv2.imshow('frame', frame)
    
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

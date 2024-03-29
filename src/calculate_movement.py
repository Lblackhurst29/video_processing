import cv2
import os
import numpy as np

# contour_list = []
# frame_count_list = []

# Function to detect motion in a frame
def is_motion(frames, threshold):

    motion = []
    contours_med = []

    for frame in frames:
        # converts the current frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # applies a Gaussian blur to the grayscale frame, helps reduce noise and minor variations in pixel values 
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # when first iteration return false
        if is_motion.previous_frame is None:
            is_motion.previous_frame = gray
            continue
        
        # difference betweeen the two frames
        frame_delta = cv2.absdiff(is_motion.previous_frame, gray)
        # turns those parts about the theshold (30) t0 255 (white)
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        # morphological operation to dilate, this enhances the motion regions
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_EXTERNAL

        for contour in contours:
            # print([cv2.contourArea(contour)])
            contours_med.append(cv2.contourArea(contour))
            if cv2.contourArea(contour) > threshold:
                # draws a rectangle around the area of movement
                # (x, y, w, h) = cv2.boundingRect(contour)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion.append(True)

    is_motion.previous_frame = gray

    if len(contours_med) == 0:
        return False
    else:
        # print(np.median(contours_med))
        # print(contours_med)
        if np.median(contours_med) > threshold:
            return True
        else:
            return False

is_motion.previous_frame = None

# Function to segment the video into mobile and immobile parts
def segment_video(input_file, threshold, output, typ):
    video_capture = cv2.VideoCapture(input_file)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Desired interval in seconds for absdiff
    interval_seconds = 15

    # Convert interval to frames based on average FPS
    interval_frames = int(interval_seconds * fps)

    video_writer = None
    
    frames = []
    frame_count = 0
    count = 1

    type_frames = [True]

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        frames.append(frame)
        frame_count += 1

        if frame_count == interval_frames:
            motion_detected = is_motion(frames, threshold)
            if motion_detected == True:
                clss = 'mobile'
                type_frames.append(True)
            else:
                clss = 'immobile'
                type_frames.append(False)
            
            if  len(type_frames) == 2 or type_frames[-1] != type_frames[-2]:
                if video_writer is not None:
                    video_writer.release()    
                print(f"{output}/{typ}_{count}_{clss}_{os.path.basename(input_file)}")
                video_writer = cv2.VideoWriter(f"{output}/{typ}_{count}_{clss}_{os.path.basename(input_file)}", 
                                                        cv2.VideoWriter_fourcc(*'mp4v'), 
                                                        fps, (frame_width, frame_height))
                count += 1
            
            for frame in frames:
                video_writer.write(frame)
            frame_count = 0
            frames = []
    
    # Release video capture and writers
    video_capture.release()
    if video_writer is not None:
        video_writer.release()

def get_vid_length(input):
    video = cv2.VideoCapture(input)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    vid_len = (frame_count / fps) / 60
    if vid_len < 4.5:
        os.remove(input)

thresh = 1550

# folder = '/home/lab/Documents/all_vids/HD_vids'

# file_list = []
# for filename in os.listdir(folder):
#     f = os.path.join(folder, filename)
#     if '_WT' in f or '_CS' in f:
#         file_list.append(f)

# output_folder = '/home/lab/Desktop/video_processing/data/processed_video/mobile'
# # haven't done /home/lab/Documents/all_vids/HD_vids/04_05_2023_CS2
# for file in file_list:
#     if '_WT' in file:
#         typ = 'WC4'
#     else:
#         typ = 'CS'
#     print(f'Starting {file}')
#     file_count = 1

file = '/home/lab/Documents/test_vids'
file_count = 1
for vid in os.listdir(file):
    v = os.path.join(file, vid)
    print(f'Segmenting {file_count} of {len(os.listdir(file))}')
    file_count +=1
    try:
        segment_video(v, threshold = thresh, output = '/home/lab/Documents/output', typ = 'clss')
    except:
        print(f'Error: {v}')
        continue
# for vid in os.listdir(output_folder):
#     v = os.path.join(output_folder, vid)
#     get_vid_length(v)

# The specific methods we'll be using from the OpenCV package are:

# cv2.VideoCapture(): This function creates a VideoCapture object that can be used to read frames from a video file.

# cv2.absdiff(): This function calculates the absolute difference between two frames.

# cv2.cvtColor(): This function converts a color image from one color space to another. We'll use it to convert the difference image to grayscale.

# cv2.GaussianBlur(): This function applies a Gaussian filter to an image to reduce noise.

# cv2.threshold(): This function applies a threshold to an image to convert it to a binary image.

# cv2.countNonZero(): This function counts the number of non-zero pixels in a binary image.
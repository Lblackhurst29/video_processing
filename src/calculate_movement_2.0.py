import cv2
import os
import numpy as np

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

        if len(contours) == 0:
            contours_med.append(0)
        else:
            tmp_contours = []
            for contour in contours:
                tmp_contours.append(cv2.contourArea(contour))
            contours_med.append(np.mean(tmp_contours))
                # print([cv2.contourArea(contour)])
                # contours_med.append(cv2.contourArea(contour))
                # if cv2.contourArea(contour) > threshold:
                    # draws a rectangle around the area of movement
                    # (x, y, w, h) = cv2.boundingRect(contour)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # motion.append(True)

    is_motion.previous_frame = gray

    if len(contours_med) == 0:
        return False, contours_med
    else:
        # print(np.median(contours_med))
        # print(contours_med)
        if np.median(contours_med) > threshold:
            return True, contours_med
        else:
            return False, contours_med

is_motion.previous_frame = None

# Function to segment the video into mobile and immobile parts

def segment_video(input_file, threshold, output, typ):

    file_list = []
    for filename in os.listdir(input_file):
        f = os.path.join(input_file, filename)
        if f.endswith('.mkv'):
            file_list.append(f)
    file_list.sort()

    video_capture = cv2.VideoCapture(file_list[0])
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Desired interval in seconds for absdiff
    interval_seconds = 15

    # Convert interval to frames based on average FPS
    interval_frames = int(interval_seconds * fps)

    video_writer = None
    file_index = 0
    frames = []
    frame_count = 0
    count = 1

    type_frames = [True]
    contours_all = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            try:
                file_index += 1
                video_capture.release()
                video_capture = cv2.VideoCapture(file_list[file_index])
                continue
            except IndexError:
                break
        frames.append(frame)
        frame_count += 1
        if frame_count == interval_frames:
            motion_detected, contours_lst = is_motion(frames, threshold)
            contours_all.append(contours_lst)
            if motion_detected == True:
                clss = 'mobile'
                type_frames.append(True)
            else:
                clss = 'immobile'
                type_frames.append(False)
            
            if  len(type_frames) == 2 or type_frames[-1] != type_frames[-2]:
                if video_writer is not None:
                    video_writer.release()
                # print('video creaed')
                # print(f"{output}/{typ}_{count}_{clss}_{os.path.basename(input_file)}")
                video_writer = cv2.VideoWriter(f"{output}/{count}_{clss}_{typ}.mkv", 
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
    contours_all = [item for sublist in contours_all for item in sublist]
    np.savetxt(f'{output}/contours_{typ}.txt', np.array(contours_all))

VID_LEN = 4.8

def get_vid_length(folder):
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if f.endswith('.mkv'):
            video = cv2.VideoCapture(f)
            fps = video.get(cv2.CAP_PROP_FPS)
            frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
            
            vid_len = (frame_count / int(fps)) / 60
            if vid_len < VID_LEN:
                os.remove(f)

thresh = 1550
folder = os.getcwd()
output_folder = f'{folder}/output'
os.mkdir(output_folder)
name = 'xxFLYxx'

segment_video(folder, threshold = thresh, output = output_folder, typ = name)

get_vid_length(output_folder)

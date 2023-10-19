import cv2
import os
def extract_frames(video_path, output_folder):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    # fps = video.get(cv2.CAP_PROP_FPS)
    # print(fps)
    # Create a counter to keep track of frame numbers
    frame_counter = 0
    wait_speed = 1

    while True:
        # Read the next frame from the video
        ret, frame = video.read()
        
        # Break the loop if no frame is retrieved
        if not ret:
            break
        
        # Display the frame
        cv2.imshow('Frame', frame)
        
        # Check for key press
        key = cv2.waitKey(wait_speed) & 0xFF
        
        # Save the frame if the 's' key is pressed
        if key == ord('s'):
            # Generate the output file path
            output_path = f"{output_folder}/img{frame_counter}.png"
            
            # Save the frame as a PNG image
            cv2.imwrite(output_path, frame)
            print(f"Saved frame {frame_counter} as {output_path}")
            frame_counter += 1
            continue
        
        # Slow down the wait time a lot 
        elif key == ord('g'):
            wait_speed = 1200
            frame_counter += 1
            continue

        # Slow down the wait time a little bit
        elif key == ord('h'):
            wait_speed = 200
            frame_counter += 1
            continue

        # Speed it back up
        elif key == ord('f'):
            wait_speed = 1
            frame_counter += 1
            continue

        # Break the loop if the 'q' key is pressed
        elif key == ord('q'):
            break

        frame_counter += 1
    
    # Release the video object and close all windows
    video.release()
    cv2.destroyAllWindows()

# Provide the path to the video file and output folder
video_path = '/home/lab/Documents/all_vids/HD_vids/22_04_2023_CS/22_04_23_16-11-50.mkv'
# The output folder should be in the created DLC folder called labeled-date
output_folder = f"/home/lab/Desktop/DLC/sleeping_flies-LB-2023-07-13/labeled-data/{os.path.basename(video_path)[:-4]}"
# Call the function to extract frames
extract_frames(video_path, output_folder)

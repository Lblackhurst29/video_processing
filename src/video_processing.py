import cv2

def remove_background(video_path):
    cap = cv2.VideoCapture(video_path)

    # Create background subtraction object
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Define codec for output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #(*'DIVX')

    # Set up output video file
    out_path = '/home/lab/Desktop/video_processing/data/processed_video/output.mp4'
    # print(cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(out_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Apply background subtraction
        fgmask = fgbg.apply(frame)
        cv2.imshow('fgmask', fgmask)
        cv2.imshow('frame',frame )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Write frame to output video
        out.write(fgmask)
        # out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return out_path


video_path = '/home/lab/Documents/all_vids/HD_vids/11_05_23_21-28-15.mkv'
new_vid = remove_background(video_path)
print(new_vid)
def calculate_movement(video_path):
    cap = cv2.VideoCapture(video_path)
    success, prev_frame = cap.read()
    movement = 0
    
    while success:
        success, curr_frame = cap.read()
        if success:
            diff = cv2.absdiff(prev_frame, curr_frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            movement += cv2.countNonZero(thresh)
            prev_frame = curr_frame
    
    return movement

input_folder = "/path/to/input/folder"
output_folder_low = "/path/to/output/low/activity"
output_folder_medium = "/path/to/output/medium/activity"
output_folder_high = "/path/to/output/high/activity"


for filename in os.listdir(input_folder):
    if filename.endswith(".mkv"):
        video_path = os.path.join(input_folder, filename)
        movement = calculate_movement(video_path)
        if movement < 10000:
            output_folder = output_folder_low
        elif movement < 50000:
            output_folder = output_folder_medium
        else:
            output_folder = output_folder_high
        shutil.move(video_path, output_folder)

# The specific methods we'll be using from the OpenCV package are:

# cv2.VideoCapture(): This function creates a VideoCapture object that can be used to read frames from a video file.

# cv2.absdiff(): This function calculates the absolute difference between two frames.

# cv2.cvtColor(): This function converts a color image from one color space to another. We'll use it to convert the difference image to grayscale.

# cv2.GaussianBlur(): This function applies a Gaussian filter to an image to reduce noise.

# cv2.threshold(): This function applies a threshold to an image to convert it to a binary image.

# cv2.countNonZero(): This function counts the number of non-zero pixels in a binary image.
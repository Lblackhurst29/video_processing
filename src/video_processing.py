import cv2

def remove_background(frame):
    # Apply background subtraction to extract the foreground mask
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fgmask = fgbg.apply(frame)
    
    # Apply morphological opening to remove noise and smooth the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    # Invert the mask and apply it to the original frame to extract the foreground object
    fg = cv2.bitwise_and(frame, frame, mask=fgmask)
    bg = cv2.cvtColor(cv2.bitwise_not(fgmask), cv2.COLOR_GRAY2BGR)
    return cv2.add(fg, bg)

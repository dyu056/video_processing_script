import cv2
import os

# Input folder with video files
current_directory = os.getcwd()
video_folder = os.path.join(current_directory, 'videos')  # Ensure the correct path format
print(video_folder)

# Base folder for images (individual folders will be created for each video)
base_image_folder = 'processed_videos_blurred'

# Option to switch blurring on or off
apply_blur = True  # Set to False if you don't want to apply the blur

# Iterate over all video files in the folder
for index, video_filename in enumerate(os.listdir(video_folder), start=1):  # Start numbering from 1
    video_path = os.path.join(video_folder, video_filename)
    
    if video_filename.endswith(('.mp4', '.avi', '.mov')):  # Add more formats as needed
        # Create a new folder for the current video file (sequentially named 1, 2, 3, etc.)
        video_image_folder = os.path.join(base_image_folder, str(index))
        
        if not os.path.exists(video_image_folder):
            os.makedirs(video_image_folder)
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # No more frames
            
            # Get the height and width of the frame
            height, width = frame.shape[:2]
            
            # Calculate the cropping area to keep the center of the image
            crop_width = height  # The width of the crop will be equal to the height (square)
            crop_x = (width - crop_width) // 2  # Calculate the starting x coordinate (center)
            
            # Crop the image to make it square
            cropped_frame = frame[:, crop_x:crop_x + crop_width]
            
            # Rotate the image 90 degrees clockwise
            rotated_frame = cv2.rotate(cropped_frame, cv2.ROTATE_90_CLOCKWISE)
            
            # Apply blur if the switch is enabled
            if apply_blur:
                blurred_frame = cv2.GaussianBlur(rotated_frame, (5, 5), 0)
                resized_frame = cv2.resize(blurred_frame, (64, 64), interpolation=cv2.INTER_LINEAR)
            else:
                resized_frame = cv2.resize(rotated_frame, (64, 64), interpolation=cv2.INTER_LINEAR)
            
            # Save the frame as a PNG image in the newly created folder
            image_filename = f"{frame_count}.png"
            image_path = os.path.join(video_image_folder, image_filename)
            cv2.imwrite(image_path, resized_frame)
            
            frame_count += 1
        
        # Release the video capture object
        cap.release()

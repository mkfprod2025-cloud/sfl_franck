import cv2
import os
import numpy as np
from PIL import Image

def extract_frames(video_path, output_folder, prefix):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR (OpenCV) to RGBA (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb).convert("RGBA")
        
        # Remove background (assuming top-left pixel is background)
        data = np.array(pil_img)
        bg_color = data[0, 0, :3]
        
        # Simple color keying
        mask = np.all(data[:, :, :3] == bg_color, axis=-1)
        data[mask, 3] = 0 # Set alpha to 0 for background pixels
        
        # Save frame
        final_img = Image.fromarray(data)
        final_img.save(os.path.join(output_folder, f"{prefix}_{count:03d}.png"))
        count += 1
        
    cap.release()
    print(f"Extracted {count} frames from {video_path} to {output_folder}")

if __name__ == "__main__":
    assets_dir = r"C:\Users\amber\OneDrive\Bureau\SFL_franck\assets"
    videos = [
        ("Enregistrement 2026-05-23 143239.mp4", "anim1"),
        ("Enregistrement 2026-05-23 143350.mp4", "anim2"),
        ("Enregistrement 2026-05-23 143445.mp4", "anim3")
    ]
    
    for video_file, prefix in videos:
        v_path = os.path.join(assets_dir, video_file)
        o_path = os.path.join(assets_dir, "extracted", prefix)
        extract_frames(v_path, o_path, prefix)

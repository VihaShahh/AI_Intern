import os
from moviepy.editor import *

# Step 1: Use Wav2Lip for lip-syncing
def generate_lip_sync_video(image_path, audio_path, output_path):
    # Run Wav2Lip inference
    command = f"python inference.py --checkpoint_path wav2lip_gan.pth --face {image_path} --audio {audio_path} --outfile {output_path}"
    os.system(command)

# Step 2: Add eye and head movement (using pre-trained First-Order Motion Model)
def add_eye_head_movement(video_path, motion_model_path, output_path):
    # Run first-order motion model
    command = f"python demo.py --config config/vox-256.yaml --driving_video {video_path} --source_image {video_path} --checkpoint {motion_model_path} --relative --adapt_scale --result_video {output_path}"
    os.system(command)

# Step 3: Merge video with audio
def merge_audio_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    
    video_clip = video_clip.set_duration(audio_clip.duration)
    final_clip = video_clip.set_audio(audio_clip)
    
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Main function
def create_video(image_path, audio_path, output_path, motion_model_path):
    temp_lip_sync_output = "temp_lip_sync_video.mp4"
    temp_motion_output = "temp_motion_video.mp4"

    print("Generating lip-sync video...")
    generate_lip_sync_video(image_path, audio_path, temp_lip_sync_output)

    print("Adding eye and head movements...")
    add_eye_head_movement(temp_lip_sync_output, motion_model_path, temp_motion_output)

    print("Merging audio and final video...")
    merge_audio_video(temp_motion_output, audio_path, output_path)

    # Cleanup temporary files
    os.remove(temp_lip_sync_output)
    os.remove(temp_motion_output)

# Example usage
if __name__ == "__main__":
    # Update the file paths to the full paths where your files are located
    image_path = "C:\\Users\\Viha Shah\\Desktop\\Brainy Neurals\\task_2\\WhatsApp Image 2024-09-23 at 2.48.55 PM.jpeg"  # Input image
    audio_path = "C:\\Users\\Viha Shah\\Desktop\\Brainy Neurals\\task_2\\Recording (2).m4a"  # Input audio
    output_path = "C:\\Users\\Viha Shah\\Desktop\\Brainy Neurals\\task_2\\final_video.mp4"  # Output video
    motion_model_path = "C:\\Users\\Viha Shah\\Desktop\\Brainy Neurals\\Wav2Lip\\fomm_checkpoint.pth"  # Pre-trained motion model path

    create_video(image_path, audio_path, output_path, motion_model_path)

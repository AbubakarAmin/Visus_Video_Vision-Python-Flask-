import cv2
import os
import time

def extract_frames_from_video(video_path, output_folder, interval_ms=500):
    """
    Extracts frames from a video at a specified interval and saves them as images.

    Args:
        video_path (str): The path to the input video file.
        output_folder (str): The path to the folder where extracted frames will be saved.
        interval_ms (int): The interval in milliseconds at which to extract frames (default is 500ms).

    Returns:
        list: A list of file paths to the extracted image frames.
              Returns an empty list if the video cannot be opened.
    """
    # Always resolve output_folder relative to the project root
    output_folder = os.path.abspath(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return []

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the number of frames to skip based on the desired interval
    # frame_skip_interval = (interval_ms / 1000.0) * fps
    
    extracted_frame_paths = []
    frame_count = 0
    next_extraction_time_ms = 0

    print(f"Processing video: {video_path}")
    print(f"Total frames: {total_frames}, FPS: {fps}")
    print(f"Extracting frames every: {interval_ms} milliseconds")

    while True:
        # Read a frame
        ret, frame = cap.read()

        # If no frame is retrieved, we've reached the end of the video
        if not ret:
            break

        # Get the current position in milliseconds
        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

        if current_time_ms >= next_extraction_time_ms:
            # Construct the filename for the extracted frame
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")

            # Save the frame as a JPEG image
            cv2.imwrite(frame_filename, frame)
            extracted_frame_paths.append(frame_filename)
            
            # Print progress
            print(f"Extracted {frame_filename} at {current_time_ms:.2f} ms")

            # Set the next extraction time
            next_extraction_time_ms += interval_ms
        
        frame_count += 1

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

    print(f"\nFinished extracting frames. Total frames extracted: {len(extracted_frame_paths)}")
    return extracted_frame_paths




import os
import shutil # Still useful for deleting the video, and potentially empty parent folders

def delete_video_and_images_by_list(video_path, list_of_image_paths):
    """
    Deletes a specified video file and a list of image files.
    It also attempts to delete the parent directories of the images if they become empty.

    Args:
        video_path (str): The path to the video file to be deleted.
        list_of_image_paths (list): A list of strings, where each string is the
                                     full path to an image file to be deleted.
    """
    # 1. Delete the video file
    if os.path.exists(video_path):
        try:
            os.remove(video_path)
            print(f"Successfully deleted video: {video_path}")
        except OSError as e:
            print(f"Error deleting video {video_path}: {e}")
    else:
        print(f"Video not found, skipping deletion: {video_path}")

    # 2. Delete the specific image files and track their parent directories
    parent_directories_to_check = set() # Use a set to store unique parent directories

    if not list_of_image_paths:
        print("No image paths provided for deletion.")
    else:
        print(f"\nAttempting to delete {len(list_of_image_paths)} images...")
        for image_path in list_of_image_paths:
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print(f"  Deleted image: {os.path.basename(image_path)}")
                    # Add the parent directory to the set for later checking
                    parent_dir = os.path.dirname(image_path)
                    if parent_dir: # Ensure it's not an empty string (e.g., if path is just a filename)
                        parent_directories_to_check.add(parent_dir)
                except OSError as e:
                    print(f"  Error deleting image {image_path}: {e}")
            else:
                print(f"  Image not found, skipping deletion: {image_path}")

    # 3. Attempt to delete parent directories if they are now empty
    if parent_directories_to_check:
        print("\nChecking parent directories for emptiness and deletion...")
        # Sort for consistent output, though not strictly necessary
        sorted_dirs = sorted(list(parent_directories_to_check), key=len, reverse=True) # Delete deepest first
        for p_dir in sorted_dirs:
            if os.path.exists(p_dir):
                try:
                    # Check if the directory is empty
                    if not os.listdir(p_dir):
                        os.rmdir(p_dir) # rmdir only removes empty directories
                        print(f"  Deleted empty directory: {p_dir}")
                    else:
                        print(f"  Directory not empty, skipping deletion: {p_dir}")
                except OSError as e:
                    print(f"  Error deleting directory {p_dir}: {e}")
            else:
                print(f"  Directory not found, skipping deletion: {p_dir}")

# --- Example Usage with the previous frame extraction logic ---



from openai import OpenAI
import os

# --- Configuration ---
OPENROUTER_API_KEY = "<YOUR_API_KEY>"  # Replace with your OpenRouter API key
YOUR_SITE_URL = "<YOUR_SITE_URL>"  # Optional: Site URL for rankings on openrouter.ai.
YOUR_SITE_NAME = "<YOUR_SITE_NAME>" # Optional: Site title for rankings on openrouter.ai.

# --- Initialize OpenAI Client for OpenRouter ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def analyze_video_from_image_urls(image_urls: list[str]) -> str or None:
    """
    Takes a list of image URLs and sends them directly to the OpenRouter API
    (using a vision-capable model like Qwen2.5-VL) for video understanding.
    This function assumes the LLM can access and process external image URLs.

    Args:
        image_urls (list[str]): A list of strings, where each string is a direct URL
                                 to an image (e.g., "http://example.com/image.jpg").
                                 The order of URLs in the list is considered chronological frames.

    Returns:
        str or None: The summarized text description of the video from the API,
                     or None if an error occurred or no URLs were provided.
    """
    if not image_urls:
        print("Error: No image URLs provided to analyze_video_from_image_urls.")
        return None

    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes video content."},
        {"role": "user", "content": []}
    ]

    # Add each image URL directly to the user's message content
    print(f"Preparing {len(image_urls)} image URLs for API analysis...")
    for i, url in enumerate(image_urls):
        print(f"Adding image URL {i+1}/{len(image_urls)}: {url}")
        messages[1]["content"].append(
            {
                "type": "image_url",
                # The 'url' field takes the direct image URL
                "image_url": {"url": url}
            }
        )

    # Add the final text query after all image frames
    messages[1]["content"].append(
        {"type": "text", "text": "The above images are a sequence of frames from a video, presented in chronological order. Please describe the main activities, objects, and scene changes visible across these frames, and provide a concise summary of what happens in the video. Focus on narrative flow and key events."}
    )

    try:
        print(f"Sending {len(image_urls)} image URLs to OpenRouter API for analysis...")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_SITE_NAME,
            },
            model="qwen/qwen2.5-vl-72b-instruct:free", # Ensure this model supports vision with external URLs
            messages=messages,
            max_tokens=4000 # Adjust max_tokens based on expected response length
        )
        print("API Call Successful!")
        return completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred during API call: {e}")
        print("Please check your OpenRouter API key and confirm the model name (e.g., 'qwen2.5-vl-72b-instruct').")
        print("Ensure the model supports multimodal input (images via external URLs + text) and can handle the total token count for your request.")
        return None

import os
import base64
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(base64_image):
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in 4 words in this form: word-word-word-word. Nothing else."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    # Extracting the content from the response
    description = response.choices[0].message.content
    return description

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"New image detected: {event.src_path}")
            self.process_new_image(event.src_path)

    def process_new_image(self, image_path):
        base64_image = encode_image(image_path)
        description = analyze_image(base64_image)
        new_filename = description.replace(" ", "_") + os.path.splitext(image_path)[1]
        new_file_path = os.path.join(os.path.dirname(image_path), new_filename)

        os.rename(image_path, new_file_path)
        print(f'Renamed "{image_path}" to "{new_filename}"')

if __name__ == "__main__":
    folder_path = os.getenv("FOLDER_PATH")

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        print(f"Monitoring folder: {folder_path}. Press Ctrl+C to exit.")
        while True:
            # Keep the script running
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
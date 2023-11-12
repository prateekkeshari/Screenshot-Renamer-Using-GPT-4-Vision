# Screenshot Renamer

This Python script uses OpenAI's GPT-4 Vision model to analyze images and rename them based on their content. It monitors a specified folder for new images and automatically processes them as they are added.

## Dependencies

The script requires the following Python packages:

- `os`
- `base64`
- `openai`
- `watchdog`
- `dotenv`

You can install these dependencies using pip:

```bash
pip install python-dotenv watchdog openai
```
## Environment Variables

The script uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `FOLDER_PATH`: The path to the folder you want to monitor for new images.

You can set these variables in a `.env` file in the same directory as the script.

## How It Works

1. The script starts by loading the environment variables and setting the OpenAI API key.
2. It defines a function `encode_image` to convert an image to a base64 string.
3. It defines a function `analyze_image` to send a request to the OpenAI API, asking it to describe the image in a specific format.
4. It defines a class `ImageHandler` that inherits from `FileSystemEventHandler`. This class has a method `on_created` that gets triggered whenever a new file is created in the monitored folder. If the new file is an image, it processes the image by encoding it, analyzing it, and renaming it based on the analysis.
5. Finally, it sets up a `watchdog.Observer` to monitor the specified folder and starts the observer.

## Usage

To use the script, simply run it with Python:

```bash
python script.py
```

The script will start monitoring the specified folder. Whenever a new image is added to the folder, the script will automatically analyze the image and rename it based on its content.

## Note
This script only processes new images added to the folder after the script starts. It does not process existing images in the folder.
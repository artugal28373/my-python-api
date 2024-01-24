from flask import Flask, request, jsonify
import requests
import os

# Generic WSGI server setup
from werkzeug.serving import run_simple

app = Flask(__name__)

@app.route("/", methods=["POST"])
def download_image():
    image_link = request.get_json()["url"]

    try:
        # Extract the image code from the URL
        image_code = image_link.split("/")[-1]

        # Set the download directory
        #download_dir = "/content/"

        # Ensure the directory exists
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Get the actual image URL
        download_url = f"https://i.imgbb.com/{image_code}"

        # Send the GET request
        response = requests.get(download_url)

        # Check for successful response
        if response.status_code == 200:
            # Prepare the filename with extension
            filename = f"{image_code}{os.path.splitext(image_link)[1]}"

            # Write the image data to file
            with open(os.path.join(download_dir, filename), "wb") as file:
                file.write(response.content)

            return jsonify({"success": True, "filename": filename})
        else:
            return jsonify({"success": False, "error": f"Error downloading image: {response.status_code}"})
    except Exception as e:
        return jsonify({"success": False, "error": f"General error: {e}"})

if __name__ == "__main__":
    # Replace host and port with your server's specific values
    run_simple("localhost", 5000, app)


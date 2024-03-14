import io
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import pyautogui
from PIL import Image, ImageGrab, ImageDraw
import streamlink
from pynput import keyboard  # Import the keyboard module from pynput

HOST = '192.168.0.118'
# HOST = '127.0.0.1'
PORT = 4002
FPS = 30
STREAM_URL = ''
TARGET_QUALITY_STEP = 10  # Set the step size for quality adjustments

# Global variables
last_request_time = 0
target_quality = 70
keyboard_lock = threading.Lock()


# Define the request handler class
class MyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        global last_request_time  # Access the global variable
        if last_request_time != 0:
            elapsed_time = time.time() - last_request_time
            print(f"Time between requests: {elapsed_time} seconds")
        last_request_time = time.time()  # Update the last request time

        # Get the requested path from the request
        path = self.path

        # Check if the path is "/stream"
        if path == "/stream":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            stream_url_bytes = STREAM_URL.encode('utf-8')
            if stream_url_bytes != "":
                print(stream_url_bytes)
            else:
                print("no stream to share, so go live plz")
            self.wfile.write(stream_url_bytes)
        elif path == "/live":
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            with keyboard_lock:
                data = self.get_frame(target_resolution=(640, 360), target_quality=target_quality)
            self.wfile.write(data)
            print("Sent data size:", len(data))

    def get_frame(self, target_resolution=(640, 480), target_quality=70):
        start_time_total = time.time()
        im = ImageGrab.grab()
        end_time_total = time.time()
        elapsed_time_total = end_time_total - start_time_total
        print(f"Time to capture screen: {elapsed_time_total} seconds")

        # Get cursor position
        cursor_x, cursor_y = pyautogui.position()

        # Draw a red circle at the cursor position
        draw = ImageDraw.Draw(im)
        circle_radius = 12
        draw.ellipse((cursor_x - circle_radius, cursor_y - circle_radius,
                      cursor_x + circle_radius, cursor_y + circle_radius),
                     outline="red", width=2)

        start_time_total = time.time()
        im_resized = im.resize(target_resolution, resample=Image.NEAREST)
        end_time_total = time.time()
        elapsed_time_total = end_time_total - start_time_total
        print(f"Time to resize image: {elapsed_time_total} seconds")

        start_time_total = time.time()
        screenfile = io.BytesIO()
        im_resized.save(screenfile, format="jpeg", quality=target_quality, optimize=True)
        end_time_total = time.time()
        elapsed_time_total = end_time_total - start_time_total
        print(f"Time to convert to jpeg with less quality: {elapsed_time_total} seconds")

        return screenfile.getvalue()


def keyboard_input_handler():
    global target_quality
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


def on_key_press(key):
    global target_quality
    try:
        # Handle key press events
        if key.char == '-':
            if target_quality > 10:
                target_quality -= TARGET_QUALITY_STEP
                print(f"Quality is now at: {target_quality}")
        elif key.char == '=':
            if target_quality < 91:
                target_quality += TARGET_QUALITY_STEP
                print(f"Quality is now at: {target_quality}")
    except AttributeError:
        pass  # Ignore non-character keys


if __name__ == "__main__":
    streams = streamlink.streams("https://www.twitch.tv/strayeddy")
    if streams != {}:
        STREAM_URL = streams["best"].url
        print(STREAM_URL)

    # Start the keyboard input thread
    keyboard_thread = threading.Thread(target=keyboard_input_handler, daemon=True)
    keyboard_thread.start()

    # Set the server address and port
    server_address = (HOST, PORT)

    # Create the HTTP server
    httpd = HTTPServer(server_address, MyRequestHandler)

    print(f'Starting server on {server_address[0]}:{server_address[1]}...')
    httpd.serve_forever()
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

HOST = '192.168.0.118'
PORT = 4002
VIDEO_FPS = 60
VIDEO_PATH = "../captured_videos/hls.m3u8"

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received GET request for {self.path}")

        file_path = self.path.lstrip('/')

        # Check if the video file exists
        if os.path.exists(file_path):

            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'application/vnd.apple.mpegurl')
            self.end_headers()

            # Read the video file as bytes and send it to the client
            with open(file_path, 'rb') as video_file:
                video_data = video_file.read()
                self.wfile.write(video_data)
        else:
            # Send response status code indicating video not found
            self.send_response(404)

            # Send headers
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Send a message indicating the video is not available
            self.wfile.write(b'Video not available')

class VideoCaptureThread(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True  # Daemonize the thread

    def run(self):
        x11_display = ":0"
        video_input = ffmpeg_streaming.input(x11_display, capture=True, screen=True)
        hls = video_input.hls(Formats.h264(), hls_list_size=10, hls_time=5)
        hls.flags('delete_segments')

        _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        _1080p = Representation(Size(1920, 1080), Bitrate(750 * 1024, 192 * 1024))
        hls.representations(_720p)
        hls.output('captured_videos/hls.m3u8')

def start_server():
    # Set the server address and port
    server_address = (HOST, PORT)

    # Create the HTTP server with the custom request handler
    httpd = HTTPServer(server_address, MyRequestHandler)

    print(f'Starting server on {server_address[0]}:{server_address[1]}...')
    httpd.serve_forever()

if __name__ == "__main__":
    # Start the video capture thread
    video_capture_thread = VideoCaptureThread()
    video_capture_thread.start()

    # Start the HTTP server on the main thread
    start_server()

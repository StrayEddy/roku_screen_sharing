# Streaming Server
import io
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image, ImageGrab

HOST = '192.168.0.118'
# HOST = '127.0.0.1'
PORT = 4002
FPS = 30

# Define the request handler class
class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		start_time_total = time.time()
		# Send response status code
		self.send_response(200)

		# Send headers
		self.send_header('Content-type', 'text/plain')
		self.end_headers()

		# Send message back to client
		start_time = time.time()
		# data = self.get_frame(target_resolution=(1280, 720), target_quality=15)
		data = self.get_frame(target_resolution=(320*2, 180*2), target_quality=25)
		end_time = time.time()
		print(f"Time taken for get_frame: {end_time - start_time} seconds")

		self.wfile.write(data)
		print("Sent data size:", len(data))

		end_time_total = time.time()
		elapsed_time_total = end_time_total - start_time_total
		print(f"Time taken for do_GET: {elapsed_time_total} seconds")

	def get_frame(self, target_resolution=(640, 480), target_quality=75):
		start_time = time.time()
		im = ImageGrab.grab()
		end_time = time.time()
		print(f"Time taken for grab: {end_time - start_time} seconds")

		# Resize the image to the target resolution
		start_time = time.time()
		im_resized = im.resize(target_resolution, resample=Image.NEAREST)
		end_time = time.time()
		print(f"Time taken for resize: {end_time - start_time} seconds")

		start_time = time.time()
		screenfile = io.BytesIO()
		im_resized.save(screenfile, format="jpeg", quality=target_quality, optimize=True)
		# im_resized.save(screenfile, format="jpeg", optimize=True)
		# im_resized.save(screenfile, format="webp", quality=50, optimize=True)

		end_time = time.time()
		print(f"Time taken for save: {end_time - start_time} seconds")

		return screenfile.getvalue()

# Set the server address and port
server_address = (HOST, PORT)

# Create the HTTP server
httpd = HTTPServer(server_address, MyRequestHandler)

print(f'Starting server on {server_address[0]}:{server_address[1]}...')
httpd.serve_forever()



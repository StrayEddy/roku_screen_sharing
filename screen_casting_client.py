import requests
import cv2
import numpy as np

server_url = 'http://192.168.0.118:4002'  # Replace with your server details

while True:
    response = requests.get(server_url)

    if response.status_code == 200:
        print(f"Received data size: {len(response.content)}")

        # Convert the received binary data to a NumPy array
        nparr = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Display the image using OpenCV
        cv2.imshow('Received Image', img)

        # Wait for a key press and check if it's 'q' to exit the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    else:
        print(f"Failed to receive data. HTTP Status Code: {response.status_code}")

# Close the OpenCV window when exiting the loop
cv2.destroyAllWindows()

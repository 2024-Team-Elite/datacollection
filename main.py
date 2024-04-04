import depthai as dai
import cv2
import os

# Create output directory if it doesn't exist
output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

# Create pipeline
pipeline = dai.Pipeline()

# Define camera node
cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080P)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Create output queue
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.video.link(xout.input)

# Connect to device
with dai.Device(pipeline) as device:
    # Output queue
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    while True:
        # Get frame from output queue
        frame = q.get()

        # Get BGR frame
        img = frame.getCvFrame()

        # Display frame
        cv2.imshow("Frame", img)

        # Save frame to file
        filename = os.path.join(output_dir, f"image_{time.time()}.jpg")
        cv2.imwrite(filename, img)

        # Wait for key press to exit
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()


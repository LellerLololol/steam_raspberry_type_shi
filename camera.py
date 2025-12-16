import cv2 as cv
from ultralytics import YOLO
import time
import asyncio



async def camera_main(queue):
	model = YOLO("yolo11n.pt") 

	capture = cv.VideoCapture(0)
	capture.set(cv.CAP_PROP_FRAME_WIDTH, 160)
	capture.set(cv.CAP_PROP_FRAME_HEIGHT, 120)
	capture.set(cv.CAP_PROP_FPS, 10)

	if not capture.isOpened():
		print("Cannot open camera. Exiting...")
		exit()
	while True:
		ret, frame = capture.read()
		#print("Camera loop running...")   # DEBUG
		if not ret:
			print("Cannot receive frame. Exiting...")
			break
		frame_count = 0
		frame_count += 1
		start_time = time.time()
			
		results = model(frame, imgsz=128, classes=[0], conf=0.42, verbose=False, device="cpu")
		
		num_people = len(results[0].boxes)
		#fps = 1 / (time.time() - start_time)
		#print(f"People detected: {num_people}. FPS: {fps}")
		
		# Push result to queue (overwrites old data)
		if queue.full():
			queue.get_nowait()   # remove oldest entry
		queue.put_nowait(num_people)

		await asyncio.sleep(0) # Yield control to event loop
		

	

if __name__ == "__main__":
	print("Starting person detection...")
	camera_main()
	
	capture.release()

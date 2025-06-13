import time
import cv2


def capture_frame(rtsp_url, output_filename = 'output.jpg'):
	"""
	Captures a single frame from an RTSP stream and saves it as an image.

	Args:
		rtsp_url (str): The RTSP URL of the video stream.
		output_path (str): The path to save the captured image.
	"""
	cap = cv2.VideoCapture(rtsp_url)

	if not cap.isOpened():
		print(f"ERROR Could not open RTSP stream: {rtsp_url}")
	else:
		ret, frame = cap.read()
		if not ret:
			print("ERROR Could not read frame from RTSP stream.")
		else:
			cv2.imwrite(output_filename, frame)
			print(f"Image saved as: {output_filename}")
		cap.release()


def main():

	cap_west = cv2.VideoCapture("rtsp://localhost:8554/evwest")
	if not cap_west.isOpened():
		print("ERROR Could not open RTSP stream evwest.")
	else:
		ret, frame = cap_west.read()
		if not ret:
			print("ERROR Could not read frame from evwest RTSP stream.")
		else:
			cv2.imwrite("evwest_cap1.jpg", frame)
			print("Saved evwest_cap1.jpg")

	cap_east = cv2.VideoCapture("rtsp://localhost:8554/eveast")
	if not cap_east.isOpened():
		print("ERROR Could not open RTSP stream eveast.")
	else:
		ret, frame = cap_east.read()
		if not ret:
			print("ERROR Could not read frame from eveast RTSP stream.")
		else:
			cv2.imwrite("eveast_cap1.jpg", frame)
			print("Saved eveast_cap1.jpg")

	time.sleep(10)

	if not cap_west.isOpened():
		print("ERROR Could not open RTSP stream evwest again.")
	else:
		ret, frame = cap_west.read()
		if not ret:
			print("ERROR Could not read frame from evwest RTSP stream again.")
		else:
			cv2.imwrite("evwest_cap2.jpg", frame)
			print("Saved evwest_cap2.jpg")

	if not cap_east.isOpened():
		print("ERROR Could not open RTSP stream eveast again.")
	else:
		ret, frame = cap_east.read()
		if not ret:
			print("ERROR Could not read frame from eveast RTSP stream again.")
		else:
			cv2.imwrite("eveast_cap2.jpg", frame)
			print("Saved eveast_cap2.jpg")

	cap_west.release()
	cap_east.release()

#	capture_frame("rtsp://localhost:8554/evwest", "evwest_cap1.jpg")
#	capture_frame("rtsp://localhost:8554/eveast", "eveast_cap1.jpg")
#	time.sleep(10)
#	capture_frame("rtsp://localhost:8554/evwest", "evwest_cap2.jpg")
#	capture_frame("rtsp://localhost:8554/eveast", "eveast_cap2.jpg")


if __name__ == "__main__":
	main()

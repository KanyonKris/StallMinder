from PIL import Image, ImageChops
import subprocess
import io
import time


def capture_frame(rtsp_url, output_path="output.jpg"):
    """
    Captures a single frame from an RTSP stream and saves it as an image.

    Args:
        rtsp_url (str): The RTSP URL of the video stream.
        output_path (str): The path to save the captured image.
    """
    try:
        process = subprocess.run(
            ['ffmpeg', '-i', rtsp_url, '-vframes', '1', '-f', 'image2', '-q:v', '2', '-'],
            capture_output=True,
            check=True
        )
        image_data = process.stdout
        image = Image.open(io.BytesIO(image_data))
        image.save(output_path)
        print(f"Frame captured and saved to {output_path}")

    except subprocess.CalledProcessError as e:
         print(f"Error capturing frame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def detect_change(image_1, image_2, threshold=20):
	"""
	Detects changes between two images.

	Args:
            image_path1: Path to the first image.
            image_path2: Path to the second image.
            threshold: Sensitivity threshold for change detection (0-255).

        Returns:
            True if changes are detected, False otherwise.
        """
	#img1 = Image.open(image_path1).convert("RGB")
	#img2 = Image.open(image_path2).convert("RGB")

	if imgage_1.size != imgage_2.size:
		raise ValueError("Images must have the same dimensions")

	diff = ImageChops.difference(imgage_1, imgage_2)
	if diff.getbbox() is None:
		return False  # Images are identical

	pixels = diff.getdata()
	changed_pixels = [p for p in pixels if sum(p) > threshold]

	return len(changed_pixels) > 0


def main():
	originX = 66  # Corner of curb, stall 1 lower left
	originY = 325
	stalls = (
		(31, -101, 12, 81),
		(70, -98, 20, 71),
		(114, -101, 24, 76),
		(169, -106, 32, 85),
		(224, -110, 37, 90),
		(284, -113, 46, 90),
		(348, -115, 46, 90),
		(412, -117, 44, 90),
		(474, -119, 35, 90),
		(530, -122, 27, 90)
		)
#	capture_frame('http://leh-ev-charging:8554/evwest/', 'evwest_new.jpg')
#	capture_frame('http://leh-ev-charging:8554/eveast/', 'eveast_new.jpg')
#	time.sleep(5)
	image_old = Image.open('stall1car.jpg').convert('RGB')
	image_new = Image.open('stall1nocar.jpg').convert('RGB')
	stall_box_left = originX + stalls[0][0]
	stall_box_upper = originY + stalls[0][1]
	stall_box_right = originX + stalls[0][2]
	
	image_stall_1_old = Image.crop(((originX + stalls[0][0]), (originY + stalls[0][1]), (originX + stalls[0][0] + stalls[0][2]
	
	res = detect_change('evw0001.jpg', 'evw0004.jpg', 20)
	print(res)

if __name__ == "__main__":
	main()


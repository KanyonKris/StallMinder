from PIL import Image, ImageChops, ImageStat
import subprocess
import io
import time


def capture_frame(rtsp_url, output_path = None):
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
        if output_path != None:
        	image.save(output_path)
        	print(f"Frame captured and saved to {output_path}")
        return image

    except subprocess.CalledProcessError as e:
         print(f"Error capturing frame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def detect_change(image_1, image_2, threshold=50):
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

	if image_1.size != image_2.size:
		raise ValueError("Images must have the same dimensions")

	diff = ImageChops.difference(image_1, image_2)
#	if diff.getbbox() is None:
#		return False  # Images are identical

	pixels = diff.getdata()
	changed_pixels = [p for p in pixels if sum(p) > threshold]

	return len(changed_pixels) > 0


def threshold(pixel):
	if sum(pixel) > 50:
		return pixel
	else:
		return 0


def main():
	interval = 15
	threshold = 50
	originX = 22  # Corner of curb, stall 1 lower left
	originY = 286
	empty_asphalt = (originX + 125, originY - 235, originX + 125 + 430, originY - 235 + 100)
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
	start_time = time.monotonic()
#	time.sleep(interval - ((time.monotonic() - start_time) % interval))
#	capture_frame('http://leh-ev-charging:8554/evwest/', 'evwest_new.jpg')
#	capture_frame('http://leh-ev-charging:8554/eveast/', 'eveast_new.jpg')
#	time.sleep(5)
	image_old = Image.open('images/stall1car.jpg').convert('RGB')
	image_new = Image.open('images/stall1nocar.jpg').convert('RGB')
	image_old = Image.open('images/cars1-3-6-8-9-10.jpg').convert('RGB')
	image_empty_asphalt = image_new.crop(empty_asphalt)
	stats_asphalt = ImageStat.Stat(image_empty_asphalt)
	asphalt_color = (round(stats_asphalt.mean[0]), round(stats_asphalt.mean[1]), round(stats_asphalt.mean[2]))
	print(f"Asphalt color: {asphalt_color}")
	count = 1
	for stall in stalls:
		stall_box_left = originX + stall[0]
		stall_box_upper = originY + stall[1]
		stall_box_right = originX + stall[0] + stall[2]
		stall_box_lower = originY + stall[1] + stall[3]
		stall_area = stall[2] * stall[3]
		image_stall_old = image_old.crop((stall_box_left, stall_box_upper, stall_box_right, stall_box_lower))
		image_stall_new = image_new.crop((stall_box_left, stall_box_upper, stall_box_right, stall_box_lower))
		image_diff = ImageChops.difference(image_stall_old, image_stall_new)
		pixels = image_diff.getdata()
		changed_pixels = [p for p in pixels if sum(p) > threshold]
		changed_amount = round(len(changed_pixels) * 100 / stall_area)
		image_thresh = Image.eval(image_diff, lambda px: 0 if px < threshold else px)
		image_stats_new = ImageStat.Stat(image_stall_new)
		image_stats_old = ImageStat.Stat(image_stall_old)
		print(f"Box {count}: changed_amount: {changed_amount}, new mean: {image_stats_new.mean} old mean: {image_stats_old.mean}")
		image_new.paste(image_thresh, (stall_box_left, stall_box_upper, stall_box_right, stall_box_lower))
		count += 1
	image_new.save('debug.jpg')

if __name__ == "__main__":
	main()

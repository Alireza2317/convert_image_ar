from PIL import Image
import os
import sys
from datetime import datetime


def crop_to_ar(image_path: str, output_path: str, target_ar: float = 16/9) -> None:
	img = Image.open(image_path)

	width, height = img.size
	current_ar: float = width / height

	if current_ar > target_ar:
		# the image is wider than desired ar
		# should crop the sides / reduce width
		target_width: int = int(height * target_ar)
		target_height: int = height
	else:
		# the image is taller than desired ar
		# should crop top&bottom / reduce height
		target_width: int = width
		target_height: int = int(width / target_ar)


	# symmetric crop from the center
	# calculating crop box
	x_min: int = abs(width - target_width) // 2
	x_max: int = x_min + target_width
	y_min: int = abs(height - target_height) // 2
	y_max: int = y_min + target_height


	cropped_img = img.crop(
		(x_min, y_min, x_max, y_max)
	)

	cropped_img.save(output_path, quality=100, subsampling=0)


def main():
	to_crop_path: str = sys.argv[1]
	output_path: str = f'{to_crop_path}/cropped_images_{datetime.now().strftime("%y%m%d")}'
	os.makedirs(output_path, exist_ok=True)

	if not os.path.isdir(to_crop_path):
		print('Please enter a valid path!')
		exit(1)

	for filename in os.listdir(to_crop_path):
		if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
			continue

		image_path: str = f'{to_crop_path}/{filename}'

		crop_to_ar(
			image_path, f"{output_path}/{filename}"
		)

if __name__ == "__main__":
	main()

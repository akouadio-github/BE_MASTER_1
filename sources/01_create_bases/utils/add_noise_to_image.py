import argparse
import os
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rich.progress import track

def add_random_noise_to_images(root_path, n1, n2):
    # Iterate through each subfolder

    for folder_name in track(os.listdir(root_path), description='Processing...'):
        folder_path = os.path.join(root_path, folder_name)
        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Get list of images in the 'images' subfolder
            images_folder = os.path.join(folder_path, 'images')
            image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

            # Randomly choose the number of images to modify between n1 and n2
            num_images_to_modify = random.randint(n1, n2)

            # Randomly select num_images_to_modify images
            selected_images = random.sample(image_files, min(num_images_to_modify, len(image_files)))

            # Apply random noise to each selected image
            for image_file in selected_images:
                image_path = os.path.join(images_folder, image_file)
                img = Image.open(image_path)

                if img.mode == 'P':
                    img = img.convert('RGB')
                # Apply random transformations
                if random.choice([True, False]):
                    img = img.rotate(random.uniform(-2, 5))
                if random.choice([True, False]):
                    n = random.randint(0,5)
                    img = img.filter(ImageFilter.GaussianBlur(radius=n))
                if random.choice([True, False]):
                    img = ImageOps.grayscale(img)
                if random.choice([True, False]):
                    img = ImageEnhance.Contrast(img.convert("RGB")).enhance(random.uniform(0.5, 1.5))
                if random.choice([True, False]):
                    img = ImageEnhance.Brightness(img).enhance(random.uniform(0.5, 1.5))
                if random.choice([True, False]):
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)

                # Save the modified image
                modified_image_path = os.path.join(images_folder, f"m_{image_file}")
                img.save(modified_image_path)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Ajouter du bruit au jeu de données')
    # parser.add_argument('-dir', '--directory', help='Chemin du jeu de données. Default : ./train_test_dataset/' )
    # args = parser.parse_args()

    root_directory = "../../../train_test_dataset/"
    n1 = 5
    n2 = 50
    add_random_noise_to_images(root_directory, n1, n2)

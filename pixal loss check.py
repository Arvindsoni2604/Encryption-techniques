from PIL import Image
import numpy as np

def calculate_pixel_loss(original_path, restored_path):
    """Compare original and restored images to detect pixel loss"""
    original = np.array(Image.open(original_path).convert('RGB'))
    restored = np.array(Image.open(restored_path).convert('RGB'))

    if original.shape != restored.shape:
        raise ValueError("Image dimensions do not match!")

    # Count pixels that changed
    pixel_diff = np.sum(original != restored)
    total_pixels = original.size  # Total pixels in image

    # Calculate pixel loss percentage
    pixel_loss = (pixel_diff / total_pixels) * 100
    return pixel_diff, pixel_loss

# Example usage
original_image = "pikachu.JPG"
restored_image = "decrypted.JPG" 

changed_pixels, loss_percentage = calculate_pixel_loss(original_image, restored_image)
print(f"Pixel Difference: {changed_pixels} pixels")
print(f"Pixel Loss: {loss_percentage:.4f}%")

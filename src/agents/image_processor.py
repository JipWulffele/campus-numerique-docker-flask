from PIL import Image
import os
import math

class ImageProcessor:
    def __init__(self, downscale_image, max_pixels):
        self.downscale = downscale_image # Whether to downscale images True/False
        self.max_pixels = max_pixels

    def downscale_image(self, filepath):
        """Downscale image if it exceeds max pixels."""
        if not self.downscale_image:
            return Image.open(filepath)
        with Image.open(filepath) as img:
            width, height = img.size
            current_pixels = width * height

            # Need to downscale
            if current_pixels > self.max_pixels:
                scale_factor = math.sqrt(self.max_pixels / current_pixels)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            return img.copy() # downscaled or not
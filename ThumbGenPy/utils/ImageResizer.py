from PIL import Image
from io import BytesIO


def resize_image(bytes, new_width, new_height):
    # Open the image
    image = Image.open(BytesIO(bytes))

    # Calculate the aspect ratio
    aspect_ratio = image.width / image.height

    # Calculate the new height based on the aspect ratio
    calculated_height = int(new_width / aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, calculated_height))

    # Return the resized image as bytes
    bytes_io = BytesIO()
    resized_image.save(bytes_io, format='JPEG')
    resized_image_bytes = bytes_io.getvalue()
    return resized_image_bytes

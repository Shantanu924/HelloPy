import turtle
from PIL import Image, ImageOps
import numpy as np

def convert_image_to_sketch(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Convert to grayscale
    img_gray = ImageOps.grayscale(img)
    
    # Apply edge detection (using a simple threshold)
    img_gray = img_gray.filter(Image.Filter.FIND_EDGES)
    
    # Resize for turtle drawing speed (optional, 100x100 for faster performance)
    img_resized = img_gray.resize((100, 100))
    
    # Convert to a numpy array
    pixel_data = np.array(img_resized)
    return pixel_data

def draw_with_turtle(pixel_data):
    turtle.speed(0)  # Fastest drawing speed
    turtle.colormode(255)
    turtle.penup()
    
    rows, cols = pixel_data.shape
    cell_size = 5  # Adjust as needed for size of the drawing
    
    # Start from top-left corner
    start_x = -cols * cell_size // 2
    start_y = rows * cell_size // 2
    
    for y in range(rows):
        for x in range(cols):
            brightness = pixel_data[y, x]
            if brightness < 128:  # Adjust threshold as needed
                # Move to the position
                turtle.goto(start_x + x * cell_size, start_y - y * cell_size)
                turtle.pendown()
                turtle.dot(2, "black")
                turtle.penup()
    
    turtle.done()

def main():
    # Ask the user for an image file path
    image_path = input("Enter the path to the image file: ")
    
    try:
        # Process the image and get the sketch data
        pixel_data = convert_image_to_sketch(image_path)
        
        # Use turtle to draw the sketch
        draw_with_turtle(pixel_data)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

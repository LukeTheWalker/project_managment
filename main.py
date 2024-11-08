from PIL import Image
import math
import os

# Load a sample image to get dimensions
sample_image_path = "cut_images/Cathedral.png"
sample_image = Image.open(sample_image_path)
parallelogram_width, parallelogram_height = sample_image.size

# Function to create a hexagon grid
def create_hexagon_grid(parallelogram_image_paths, hexagon_rows, hexagon_cols, save_path="hexagon_grid.png"):
    # Calculate offsets for positioning
    hexagon_width = parallelogram_width
    hexagon_height = parallelogram_height * math.sqrt(3) / 2

    # Calculate final image dimensions
    grid_width = int(hexagon_cols * hexagon_width * 1.5 + parallelogram_width / 2)
    grid_height = int(hexagon_rows * hexagon_height * 2 + parallelogram_height / 2)
    
    # Create a blank canvas
    canvas = Image.new("RGBA", (grid_width, grid_height), (255, 255, 255, 0))

    cnt = 0

    # Place each hexagon
    for row in range(hexagon_rows):
        for col in range(hexagon_cols):
            # Calculate position offset for each hexagon based on row and column
            x_offset = col * hexagon_width * 1.5
            y_offset = row * hexagon_height * 2
            
            # Offset alternate columns to create a staggered hexagonal pattern
            if row % 2 == 1:
                x_offset += hexagon_width * 0.75

            # Load images for the three parallelograms of a hexagon
            for i, angle in enumerate([0, -120, 120]):
                img_path = parallelogram_image_paths[cnt % len(parallelogram_image_paths)]
                img = Image.open(img_path)
                
                # Rotate the image around its center
                rotated_img = img.rotate(angle, expand=True, center=(img.width / 2, img.height / 2))
                
                # Calculate position for each parallelogram within the hexagon
                if i == 0:
                    img_x, img_y = x_offset, y_offset
                elif i == 1:
                    img_x, img_y = x_offset + parallelogram_width * 0.5,  y_offset
                elif i == 2:
                    img_x, img_y = x_offset, y_offset + parallelogram_height * 0.5

                # Paste rotated image onto the canvas
                canvas.paste(rotated_img, (int(img_x), int(img_y)), rotated_img)
                cnt += 1

    # Save the result
    canvas.save(save_path)
    print(f"Hexagon grid saved as {save_path}")

# Path to directory containing the parallelogram images
parallelogram_folder = "cut_images"
parallelogram_image_paths = [os.path.join(parallelogram_folder, f) for f in os.listdir(parallelogram_folder) if f.endswith(".png")]

# Parameters: Number of hexagon rows and columns in the grid
hexagon_cols = 3
hexagon_rows = math.ceil(len(parallelogram_image_paths) / (3 * hexagon_cols))

# Run the function to create the hexagonal grid
create_hexagon_grid(parallelogram_image_paths, hexagon_rows, hexagon_cols)

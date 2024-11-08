import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from math import cos, sin, tan, pi
import json

size = 1024 / (1 + cos(pi/3))

par_position = lambda width, height: [
    (0, height - size * sin(pi / 3) / 2),
    (size, height - size * sin(pi / 3) / 2),
    (size + size * cos(pi / 3), height - size * sin(pi / 3) - size * sin(pi / 3) / 2),
    (size * cos(pi / 3), height - size * sin(pi / 3) - size * sin(pi / 3) / 2)
]

house_images = {
    "active"  : "house_green.png",
    "once"    : "house_purple.png",
    "passive" : "house_brown.png",
}

def insert_newlines(text, n):
    result = ''
    count = 0

    for char in text:
        if char == '\n':
            count = 0  # Reset count if a newline is found
        if char == ' ':
            if count >= n:
                result += '\n'  # Replace space with newline if the limit is reached
                count = 0  # Reset the count
            else:
                result += char  # Otherwise, just add the space
        else:
            result += char
            count += 1

    return result
# load into a json al the informations from the buildings inside game/buildings.json
with open('game/buildings.json') as f:
    buildings = json.load(f)

def add_effect_to_building(building, effect):
    # create a new image with the same size as the building
    effect_img = Image.new('RGBA', building.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(effect_img)

    # draw the text in the image
    # Calculate the position to start the text at the top of the parallelogram

    effect = insert_newlines(effect, 20)

    fontsize = 40

    font = ImageFont.truetype("Helvetica", fontsize)

    text_width = max([d.textlength(line, font=font) for line in effect.split("\n")])

    text_height = fontsize * effect.count('\n') + fontsize

    # start_x = building.size[0] - size / 2 - ( size - text_width + 40)
    start_y = 225
    start_x = (start_y) / tan(pi / 4) + text_width / 2 + 20

    # Draw rounded rectangle
    rect_x0 = start_x - text_width / 2 - 10
    rect_y0 = start_y - 10
    rect_x1 = start_x + text_width / 2 + 10
    rect_y1 = start_y + text_height + 10

    d.rounded_rectangle(
        [rect_x0, rect_y0, rect_x1, rect_y1], 
        radius=10, 
        fill=(255, 255, 255, 200)
    )

    # Draw text
    d.text(
        xy=(start_x, start_y), 
        text=effect,
        fill=(0, 0, 0, 255),
        font=font,
        anchor='ma'
    )

    # combine the two images
    out = Image.alpha_composite(building.convert('RGBA'), effect_img)

    return out

def add_cost_to_building(building, cost, points, effect_type):
    # create a new image with the same size as the building
    cost_img = Image.new('RGBA', building.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(cost_img)

    shapes = [
        lambda x, y, r: d.ellipse([x - r, y - r, x + r, y + r], fill="red", outline="red", width=3),  # Circle
        lambda x, y, r: d.polygon([x, y - r, x - r, y + r, x + r, y + r], fill="green", outline="green", width=3),  # Triangle
        lambda x, y, r: d.polygon([x - r, y - r, x + r, y - r, x + r, y + r, x - r, y + r], fill="blue", outline="blue", width=3),  # Square
        lambda x, y, r: d.polygon([x, y - r, x + r * cos(pi / 4), y - r * cos(pi / 4), x + r, y, x + r * cos(pi / 4), y + r * cos(pi / 4), x, y + r, x - r * cos(pi / 4), y + r * cos(pi / 4), x - r, y, x - r * cos(pi / 4), y - r * cos(pi / 4)], fill="yellow", outline="yellow", width=3),  # Pentagon
        lambda x, y, r: d.polygon([(x + r * cos(2 * pi * i / 6), y + r * sin(2 * pi * i / 6)) for i in range(6)], fill="cyan", outline="cyan", width=3)  # Hexagon
    ]

    # Draw the cost shapes
    x, y = building.width - size, 150
    r = 20  # Radius/size of the shapes

    # Calculate the bounding box for the cost shapes
    total_width = sum((2.5 * r * int(char)) for char in cost)
    rect_x0 = x - r - 10
    rect_y0 = y - r - 10
    rect_x1 = x + total_width - r + 10
    rect_y1 = y + r + 10

    # Draw rounded rectangle
    d.rounded_rectangle(
        [rect_x0, rect_y0, rect_x1, rect_y1], 
        radius=10, 
        fill=(255, 255, 255, 200)
    )

    for i, char in enumerate(cost):
        num = int(char)
        for _ in range(num):
            shapes[min(i, len(shapes) - 1)](x, y, r)
            x += 2.5 * r # Move to the right for the next shape

    if len(str(points)) > 1:
        points = "*"

    # Draw the points box
    points_text = f"{points}"
    points_fontsize = 50
    points_font = ImageFont.truetype("Helvetica", points_fontsize, index=1)
    points_text_width = d.textlength(points_text, font=points_font)
    points_text_height = points_fontsize

    points_start_x = building.width - 200
    points_start_y = y

    # Draw rounded rectangle for points
    points_rect_x0 = points_start_x - 30
    points_rect_y0 = points_start_y - 30
    points_rect_x1 = points_start_x + 30
    points_rect_y1 = points_start_y + 30

    d.rounded_rectangle(
        [points_rect_x0, points_rect_y0, points_rect_x1, points_rect_y1], 
        radius=10, 
        fill=(255, 255, 255, 200)
    )

    # Draw points text
    d.text(
        xy=(points_start_x, points_start_y), 
        text=points_text,
        fill=(0, 0, 0, 255),
        font=points_font,
        anchor='mm'
    )

    # Load one of the house images
    house_img_path = os.path.join('houses', house_images[effect_type])
    house_img = Image.open(house_img_path).convert('RGBA')

    house_img = house_img.resize((int(100), int(100)))

    # Calculate the position to paste the house image next to the cost
    house_y = int(rect_y0) - house_img.height // 5
    house_x = int((points_rect_x0 + rect_x1) // 2 - house_img.width // 2)
    # house_x = int((house_y) / tan(pi / 6) + size * 3 / 5)

    # Draw a white rounded box for clarity
    clarity_box_x0 = house_x - 10 
    clarity_box_y0 = house_y - 10
    clarity_box_x1 = house_x + 10 + house_img.width
    clarity_box_y1 = house_y + 10 + house_img.height

    d.rounded_rectangle(
        [clarity_box_x0, clarity_box_y0, clarity_box_x1, clarity_box_y1], 
        radius=15, 
        fill=(255, 255, 255, 200)
    )

    # Combine the two images again to include the clarity box
    out = Image.alpha_composite(building.convert('RGBA'), cost_img)

    # Resize the house image to fit next to the cost
    # Paste the house image onto the effect image
    cost_img.paste(house_img, (house_x, house_y), house_img)

    # Combine the two images
    out = Image.alpha_composite(building.convert('RGBA'), cost_img)

    return out

def add_text_to_building(building, name):
    name = name.split('/')[-1].split('.')[0]
    # find in the building with the same name as the image
    for b in buildings['buildings']:
        if b['name'] == name:
            # create a new image with the same size as the building
            txt = Image.new('RGBA', building.size, (255, 255, 255, 0))
            d = ImageDraw.Draw(txt)

            # draw the text in the image
            # Calculate the position to start the text at the top of the parallelogram

            fontsize = 50

            font = ImageFont.truetype("Helvetica", fontsize)

            text_width = d.textlength(b['name'], font=font)
            text_height = fontsize


            start_x = building.size[0] - size / 2 
            start_y = fontsize

            # Draw rounded rectangle
            rect_x0 = start_x - text_width / 2 - 10
            rect_y0 = start_y - text_height / 2 - 10
            rect_x1 = start_x + text_width / 2 + 10
            rect_y1 = start_y + text_height / 2 + 10

            d.rounded_rectangle(
                [rect_x0, rect_y0, rect_x1, rect_y1], 
                radius=10, 
                fill=(255, 255, 255, 200)
            )

            # Draw text
            d.text(
                xy=(start_x, start_y), 
                text=b['name'],
                fill=(0, 0, 0, 255),
                font=font,
                anchor='mm'
            )

            # combine the two images
            out = Image.alpha_composite(building.convert('RGBA'), txt)

            out = add_cost_to_building(out, b['cost'], b['points'], b['effect']['type'])

            out = add_effect_to_building(out, b['effect']['description'])

            return out
    
    print(f"Building '{name}' not found in the JSON file.")
    return building

def extract_parallelogram(image):
    """
    Extracts a parallelogram shape from the center of the image.
    """
    width, height = image.size
    # Define the coordinates of the parallelogram (change as needed)
    parallelogram_coords = par_position(width, height)

    # Create a mask for the parallelogram shape
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon(parallelogram_coords, fill=255)
    
    # Apply the mask to the image
    extracted = Image.new("RGBA", image.size)
    extracted.paste(image, mask=mask)

    # Crop to bounding box of the parallelogram and resize
    bbox = extracted.getbbox()
    extracted = extracted.crop(bbox)
    
    return extracted

def cut_images(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))]

    for image_file in image_files:
        img_path = os.path.join(input_folder, image_file)
        
        with Image.open(img_path) as img:
            # Extract the parallelogram
            extracted_img = extract_parallelogram(img)

            extracted_img = add_text_to_building(extracted_img, image_file) 

            # Save the extracted image to temporary file
            temp_img_path = os.path.join(output_folder, image_file)
            extracted_img.save(temp_img_path)
            print(f"Image saved as '{temp_img_path}'.")
        # input("Press Enter to continue...")

            
# Usage
input_folder = 'images'
output_folder = 'cut_images'
cut_images(input_folder, output_folder)
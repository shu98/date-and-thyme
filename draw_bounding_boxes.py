from PIL import Image, ImageDraw, ImageColor, ImageFont
import identify_text

def draw_boxes(filename, isSave=True):

    data = identify_text.identify(filename)
    im = Image.open(filename)
    draw = ImageDraw.Draw(im, 'RGBA')
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 14)

    count = 1
    for box in data:
        coords = box['bounding_box'].split(',') 
        draw.rectangle([int(coords[0]), int(coords[1]), int(coords[0])+int(coords[2]), int(coords[1])+int(coords[3])], (255, 255, 0, 100))
        draw.text((int(coords[0]), int(coords[1])), str(count), fill=(0, 0, 0), font=font)
        count += 1

    del draw
    if isSave:
        im.save('static/photo.jpg')

    return data


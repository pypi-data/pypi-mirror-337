from PIL import Image

def is_light(r: float, g: float, b: float) -> bool:
    '''
    Classifies a given RGB color code as 'Light' or 'Dark'

    Args:
        r (float): Red Value ranging between 0 and 255
        g (float): Green Value ranging between 0 and 255
        b (float): Blue Value ranging between 0 and 255

    Returns:
        bool: True if 'Light' else False
    '''
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance > 128

def change_colors(img_path: str, light_color: tuple, dark_color: tuple, new_img_path: str) -> None:
    '''
    Generates a new image in the specified folder with new color values. Ensure to pass only Dichromatic Images.
    Images containing more than 2 colors are considered Dichromatic only

    Args:
        img_path (str): Path to the original Image. Provide 'raw' string if it is a Windows path (r'path\\to\\the\\file')
        light_color (tuple): (r, g, b) of the new light color
        dark_color (tuple): (r, g, b) of the new dark color
        new_img_path (str): Name of the new image along with the path. Provide 'raw' string if it is a Windows path (r'path\\to\\the\\file')
    '''
    img = Image.open(img_path)
    pixels = list(img.getdata())
    new_img = Image.new(img.mode, img.size)
    new_pixels = [(light_color if is_light(r, g, b) else dark_color) for (r, g, b) in pixels]
    new_img.putdata(new_pixels)
    new_img.save(new_img_path)
    print(f'Image saved to: {new_img_path}')
    
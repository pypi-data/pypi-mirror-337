# Change colors in a Dichromatic Image

## Installation

`pip install navam`

## Example Usage

```python
from navam import change_colors

img_path = 'Path/to/Image.jpg'      # Provide 'raw' string incase of Windows Path
light_color = (0, 0, 0)             # Color value for the light pixels
dark_color = (0, 255, 0)            # Color value for the dark pixels
new_img_path = 'Path/to/Image.jpg'  # Don't forget the file extension

change_colors(img_path, light_color, dark_color, new_img_path)
```

### NOTE

If successfully processed, prints a message

`Image saved to: {new_img_path}`
from PIL import Image, ImageFilter
from urllib.request import urlopen
import io

with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
    img = Image.open(conn)
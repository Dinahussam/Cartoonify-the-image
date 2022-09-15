import cv2
import numpy as np
from numpy import asarray
from PIL import Image
import PySimpleGUI as Sg
import pathlib
import tempfile
from skimage import io

cartoon_image = 0


class MAIN:
    def __init__(self):
        self.layout = []
        Sg.theme('DarkTeal6')
        self.FIRST_COLOR = f'#E7E7E7 on #041B2D'
        self.SECOND_COLOR = '#041B2D on #9B9B9B '
        self.menu_def = [['&File', ['&Open (Ctrl+O)', '&Save', 'Exit']], ]

    def components(self):
        mid_col = Sg.Column([
            [Sg.Text("Import Image To Cartoonify It :", font='Helvetica 12 bold italic')],
            [Sg.Image(key="-IMAGE-", size=(400, 400), background_color='white')],
            [Sg.B('Cartoonify', button_color='#9B9B9B', pad=(150, 10), font='Helvetica 12 bold italic', border_width=8)]
        ], pad=(65, 0))

        self.layout = [
            [Sg.MenubarCustom(self.menu_def, font='Helvetica 12 bold italic')],
            [mid_col]
        ]
        return self.layout

    @staticmethod
    def open_file():
        filename = Sg.popup_get_file('Open', no_window=True)
        if filename:
            file = pathlib.Path(filename)
            return file

    file_types = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name

    @staticmethod
    def save_image(save_path):
        io.imsave(save_path, cartoon_image)

    @staticmethod
    def cartoon(image):
        global cartoon_image
        arr = asarray(image)
        # img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

        line_size, blur_value = 7, 5

        # Create Edge Mask
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        gray_blur = cv2.medianBlur(gray, blur_value)

        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size,
                                      blur_value)

        k = 16  # is the number of colors

        # Reduce the color palette :
        # Transform the image
        data = np.float32(arr).reshape((-1, 3))

        # Determine criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        # Implementing k-means
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)

        result = center[label.flatten()]
        result = result.reshape(arr.shape)

        # Reduce the noise :
        blurred = cv2.bilateralFilter(result, d=1, sigmaColor=200, sigmaSpace=200)

        # Combine edge mask with the quantization image:
        cartoon_image = cv2.bitwise_and(blurred, blurred, mask=edges)

        return Image.fromarray(cartoon_image)
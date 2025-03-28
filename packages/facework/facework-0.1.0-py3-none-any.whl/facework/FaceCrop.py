from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
import cv2
import numpy as np
from scipy.interpolate import splprep, splev
import os
from wand.color import Color
from wand.image import Image
import PIL
from PIL import ImageDraw
import psutil
import gc
from scipy.spatial import Delaunay
from scipy.ndimage import label
import tempfile
from pathlib import Path
import shutil
from matplotlib import pyplot as plt



class FaceCrop:
    def __init__(self):
        #index of the markers of the silhouette of the face
        self.silhouette_landmarks = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        #model to make the landmarks 
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        # #factor to wich scale the resolution for a cleaner crop
        self.scale_factor=35
        #working folders
        self.mask_folder=r'face_cropping_mask'
    

    def load_images(self, images_path=[], images=[]):
        self.clear_all()

        if not images:
            self.image_path = images_path
            self.image_array_original = [cv2.imread(path) for path in images_path]
        else:
            self.image_array_original = images
            self.image_path = [f"image_{i:03d}.jpg" for i in range(len(images))]  # Placeholder if needed for tracking

        # Precompute all: landmarks, normalized landmarks, and silhouettes
        self.image_landmark_list = []
        self.nomralized_landmarks = []
        self.image_silhouette_list = []

        for img in self.image_array_original:
            landmarks = self._compute_landmarks(img)
            normalized = self._normalize_facial_landmarks(landmarks, img.shape)
            silhouette = self._extract_silhouette(normalized)

            self.image_landmark_list.append(landmarks)
            self.nomralized_landmarks.append(normalized)
            self.image_silhouette_list.append(silhouette)

        
        

    
    #funciton to show a cv2 image
    def show(self, img, title=''):

        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.title(title)
        plt.axis('off')
        plt.show()


    def _compute_landmarks(self, image):
        #here we instantiaate the model and predict the land marks 
        with self.mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        landmark_list=results.multi_face_landmarks
        return landmark_list



    def _extract_silhouette(self, norm_land):

        contour = [norm_land[idx] for idx in self.silhouette_landmarks]
        
        return contour
        



    def _normalize_facial_landmarks(self, land_list, img_shape):
        image_height, image_width, _ = img_shape
        normalized_points = [
            (
                min(int(point.x * image_width), image_width - 1),
                min(int(point.y * image_height), image_height - 1)
                )
                for point in land_list[0].landmark
                ]

        return normalized_points

    def _make_splies(self, contour):
        points = np.array(contour)
        points_high_res = points * self.scale_factor

        # Fit a spline to the high-resolution contour points
        tck, u = splprep((points_high_res[:, 0], points_high_res[:, 1]), k=4)

        # Generate smooth points along the spline at high resolution
        new = np.linspace(0, 1, 500)  # Increase the number of points for a smoother curve
        smooth_points_high_res = np.array(splev(new, tck)).T

        #convert points back to original resolution
        smooth_points_normal_res=smooth_points_high_res/self.scale_factor
        return smooth_points_normal_res

    def _points_to_svg_path(self, x, y):
        """Convert points to SVG path data."""
        path = [f'M {x[0]} {y[0]}']  # start path
        path += [f'L {x_i} {y_i}' for x_i, y_i in zip(x[1:], y[1:])]
        path.append('Z')  # close path
        return ' '.join(path)

    def _write_svg(self, filename, path_data, width=800, height=600):
        """Write SVG file with the given path data."""
        svg_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
    <rect width="{width}" height="{height}" fill="black" />
    <path d="{path_data}" stroke="white" fill="white" stroke-width="1" />
</svg>"""
        with open(filename, 'w') as file:
            file.write(svg_template)
        return filename

    def _swap_file_ext(self, filepath: str, newExt: str) -> str:
        splitpath = filepath.split('.')
        splitpath.pop(len(splitpath)-1)
        return '.'.join(splitpath) + '.' + newExt

    def _convert_svg_to_png(self, filepath: str) -> str: # update the folder
        updatedFilepath = self._swap_file_ext(filepath=filepath, newExt="png")
        with Image(filename=filepath, background=Color("transparent"), resolution=144) as img:
            img.format = 'png'
            img.save(filename=updatedFilepath)
        return updatedFilepath

    #makes a mask for each face loaded
    def generate_mask(self, return_mask_path=None):
    # Create the splines and SVG path strings
        self.splines = [self._make_splies(sil) for sil in self.image_silhouette_list]
        self.svg_file = [self._points_to_svg_path(s[:, 0], s[:, 1]) for s in self.splines]
        self.masks = []

        # Use a provided path or create a temporary one
        use_temp = return_mask_path is None
        mask_folder = tempfile.mkdtemp() if use_temp else return_mask_path
        os.makedirs(mask_folder, exist_ok=True)

        try:
            for idx, img in enumerate(self.image_path):
                img_name = os.path.splitext(os.path.basename(img))[0] + '.svg'
                image_width = self.image_array_original[idx].shape[1]
                image_height = self.image_array_original[idx].shape[0]

                # Create the SVG and PNG paths
                pat = os.path.join(mask_folder, img_name)
                svg_path = self._write_svg(pat, self.svg_file[idx], width=image_width, height=image_height)
                png_path = self._convert_svg_to_png(svg_path)

                # Open and convert the image safely
                with PIL.Image.open(png_path) as img_obj:
                    self.masks.append(img_obj.convert("RGBA"))

        finally:
            if use_temp:
                shutil.rmtree(mask_folder, ignore_errors=True)

        return self.masks
        
    #
    def center_faces(self):
        self.centered_faces=[]
        for idx, img in enumerate(self.image_array_original):
            contour_np=np.array(self.image_silhouette_list[idx], dtype=np.int32)
            x, y, w,h =cv2.boundingRect(contour_np)
            perc_y=int((y/100)*60)
            img=img[y-perc_y:y+h+25,x-25:x+w+25]
            self.centered_faces.append(img)

        return self.centered_faces


        


    def crop_face(self, contour_img=None):
        #if no external cropping mask use generate mask and resize, otherwise skip mask generation and use external mask don't resize
        self.cropped_images=[]

        for idx, img in enumerate(self.image_array_original):
            

            #extract orgignal heigth and with for comparison
            image_height, image_width, _ = img.shape

            #make sure contour image and actual image are the same size  by resizing the contour if necessary
            if contour_img is not None: contour_img = contour_img.resize((image_width,image_height))
            else: contour_img=self.masks[idx].resize((image_width,image_height))


            #import original image form self
            image_pil = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            #convert contorur to grayscale
            contour_mask = contour_img.convert("L")

            np_contour_mask = np.array(contour_mask)
            eroded_mask=np_contour_mask
            #Apply erosion to the mask to make a little bit smaller for empty spaced generated by concave parts of the face
            kernel = np.ones((5,5), np.uint8)  # Define the erosion kernel&erode
            eroded_mask = cv2.erode(np_contour_mask, kernel, iterations=2)       
            alpha_mask = PIL.Image.fromarray(eroded_mask).convert("L")

            #apply the mask to the image effectively cropping it
            # Apply the alpha mask to the self image
            image_pil.putalpha(alpha_mask)

            

            self.cropped_images.append(image_pil)



  
        return self.cropped_images


    def clear_all(self):
        # Lista di attributi da cancellare
        attrs_to_clear = [
            'cropped_images',
            'centered_faces',
            'svg_paths',
            'png_paths',
            'splines',
            'svg_file',
            'image_path',
            'image_array_original',
            'image_landmark_list',
            'image_silhouette_list',
            'nomralized_landmarks',
            'masks',
            'png_paths'
        ]
 
        for attr in attrs_to_clear:
            try:
                setattr(self, attr, None)
            except:
                pass

        gc.collect()

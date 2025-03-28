from facework import FaceCrop
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
import ffmpeg
import tempfile
from subprocess import Popen, PIPE
from pathlib import Path


#img 1 and img 2 are cv2 image arrays

#attributes (if computed)

#aligned_faces
#dealunay_mesh




class FaceMorph():
    def __init__(self, img_1, img_2):
        #use the face crop class insternally
        self.FC=FaceCrop()
        #1st cut the faces out of the picture to focus on them
        self.FC.load_images(images=[img_1, img_2])
        focused_faces=self.FC.center_faces()
        #2 load the foces faces in the face crop class for further processing 
        self.FC.load_images(images=focused_faces)

    def _transformation_from_points(self, points1, points2):
        """
        Return an affine transformation [s * R | T] such that:

            sum ||s*R*p1,i + T - p2,i||^2

        is minimized.

        """
        # Solve the procrustes problem by subtracting centroids, scaling by the
        # standard deviation, and then using the SVD to calculate the rotation. See
        # the following for more details:
        #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

        points1 = points1.astype(np.float64)
        points2 = points2.astype(np.float64)

        c1 = np.mean(points1, axis=0)
        c2 = np.mean(points2, axis=0)
        points1 -= c1
        points2 -= c2

        s1 = np.std(points1)
        s2 = np.std(points2)
        points1 /= s1
        points2 /= s2
        U, S, Vt = np.linalg.svd(points1.T * points2)

        # The R we seek is in fact the transpose of the one given by U * Vt. This
        # is because the above formulation assumes the matrix goes on the right
        # (with row vectors) where as our solution requires the matrix to be on the
        # left (with column vectors).
        R = (U * Vt).T

        return np.vstack([np.hstack(((s2 / s1) * R, c2.T - (s2 / s1) * R * c1.T)),
                        np.matrix([0., 0., 1.])])

    def _warp_im(self, im, M, dshape):
        output_im = cv2.warpAffine(
            im, M, (dshape[1], dshape[0]),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
        )

        return output_im




    def _align_face(self):
        #load the two images and their landmarks
        ref_img=self.FC.image_array_original[0]
        ref_landmarks=np.matrix(self.FC.nomralized_landmarks[0])
        second_img=self.FC.image_array_original[1]
        second_landmarks=np.matrix(self.FC.nomralized_landmarks[1])

        #print(ref_landmarks.shape, second_landmarks.shape)
        #transformation from points
        T = self._transformation_from_points(ref_landmarks, second_landmarks)
        #affine transform matrix
        M = cv2.invertAffineTransform(T[:2])

        #warp second imgae
        warped_im2 = self._warp_im(second_img, M, ref_img.shape)

        self.aligned_faces=[ref_img,warped_im2]

        


    def _get_boundary_points(self, shape):
        h, w = shape[:2]
        boundary_pts = [
            (1,1), (w-1,1), (1, h-1), (w-1,h-1), 
            ((w-1)//2,1), (1,(h-1)//2), ((w-1)//2,h-1), ((w-1)//2,(h-1)//2)
        ]
        return np.array(boundary_pts)

    def _compute_mesh(self):
        #load images and their landmarks
        ref_img=self.FC.image_array_original[0]
        ref_landmarks=np.array(self.FC.nomralized_landmarks[0])
        second_img=self.FC.image_array_original[1]
        second_landmarks=np.array(self.FC.nomralized_landmarks[1])
        #add boudaires 
        ref_landmarks = np.append(ref_landmarks, self._get_boundary_points(ref_img.shape), axis=0)
        second_landmarks = np.append(second_landmarks, self._get_boundary_points(second_img.shape), axis=0)
        #calculate average (only one mesh only one list of points (50/50 the middle point of perfect fusion))
        avg_landmark=(ref_landmarks+second_landmarks)/2
        #make delaunay triangles (the 'mesh')
        self.dealunay_mesh=Delaunay(avg_landmark).simplices
        

    def _affine_transform(self, src, src_tri, dst_tri, size):
        M = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))
        # BORDER_REFLECT_101 is good for hiding seems
        if src.shape[0]<1 or src.shape[1]<1:
            return src
        dst = cv2.warpAffine(src, M, size ,borderMode=cv2.BORDER_REFLECT_101)
        return dst

    def _morph_triangle(self, im, im_out, src_tri, dst_tri):
        # For efficiency, we crop out a rectangular region containing the triangles 
        # to warp only that small part of the image.

        # Get bounding boxes around triangles
        sr = cv2.boundingRect(np.float32([src_tri]))
        dr = cv2.boundingRect(np.float32([dst_tri]))

        # Get new triangle coordinates reflecting their location in bounding box
        cropped_src_tri = [(src_tri[i][0] - sr[0], src_tri[i][1] - sr[1]) for i in range(3)]
        cropped_dst_tri = [(dst_tri[i][0] - dr[0], dst_tri[i][1] - dr[1]) for i in range(3)]

        # Create mask for destination triangle
        mask = np.zeros((dr[3], dr[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(cropped_dst_tri), (1.0, 1.0, 1.0), 16, 0)

        # Crop input image to corresponding bounding box
        cropped_im = im[sr[1]:sr[1] + sr[3], sr[0]:sr[0] + sr[2]]

        size = (dr[2], dr[3])


        warpImage1 = self._affine_transform(cropped_im, cropped_src_tri, cropped_dst_tri, size)



        # Copy triangular region of the cropped patch to the output image
        if (im_out[dr[1]:dr[1]+dr[3], dr[0]:dr[0]+dr[2]].shape==mask.shape) and (mask.shape==warpImage1.shape):
            im_out[dr[1]:dr[1]+dr[3], dr[0]:dr[0]+dr[2]] = \
                im_out[dr[1]:dr[1]+dr[3], dr[0]:dr[0]+dr[2]] * (1 - mask) + warpImage1 * mask

    def _morph_warp_im(self, im, src_landmarks, dst_landmarks, dst_triangulation):
        # im_out = np.zeros_like(im)
        im_out = im.copy()

        for i in range(len(dst_triangulation)):
            src_tri = src_landmarks[dst_triangulation[i]]
            dst_tri = dst_landmarks[dst_triangulation[i]]
            self._morph_triangle(im, im_out, src_tri, dst_tri)

        return im_out

    def _compute_white_black_ratio(self, mask):
        total_pixels = mask.size
        white_pixels = np.sum(mask == 255)  # Assuming white pixels are 255
        black_pixels = np.sum(mask == 0)    # Assuming black pixels are 0
        if black_pixels == 0:
            return float('inf')  # Avoid division by zero
        return white_pixels / black_pixels

    def _is_connected(self, mask):
        # Binary mask: 1 for white (255), 0 for black (0)
        binary_mask = (mask == 255).astype(int)
        # Label connected components
        labeled_array, num_features = label(binary_mask)
        # If there's exactly 1 connected component, the white area is connected
        return num_features == 1




    def make_frames(self, total_frames, out_name=None):
        #align the two faces 
        self._align_face()
        ##reload the aligned iamges in the Face cropper for 
        self.FC.load_images(images=self.aligned_faces)
        #make the morphign mesh mask
        self._compute_mesh()
        #load the images to compute the frames
        im1=self.FC.image_array_original[0]
        im2=self.FC.image_array_original[1]

        im1_landmarks=np.array(self.FC.nomralized_landmarks[0])
        im1_landmarks = np.append(im1_landmarks, self._get_boundary_points(im1.shape), axis=0)
        im2_landmarks=np.array(self.FC.nomralized_landmarks[1])
        im2_landmarks = np.append(im2_landmarks, self._get_boundary_points(im2.shape), axis=0)
        triangulation=self.dealunay_mesh.tolist()
        im1 = np.float32(im1)
        im2 = np.float32(im2)
        
        #generate frames
        uncropped_frames=[]
        for j in range(total_frames):
            print('generating frame: ', j+1, '/',total_frames )
            #-1 because max j is total_frames - 1 so that the first iteration is 0/tot-1 =0 and the last is tot -1 / tot -1 = 1
            alpha = j / (total_frames - 1)
            weighted_landmarks = (1.0 - alpha) * im1_landmarks + alpha * im2_landmarks
            #warping 
            warped_im1 = self._morph_warp_im(im1, im1_landmarks, weighted_landmarks, triangulation)
            warped_im2 = self._morph_warp_im(im2, im2_landmarks, weighted_landmarks, triangulation)
  
    

            # Convert warped images to Lab color space
            warped_im1_lab = cv2.cvtColor(np.uint8(warped_im1), cv2.COLOR_BGR2Lab)
            warped_im2_lab = cv2.cvtColor(np.uint8(warped_im2), cv2.COLOR_BGR2Lab)
        


            # Split the Lab channels
            L1, a1, b1 = cv2.split(warped_im1_lab)
            L2, a2, b2 = cv2.split(warped_im2_lab)

            # Alpha blending in Lab space
            L_blended = (1.0 - alpha) * L1 + alpha * L2
            a_blended = (1.0 - alpha) * a1 + alpha * a2
            b_blended = (1.0 - alpha) * b1 + alpha * b2

            # Merge the blended channels back to Lab image
            blended_lab = cv2.merge([L_blended, a_blended, b_blended])

            # Convert the blended Lab image back to BGR
            blended_bgr = cv2.cvtColor(np.uint8(blended_lab), cv2.COLOR_Lab2BGR)

            # Convert to PIL Image and save to the pipe stream
            res = PIL.Image.fromarray(cv2.cvtColor(np.uint8(blended_bgr), cv2.COLOR_BGR2RGB))
            

            uncropped_frames.append(np.array(res))

         
        
        #load the uncropped frames in the faceCropp class 
        self.FC.load_images(images=uncropped_frames)
       
        #generate a frame for each mask
        masks=[np.array(mask.convert('L')) for mask in self.FC.generate_mask()]

        #select most restrictve mask excluding the errors:

        #using z score to select the mask
        ratios = np.array([self._compute_white_black_ratio(mask) for mask in masks])
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)

        filtered_masks = []
        for mask, ratio in zip(masks, ratios):
            z_score = (ratio - mean_ratio) / std_ratio
            if abs(z_score) <= 1:
                filtered_masks.append(mask)

        #selectin only the mask where the white part is one single component 
        refiltered_masks = []
        for mask in filtered_masks:
            if self._is_connected(mask):
                refiltered_masks.append(mask)

        # Start with the first mask as the most restrictive
        most_restrictive_mask = refiltered_masks[0].copy()

        for mask in refiltered_masks:
            # Use bitwise AND to find overlapping white areas and ensure no black areas are infringed
            combined_mask = np.bitwise_and(most_restrictive_mask, mask)
            # The new most restrictive mask is the intersection of the previous and the current
            most_restrictive_mask = np.minimum(most_restrictive_mask, combined_mask)



        # Apply erosion to make the mask smaller
        #kernel = np.ones((3, 3), np.uint8)  # Define a 3x3 kernel for erosion
        #most_restrictive_mask = cv2.erode(most_restrictive_mask, kernel, iterations=2) 


        #the mask needs to be a PIL image
        final_mask= PIL.Image.fromarray(most_restrictive_mask)
        




        #now we cropp all the frames using the generated mask

        self.frames=self.FC.crop_face(contour_img=final_mask)

        self.frames=[np.array(frame) for frame in self.frames]

        if out_name is not None:
            for idx, frame in enumerate(self.frames):
                idx=str(idx) if idx >=10 else str(0)+str(idx)
                image_name=f'Image_{idx}.png'
                full_save_path=os.path.join(out_name, image_name)
                cv2.imwrite(str(full_save_path), frame)
     
        return self.frames

    def _make_even(self, n):
        if n%2==0:
            return n 
        else: return n + 1
    
    def _correct_frame_bg(self, frame):
        #make array
        cv2_frame=cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
        #check every pixel if is part of face or bg
        idx=cv2_frame[:,:,3]==0
        #if bg make white
        cv2_frame[idx,:3]=0  #0 for black 255 for white
        #drop alpha channel
        rgb_frame=np.array(PIL.Image.fromarray(cv2_frame).convert("RGB"))

        return rgb_frame

    def _stitch_frames_ffmpeg(self, frames, width, height, fps, output_path, codec):
        with tempfile.TemporaryDirectory() as tmpdirname:
            process = (
                ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{width}x{height}', r=fps)
                .output(output_path, pix_fmt='yuv420p', vcodec=codec, r=fps, crf=0, preset='veryslow', qscale=1)
                .overwrite_output()
                .global_args('-loglevel', 'error')  # Optional: suppress spam
                .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
            )

            try:
                for i, frame in enumerate(frames):
                    frame = cv2.resize(frame, (width, height))
                   
                    process.stdin.write(frame.astype(np.uint8).tobytes())

                process.stdin.close()
                process.wait()

            except BrokenPipeError:
                stderr = process.stderr.read().decode('utf-8')
                raise RuntimeError(f"FFmpeg crashed:\n{stderr}")

        

     



    def make_morph_video(self, output_path,with_reverse=False, fps=10, seconds=10, codec='mpeg4'):
        tot_frames=fps*seconds
        self.make_frames(tot_frames)

        clean_frames=[self._correct_frame_bg(frame) for frame in self.frames]

        
  
            # Make sure the directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Add file extension

        output_path_e = os.path.join(output_path, 'straigth.mp4')
        heigth, width = clean_frames[0].shape[:2]
        heigth=self._make_even(heigth)
        width=self._make_even(width)
        self._stitch_frames_ffmpeg(frames=clean_frames, width=width, height=heigth, fps=fps, output_path=output_path_e, codec=codec)
    
        if with_reverse:
            clean_frames_rev=clean_frames[::-1]
            output_path_r=os.path.join(output_path,'reversed.mp4')
            self._stitch_frames_ffmpeg(frames=clean_frames_rev, width=width, height=heigth, fps=fps, output_path=output_path_r, codec=codec)
           




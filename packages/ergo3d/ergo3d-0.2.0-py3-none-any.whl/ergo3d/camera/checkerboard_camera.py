# from Camera import *
from .Camera import *
import cv2
import pickle
import os
import random

def batch_load_from_checkerboard(load_dir, file_extension='_back.pkl', cameras=[]):
    """
    Choose extension from ['_back.pkl', '_right.pkl', '_left.pkl'], append to cameras list
    """
    for root, dirs, files in os.walk(load_dir):
        files = [f for f in files if not f[0] == '.']  # skip hidden files
        for file in files:
            if not file.endswith(file_extension):
                continue
            print(f"Loading {file}...", end=' ::::::: ')
            camera = Checkerboard_Camera()
            camera.load(os.path.join(root, file))
            cameras.append(camera)
    return cameras


class Checkerboard_Camera(Camera):
    def __init__(self):
        super().__init__()
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def copy(self):
        # make a new item and copy all attributes
        new_item = Checkerboard_Camera()
        new_item.__dict__ = self.__dict__.copy()
        return new_item

    def set_checkerboard_params(self, square_size, width=9, height=6):
        """
        Set the checkerboard parameters.
        :param square_size: size of the square in meters
        :param width: number of squares in the width
        :param height: number of squares in the height
        """
        self.square_size = square_size
        self.cb_width = width
        self.cb_height = height

    def set_camera_params(self, DEVICEID, VIEW_ROTATION=0):
        self.DEVICEID = DEVICEID
        self.VIEW_ROTATION = VIEW_ROTATION


    def intrinsic_calibrate(self, calibrate_img_dir, image_extension, verbose=True):
        """ Apply camera calibration operation for images in the given directory path. """
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
        objp = np.zeros((self.cb_height * self.cb_width, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.cb_width, 0:self.cb_height].T.reshape(-1, 2)
        objp = objp * self.square_size  # Create real world coords. Use your metric.

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.


        for root, dirs, files in os.walk(calibrate_img_dir):
            files = [f for f in files if not f[0] == '.']  # skip hidden files
            dirs[:] = [d for d in dirs if not d[0] == '.']  # skip hidden folders
            dirs.sort()  # Sort directories in-place --> important, will change walk sequence
            files.sort(key=str.lower)  # Sort files in-place
            for file in files:
                if not file.endswith(image_extension):
                    continue
                print(f"Loading {file}...", end=' ::::::: ')

                img = cv2.imread(os.path.join(root, file))
                assert img is not None, f"Image {file} empty read"
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv2.findChessboardCorners(gray, (self.cb_width, self.cb_height), None)
                # If found, add object points, image points (after refining them)
                if ret:
                    print(f"Found corners...")
                    objpoints.append(objp)
                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                    imgpoints.append(corners2)
                    # Draw and display the corners
                    img = cv2.drawChessboardCorners(img, (self.cb_width, self.cb_height), corners2, ret)
                else:
                    print(f"Did not find corners...")
        # flags |= CALIB_ZERO_TANGENT_DIST|CALIB_FIX_K1|CALIB_FIX_K2|CALIB_FIX_K3|CALIB_FIX_K4|CALIB_FIX_K5|CALIB_FIX_K6
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        h, w, channel = img.shape
        mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        print("Calibration is finished. RMS: ", ret)
        self.camera_matrix = mtx
        self.PRINCIPAL_POINT = np.array([mtx[0, 2], mtx[1, 2]])
        self.FOCAL_LENGTH = mtx[0, 0]
        self.PIXEL_ASPECT_RATIO = mtx[1, 1] / mtx[0, 0]
        self.dist_coeff = dist
        # self.rvecs = rvecs
        # self.tvecs = tvecs
        # self.roi = roi
        self.RESOLUTION = (w, h)
        self.RESOLUTION_U = w
        self.RESOLUTION_V = h
        self.SKEW = mtx[0, 1]
        self.RADIAL_DISTORTION1, self.RADIAL_DISTORTION2, self.RADIAL_DISTORTION3, self.TANGENTAL_DISTORTION1, self.TANGENTAL_DISTORTION2 \
            = dist.reshape(-1)
        return [ret, mtx, dist, rvecs, tvecs]

    def extrinsic_calibrate(self, verbose=True):
        success, rotation_vector, translation_vector = cv2.solvePnP(self.carpet_3D, self.carpet_2D, self.camera_matrix, self.dist_coeff, flags=0)
        print("Extrinsic calibration is finished. Success: ", success)
        self.translation_vector = translation_vector
        self.rotation_vector = rotation_vector
        self.rot3x3, _ = cv2.Rodrigues(rotation_vector)
        R_inv = self.rot3x3.T  # Transpose of rotation matrix is its inverse
        t_world = -R_inv @ translation_vector
        self.POSITION = t_world * 1000

    def set_carpet_3D(self, type='checkerboard', quadrant=1):
        """
        Simplified version:
        1) assume checkerboard is a carpet on the ground and orthogonal to gravity direction, z is up
        2) set detected checkerboard corners_2d[0] is world origin
        3) quadrant 1, 2, 3, 4, representing which quadrant the checkerboard is in regards to the +x, +y 1st quadrant in world coord
        """
        # set 3d carpet keypoints
        if type=='checkerboard':
            """ use the same checkerboard (with intrinsic calibration) to link camera to world coord"""
            # define world coord
            raise NotImplementedError

        elif type=='markers':
            """ use tape markers """
            raise NotImplementedError
    def set_checkerboard_carpet_3D(self, cam_pos='back'):
        """
        cam_position: 'back', 'right', 'left'
        Easier to customize this function each time you use
        """
        width = self.cb_width
        height = self.cb_height
        carpet_3D = np.zeros((height, width, 3))
        for h in range(height):
            for w in range(width):
                if cam_pos=='back':
                    carpet_3D[h, w, 0] = -w
                    carpet_3D[h, w, 1] = h
                elif cam_pos=='right':
                    carpet_3D[h, w, 0] = -h
                    carpet_3D[h, w, 1] = -w
                elif cam_pos == 'left':
                    carpet_3D[h, w, 0] = h
                    carpet_3D[h, w, 1] = w
                else:
                    raise ValueError(f"cam_pos {cam_pos} not recognized")
        carpet_3D = carpet_3D.reshape([-1, 3])
        carpet_3D = carpet_3D * self.square_size
        self.carpet_3D = carpet_3D
        return carpet_3D


    def find_carpet_2D(self, img_path, verbose=False):
        img = cv2.imread(img_path)
        assert img is not None, f"Image {file} empty read"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (self.cb_width, self.cb_height), None)

        self.got_carpet_2D = ret
        # If found, add object points, image points (after refining them)
        if ret:
            print(f"Found corners...")
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            # Draw and display the corners

            if verbose:
                img = cv2.drawChessboardCorners(img, (self.cb_width, self.cb_height), corners2, ret)
                # draw corner[0] as origin
                cv2.circle(img, tuple(corners2[0].astype(int).ravel()), 10, (255, 255, 255), -1)
                cv2.imshow('img', img)
                cv2.waitKey(0)

            h, w, channel = img.shape
            if not w == self.RESOLUTION_U:
                # stupid iphone's camera function in video mode gives bigger image than video frames
                ratio = self.RESOLUTION_U / w
                print(f"Image resolution does not match camera resolution: {img.shape} vs {self.RESOLUTION}, rescaling corners by {ratio}")
                assert self.RESOLUTION_V / h == ratio, f"Image landscape/portrait does not match camera resolution: {img.shape} vs {self.RESOLUTION}, not implemented yet"
                corners2 = corners2 * ratio
            self.carpet_2D = corners2
        else:
            print(f"Did not find corners...")
        return ret



    def save(self, save_dir):
        with open(save_dir, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, load_dir):
        with open(load_dir, 'rb') as f:
            self.__dict__ = pickle.load(f)

    def undistort(self, points_2d):
        raise NotImplementedError

    def distort(self, points_2d):
        raise NotImplementedError





if __name__ == '__main__':
    example_case = 1
    if example_case == 1:  # Camera intrinsic and extrinsic from checkerboard images
        checkerboard_dir = r'/Volumes/Z/Onform/synthetic_camera/calibrate/1x_intrinsic'
        # set up camera
        camera_base = Checkerboard_Camera()
        camera_base.set_checkerboard_params(square_size=0.0243, width=9, height=6)
        camera_base.intrinsic_calibrate(checkerboard_dir, '.png')

        extrinsic_dir = r'/Volumes/Z/Onform/synthetic_camera/calibrate/1x_extrinsic'
        image_extension = '.JPG'
        device_id = 0
        for root, dirs, files in os.walk(extrinsic_dir):
            files = [f for f in files if not f[0] == '.']  # skip hidden files
            for file in files:
                if not file.endswith(image_extension):
                    continue
                if "frames" in root:
                    continue
                print(f"Loading {file}...", end=' ::::::: ')
                camera_extrinsic = camera_base.copy()
                camera_extrinsic.find_carpet_2D(os.path.join(root, file), verbose=False)

                location_of_interest = ['back', 'right', 'left']
                device_id += 1
                for location in location_of_interest:
                    camera = camera_extrinsic.copy()
                    camera.set_camera_params(DEVICEID=f"{location}_{device_id}", VIEW_ROTATION=0)
                    camera.set_checkerboard_carpet_3D(cam_pos=location)

                    camera.extrinsic_calibrate()
                    camera.FOCAL_LENGTH = camera_base.FOCAL_LENGTH
                    if location == 'right':  # moving the cameras so the subject is in the 2D view range
                        camera.POSITION = camera.POSITION + np.array([[600, 0, 0]]).T
                    if location == 'left':
                        camera.POSITION = camera.POSITION + np.array([[1000, 1000, 0]]).T
                    camera.save(os.path.join(extrinsic_dir, f"{file}_{device_id}_{location}" + '.pkl'))

                    print(camera.POSITION)
                    print(camera.rot3x3)

                    # proj_point2D, jacobian = cv2.projectPoints(camera.carpet_3D, camera.rotation_vector, camera.POSITION,
                    #                                            camera.camera_matrix, camera.dist_coeff)
                    # # plot
                    # img = cv2.imread(os.path.join(root, file))
                    # img = cv2.drawChessboardCorners(img, (camera.cb_width, camera.cb_height), proj_point2D, True)
                    # cv2.imshow('img', img)
                    # cv2.waitKey(0)


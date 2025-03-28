import numpy as np
import matplotlib.pyplot as plt
import torch
from sklearn.utils import deprecated

class Point:
    def __init__(self, data, name=None):
        """
        data: torch tensor with shape (frame, 3), no exist list
        """

        self.name = name
        # If data is not a torch.Tensor, convert it to one
        if not isinstance(data, torch.Tensor):
            raise TypeError(f"data must be a torch.Tensor, not {type(data)}")
        else:
            if data.shape[1] == 3:
                if data.shape[0] == 3:
                    raise ValueError(f"May cause bug when processing 3 frames, in dim {data.shape}")
                self.x = data[:, 0]
                self.y = data[:, 1]
                self.z = data[:, 2]
                self.xyz = data.T
                self.frame_no = data.shape[0]
            elif data.shape[0] == 3:
                self.x = data[0]
                self.y = data[1]
                self.z = data[2]
                self.xyz = data
                self.frame_no = data.shape[1]
            else:
                raise ValueError(f"Expected data to have shape (frame, 3) or (3, frame), but got {data.shape}")
            self.device = data.device
            
            # print(self.name, data.shape, self.frame_no)


    @staticmethod
    def mid_point(p1, p2, precentage=0.5):
        '''
        return the midpoint of p1 and p2, if precentage is 0.5, return the mid point, if 0.25, return the point 1/4 way from p1 to p2
        '''
        try:
            xyz = p1.xyz * precentage + p2.xyz * (1 - precentage)
            p_out = Point(xyz)
            return p_out
        except:
            print('Error in "mid_point", Point not defined or exist not in python list')
            raise ValueError


    @staticmethod
    def distance(p1, p2=None):
        if p2 is None:
            return torch.norm(p1.xyz, dim=0)
        else:
            return torch.norm(p1.xyz - p2.xyz, dim=0)

    @staticmethod
    def vector(p1, p2, normalize=None):
        """
        Return the vector from p1 to p2.
        normalize:
            None -> return the raw vector,
            1 -> return the unit vector,
            other -> return the vector scaled to length 'normalize'
        """
        xyz = p2.xyz - p1.xyz
        if normalize is not None:
            dist = Point.distance(p1, p2)
            # To avoid division by zero, you might want to check if dist is nonzero
            if torch.all(dist == 0):
                raise ValueError("The two points are identical; cannot normalize a zero-length vector.")
            xyz = xyz / (dist + 1e-7) * normalize
        return Point(xyz)


    @staticmethod
    def orthogonal_vector(p1, p2, p3, normalize=None):
        """
        Return the vector orthogonal to the plane defined by p1, p2, p3.
        The direction is determined by the right-hand rule using the vectors p1->p2 and p1->p3.
        normalize:
            None -> return the raw vector,
            1 -> return the unit vector,
            other -> return the vector scaled to length 'normalize'
        Assumes that p1.xyz, p2.xyz, and p3.xyz are 3×n torch tensors.
        """
        # Get the unit vectors from p1 to p2 and from p1 to p3.
        v1 = Point.vector(p1, p2, normalize=1)
        v2 = Point.vector(p1, p3, normalize=1)

        # Transpose to shape (n, 3) so that each row is a 3D vector,
        # compute the cross product along the last dimension, then transpose back.
        xyz = torch.cross(v1.xyz.T, v2.xyz.T, dim=-1).T
        # xyz = torch.cross(v1.xyz, v2.xyz, dim=1)

        if normalize is not None:
            norm = torch.norm(xyz, dim=0)
            # To avoid division by zero, you could add a small epsilon if needed.
            xyz = xyz / (norm + 1e-7) * normalize
        return Point(xyz)

    @staticmethod
    def translate_point(p, vector, direction=1):
        """
        move p in the direction of vector with length of distance
        """
        if type(vector) is np.ndarray:
            raise ValueError(f"vector must be a torch.Tensor or Point, not {type(vector)}")
        elif isinstance(vector, torch.Tensor):
            vector = Point(vector)
        xyz = p.xyz + direction * vector.xyz
        return Point(xyz)

    @staticmethod
    def create_const_vector(x, y, z, frame=100, examplePt=None):
        """
        Create a constant vector with components (x, y, z).
        x, y, z are floats.
        If examplePt is provided, its frame_no is used and its device is adopted.
        """
        # Use the device from examplePt if provided, otherwise default to 'cpu'
        device = examplePt.device if examplePt is not None else 'cuda'
        if examplePt:
            frame = examplePt.frame_no
        # Create a tensor of shape (3, frame) with constant values for x, y, z
        xyz = torch.ones([frame, 3], device=device) * torch.tensor([x, y, z], device=device)
        return Point(xyz)

    @staticmethod
    def angle(v1, v2):
        """
        Return the angle between v1 and v2.
        v1 and v2 are tensors with shape (3, n).
        """
        dot = torch.sum(v1 * v2, dim=0)
        norm_v1 = torch.norm(v1, dim=0)
        norm_v2 = torch.norm(v2, dim=0)

        eps = 1e-7
        norm_v1 = torch.clamp(norm_v1, min=eps)
        norm_v2 = torch.clamp(norm_v2, min=eps)

        cos_angle = torch.clamp(dot / (norm_v1 * norm_v2), -1.0 + eps, 1.0 - eps)
        angle = torch.acos(cos_angle)

        # # angles here should be [0, pi], otherwise, convert
        # angle = torch.min(angle, np.pi - angle)
        return angle

    @staticmethod
    def angle_w_direction(target_vector, main_axis_vector, secondary_axis_vector):
        """
        Return the signed angle between target_vector and main_axis_vector using the right-hand rule.
        The secondary_axis_vector is used to determine the sign of the angle.
        """
        angle_abs = Point.angle(target_vector, main_axis_vector)
        angle_sign = Point.angle(target_vector, secondary_axis_vector)
        angle = torch.where(angle_sign > (np.pi / 2), -angle_abs, angle_abs)
        return angle

    @staticmethod
    def plot_points(point_list, ax=None, fig=None, frame=0):
        """
        plot a list of points
        """
        if ax is None or fig is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        x = []
        y = []
        z = []
        # make legend with point sequence
        for i, p in enumerate(point_list):
            ax.scatter(p.x[frame], p.y[frame], p.z[frame], label=str(i))
        # make sure the axis are equal
        ax.set_aspect('equal')
        # labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        # legend
        ax.legend()
        plt.show()
        return ax, fig

    @staticmethod
    def batch_export_to_nparray(point_list):
        '''
        point_list is a list of Point objects
        return a np array with shape (frame, keypoints, 3)
        '''
        xyz = np.array([p.xyz.T for p in point_list])
        xyz = np.swapaxes(xyz, 0, 1)
        return xyz

    @staticmethod
    @deprecated(extra="Not covered by test yet, dim might be wrong")
    def batch_export_to_tensor(point_list):
        """
        point_list is a list of Point objects.
        Return a torch tensor with shape (frame, keypoints, 3).
        Assumes that for each point, p.xyz is a torch tensor of shape (3, frame).
        """
        # Transpose each point's tensor to get shape (frame, 3)
        list_xyz = [p.xyz.T for p in point_list]
        # Stack along a new dimension for keypoints: result shape will be (frame, keypoints, 3)
        tensor_xyz = torch.stack(list_xyz, dim=1)
        return tensor_xyz

from .Point import Point
import torch

class Plane:
    def __init__(self, pt1=None, pt2=None, pt3=None):
        self.is_empty = True
        if pt1 is not None and pt2 is not None and pt3 is not None:
            self.set_by_pts(pt1, pt2, pt3)

    def set_by_pts(self, pt1, pt2, pt3):
        """
        Define the plane by three points (using vectors from pt1->pt2 and pt1->pt3).
        The orthogonal vector is computed and normalized (using right-hand rule).
        """
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.is_empty = False
        self.normal_vector = Point.orthogonal_vector(pt1, pt2, pt3, normalize=1)
        self.normal_vector_end = Point.translate_point(pt1, self.normal_vector, direction=1)

    def set_by_vector(self, pt1, vector, direction=1):
        """
        Define the plane by a point and a given vector.
        'vector' is expected to be a virtual Point.
        """
        self.pt1 = pt1
        self.pt2 = None
        self.pt3 = None
        self.is_empty = False
        vector_xyz = vector.xyz
        # Normalize vector_xyz using torch.norm (normalization performed along dim=0)
        normal_vector_xyz = vector_xyz / (torch.norm(vector_xyz, dim=0) + 1e-7) * direction
        # Create a new Point instance using the normalized tensor
        self.normal_vector = Point(normal_vector_xyz)
        self.normal_vector_end = Point.translate_point(pt1, vector, direction=direction)

    def project_vector(self, vector, optimize=True):
        """
        Project a vector onto the plane.
        'vector' is expected to be a torch tensor of shape (3, n) representing n vectors (each column is a vector).
        """
        plane_normal = self.normal_vector.xyz
        # Normalize along the first dimension (the 3 components)
        plane_normal = plane_normal / (torch.norm(plane_normal, dim=0) + 1e-7)

        if optimize:
            # Compute the dot product for each column (each vector) along dim=0.
            # This yields a tensor of shape (n,)
            diagonal_elements = torch.sum(vector * plane_normal, dim=0)
            # Subtract the normal component from each vector. Broadcasting:
            #   diagonal_elements[None, :] has shape (1, n), plane_normal is (3, n)
            projection = vector - diagonal_elements[None, :] * plane_normal
        else:
            # Alternative: use matrix multiplication to compute all dot products.
            # vector.T is (n, 3) and plane_normal is (3, n), so the result is (n, n)
            dot_matrix = torch.matmul(vector.T, plane_normal)
            # Extract the diagonal, which contains the dot product for each corresponding column.
            diagonal_elements = torch.diag(dot_matrix)
            projection = vector - diagonal_elements[None, :] * plane_normal
        return projection

    def project_point(self, point):
        """
        Project a given Point onto the plane.
        """
        vector = point.xyz - self.pt1.xyz
        projection = self.project_vector(vector)
        return Point.translate_point(self.pt1, projection)

    def above_or_below(self, point):
        """
        Determine whether a point is above or below the plane.
        Returns a tensor of 1's (above) or -1's (below) computed per row.
        """
        vector = point.xyz - self.pt1.xyz
        normal_vector = self.normal_vector.xyz
        # Sum along the vector dimension (dim=1) to get a scalar per row
        return torch.sign(torch.sum(vector * normal_vector, dim=0))

    @staticmethod
    def angle_w_direction(plane1, plane2):
        """
        Return the angle between two planes (plane1 and plane2) in the range [-pi, pi].
        The angle is determined by comparing plane1's normal with plane2's normal and its endpoint.
        """
        angle = Point.angle(plane1.normal_vector, plane2.normal_vector)
        angle_sign = Point.angle(plane1.normal_vector, plane2.normal_vector_end)
        angle = torch.where(angle_sign > (np.pi / 2), -angle, angle)
        return angle


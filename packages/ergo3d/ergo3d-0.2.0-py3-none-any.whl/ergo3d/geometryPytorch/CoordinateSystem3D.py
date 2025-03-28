from .Point import Point
from .Plane import Plane


class CoordinateSystem3D:
    def __init__(self):
        self.is_empty = True

    def set_by_plane(self, plane, origin_pt, axis_pt, sequence='xyz', axis_positive=True):
        """
        Set up a coordinate system using a given plane and two points.

        Parameters:
          - plane: a Plane object defining the plane of the coordinate system.
          - origin_pt: the Point object representing the origin.
          - axis_pt: a Point object used to define the in-plane axis.
          - sequence: a three-character string (e.g. 'xyz') that defines the assignment of axes.
                      The first character corresponds to the in-plane axis (from origin_pt to axis_pt,
                      with its sign adjusted by axis_positive), the second to the orthogonal (plane normal)
                      axis, and the third is computed as the remaining (orthogonal to the first two) axis.
          - axis_positive: if True, the in-plane axis is directed from origin_pt to axis_pt;
                           if False, its direction is reversed.
        """
        self.plane = plane
        self.is_empty = False
        self.origin = origin_pt
        axis_vec = Point.vector(origin_pt, axis_pt, normalize=1)
        if axis_positive:
            inplane_end = Point.translate_point(origin_pt, axis_vec, direction=1)
        else:
            inplane_end = Point.translate_point(origin_pt, axis_vec, direction=-1)
        orthogonal_end = Point.translate_point(origin_pt, plane.normal_vector)

        # Assign the first two axes according to the provided sequence.
        if sequence[0] == 'x':
            self.x_axis_end = inplane_end
        elif sequence[0] == 'y':
            self.y_axis_end = inplane_end
        elif sequence[0] == 'z':
            self.z_axis_end = inplane_end
        else:
            raise ValueError(f'sequence must be one of xyz, xzy, yxz, yzx, zxy, zyx, but {sequence} is given')

        if sequence[1] == 'x':
            self.x_axis_end = orthogonal_end
        elif sequence[1] == 'y':
            self.y_axis_end = orthogonal_end
        elif sequence[1] == 'z':
            self.z_axis_end = orthogonal_end
        else:
            raise ValueError(f'sequence must be one of xyz, xzy, yxz, yzx, zxy, zyx, but {sequence} is given')

        # Compute the third axis (the one not yet defined) using the right-hand rule.
        self.set_third_axis(sequence)
        # Define auxiliary planes based on the axis endpoints.
        self.set_plane_from_axis_end()
        # Optionally, you could plot for debugging:
        # Point.plot_points([self.origin, self.x_axis_end, self.y_axis_end, self.z_axis_end], frame=1000)

    def set_third_axis(self, sequence='xyz'):
        """
        Compute the third axis as the vector orthogonal to the other two axes.
        """
        if sequence[-1] == 'x':
            self.x_axis_end = Point.translate_point(self.origin, Point.orthogonal_vector(self.origin, self.y_axis_end, self.z_axis_end, normalize=1))
        elif sequence[-1] == 'y':
            self.y_axis_end = Point.translate_point(self.origin, Point.orthogonal_vector(self.origin, self.z_axis_end, self.x_axis_end, normalize=1))
        elif sequence[-1] == 'z':
            self.z_axis_end = Point.translate_point(self.origin, Point.orthogonal_vector(self.origin, self.x_axis_end, self.y_axis_end, normalize=1))
        else:
            raise ValueError(f'sequence must be xyz, xzy, yxz, yzx, zxy, zyx, but got {sequence}')

    def set_plane_from_axis_end(self):
        """
        Create three auxiliary planes from the origin and each pair of axis endpoints.
        These can be used for further projections or angle computations.
        """
        self.xy_plane = Plane(self.origin, self.x_axis_end, self.y_axis_end)
        self.zx_plane = Plane(self.origin, self.z_axis_end, self.x_axis_end)
        self.yz_plane = Plane(self.origin, self.y_axis_end, self.z_axis_end)

    def projection_angles(self, target_vector, threshold=1):
        """
        Compute the projection angles of a target vector onto the three coordinate planes.

        Parameters:
          - target_vector: a Point object whose .xyz is a torch tensor (frame, 3)

        Returns:
          A tuple (xy_angle, xz_angle, yz_angle) where each angle is computed (using the right-hand rule)
          between the projected target vector and the corresponding primary axis of the plane.
        """
        # Get the target vector as a torch tensor.
        vector = target_vector.xyz
        # Compute the axis vectors (from the origin to the axis endpoints).
        x_vector = Point.vector(self.origin, self.x_axis_end).xyz
        y_vector = Point.vector(self.origin, self.y_axis_end).xyz
        z_vector = Point.vector(self.origin, self.z_axis_end).xyz

        # Project the target vector onto each coordinate plane.
        xy_projection = self.xy_plane.project_vector(vector)
        xz_projection = self.zx_plane.project_vector(vector)
        yz_projection = self.yz_plane.project_vector(vector)

        # Compute the signed angles using the right-hand rule.
        xy_angle = Point.angle_w_direction(xy_projection, x_vector, y_vector)
        xz_angle = Point.angle_w_direction(xz_projection, x_vector, z_vector)
        yz_angle = Point.angle_w_direction(yz_projection, y_vector, z_vector)
        return xy_angle, xz_angle, yz_angle
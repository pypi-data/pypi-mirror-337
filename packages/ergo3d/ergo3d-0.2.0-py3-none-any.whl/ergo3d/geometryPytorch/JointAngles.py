import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
from scipy.stats import shapiro, skew, kurtosis, norm, ks_2samp
import torch
from sklearn.utils import deprecated

from .Point import Point
from .Plane import Plane


class JointAngles:
    def __init__(self):
        self.is_empty = True
        self.zero_frame_or_angle = [None, None, None]
        self.zero_by_frame_not_angle = False
        self.ergo_name = {'flexion': 'flexion', 'abduction': 'abduction', 'rotation': 'rotation'}

    def set_zero(self, frame_or_angle, by_frame=False):
        '''
        set to None if you don't want to zero the angles
        if by_frame is True, zero_frame_or_angle is a list of 3 frame numbers
        if by_frame is False, zero_frame_or_angle is a list of 3 angles in degrees
        '''
        if frame_or_angle is None:
            output = [None, None, None]
        elif isinstance(frame_or_angle, list):
            if len(frame_or_angle) != 3:
                raise ValueError('zero frame must be a list of length 3 or a single int')
            output = [np.radians(x) for x in frame_or_angle] if by_frame is False else frame_or_angle
        elif isinstance(frame_or_angle, int):
            # Convert to radian if needed.
            frame_or_angle = np.radians(frame_or_angle) if by_frame is False else frame_or_angle
            output = [frame_or_angle, frame_or_angle, frame_or_angle]
        self.zero_frame_or_angle = output
        self.zero_by_frame_not_angle = by_frame

    def get_flex_abd(self, coordinate_system, target_vector, plane_seq=['xy', 'xz'], flip_sign=[1, 1]):
        """
        Get flexion and abduction angles of a vector in a coordinate system.
        plane_seq: a list of two strings (e.g. ['xy', 'xz']). The first corresponds to flexion,
                   the second to abduction. Use None for an unused angle.
        """
        if len(plane_seq) != 2:
            raise ValueError('plane_seq must be a list of length 2, with flexion plane first and abduction plane second, fill None if not needed')
        xy_angle, xz_angle, yz_angle = coordinate_system.projection_angles(target_vector)
        output_angles = []
        for plane_id, plane_name in enumerate(plane_seq):
            if plane_name is not None:
                if plane_name == 'xy':
                    output_angle = xy_angle
                elif plane_name in ['xz', 'zx']:
                    output_angle = xz_angle
                elif plane_name == 'yz':
                    output_angle = yz_angle
                else:
                    raise ValueError('plane_name must be one of "xy", "xz", "zx", "yz", or None')
                # output_angle = np.abs(output_angle)
                if self.zero_frame_or_angle[plane_id] is not None:
                    if self.zero_by_frame_not_angle:
                        zero_frame_id = self.zero_frame_or_angle[plane_id]
                        zero_angle = output_angle[zero_frame_id]
                    else:  # zero by angle directly
                        zero_angle = self.zero_frame_or_angle[plane_id]
                    output_angle = output_angle - zero_angle
                    # Wrap angles to the range [-pi, pi] using torch.where.
                    output_angle = torch.where(output_angle > np.pi, output_angle - 2 * np.pi, output_angle)
                    output_angle = torch.where(output_angle < -np.pi, output_angle + 2 * np.pi, output_angle)
                output_angles.append(output_angle)
            else:
                output_angles.append(None)

        self.flexion = output_angles[0] * flip_sign[0]
        # self.flexion_info = {'plane': plane_seq[0], 'zero_angle': zero_angles[0], 'zero_frame': self.zero_frame[0], 'flip_sign': flip_sign[0]}
        self.abduction = output_angles[1] * flip_sign[1]
        # self.abduction_info = {'plane': plane_seq[1], 'zero_angle': zero_angles[1], 'zero_frame': self.zero_frame[1], 'flip_sign': flip_sign[1]}
        self.is_empty = False
        return output_angles

    def get_rot(self, pt1a, pt1b, pt2a, pt2b, flip_sign=1):
        """
        Get the rotation angle between two vectors defined by two pairs of points.
        flip_sign: 1 or -1, used if the rotation is in the opposite direction.
        """
        pt1mid = Point.mid_point(pt1a, pt1b)
        pt2mid = Point.mid_point(pt2a, pt2b)
        plane1 = Plane(pt1a, pt1b, pt2mid)
        plane2 = Plane(pt2a, pt2b, pt1mid)
        rotation_angle = Point.angle(plane1.normal_vector.xyz, plane2.normal_vector.xyz)

        rotation_sign = plane2.above_or_below(pt1a)
        # print(f'rotation_sign: {rotation_sign}')
        # print(f'flip_sign: {flip_sign}')
        # print(f'rotation_angle: {rotation_angle.shape}')
        rotation_angle = rotation_angle * rotation_sign * flip_sign

        if self.zero_frame_or_angle[2] is not None:
            if self.zero_by_frame_not_angle:
                rotation_zero = rotation_angle[int(self.zero_frame_or_angle[2])]
            else:
                rotation_zero = self.zero_frame_or_angle[2]
            rotation_angle = rotation_angle - rotation_zero
        else:
            rotation_zero = None

        # Wrap angles to the range [-pi, pi]
        rotation_angle = torch.where(rotation_angle > np.pi, rotation_angle - 2 * np.pi, rotation_angle)
        rotation_angle = torch.where(rotation_angle < -np.pi, rotation_angle + 2 * np.pi, rotation_angle)

        self.rotation = rotation_angle
        self.rotation_info = {'plane': None, 'zero_angle': rotation_zero, 'zero_frame': self.zero_frame_or_angle[2]}
        self.is_empty = False
        return self.rotation

    def zero_by_idx(self, idx):
        """
        idx is 0, 1, 2, corresponding to flexion, abduction, rotation
        usage:
        RKNEE_angles.flexion = RKNEE_angles.zero_by_idx(0)
        """
        angle = self.flexion if idx == 0 else self.abduction if idx == 1 else self.rotation
        this_zero_frame = self.zero_frame_or_angle[idx]
        if this_zero_frame is not None:
            if self.zero_by_frame_not_angle:
                zero_angle = angle[this_zero_frame]
            else:
                zero_angle = this_zero_frame
            output_angle = angle - zero_angle
            output_angle = torch.where(output_angle > np.pi, output_angle - 2 * np.pi, output_angle)
            output_angle = torch.where(output_angle < -np.pi, output_angle + 2 * np.pi, output_angle)
        else:
            output_angle = angle

        return output_angle

    def output_np(self):
        output_list = []
        if self.flexion is not None:
            output_list.append(self.flexion)
        if self.abduction is not None:
            output_list.append(self.abduction)
        if self.rotation is not None:
            output_list.append(self.rotation)
        return np.array(output_list)

    @deprecated(extra="Not covered by test yet, dim might be wrong")
    def output_tensor(self, device=None):
        output_list = []
        # Process flexion
        if self.flexion is not None:
            if not isinstance(self.flexion, torch.Tensor):
                angle_tensor = torch.tensor(self.flexion, device=device) if device is not None else torch.tensor(self.flexion)
            else:
                angle_tensor = self.flexion if device is None else self.flexion.to(device)
            output_list.append(angle_tensor)
        # Process abduction
        if self.abduction is not None:
            if not isinstance(self.abduction, torch.Tensor):
                angle_tensor = torch.tensor(self.abduction, device=device) if device is not None else torch.tensor(self.abduction)
            else:
                angle_tensor = self.abduction if device is None else self.abduction.to(device)
            output_list.append(angle_tensor)
        # Process rotation
        if self.rotation is not None:
            if not isinstance(self.rotation, torch.Tensor):
                angle_tensor = torch.tensor(self.rotation, device=device) if device is not None else torch.tensor(self.rotation)
            else:
                angle_tensor = self.rotation if device is None else self.rotation.to(device)
            output_list.append(angle_tensor)
        return torch.stack(output_list, dim=0)

    def plot_angles(self, joint_name='', alpha=1, linewidth=1, linestyle='-', label=None, frame_range=None, colors=['r', 'g', 'b'], overlay=None):
        """
        plot angles
        overlay: [fig, ax] to overlay on an existing plot
        """
        if self.is_empty:
            raise ValueError('JointAngles is empty, please set angles first')
        if frame_range is None:
            if self.flexion is not None:
                frame_range = [0, len(self.flexion)]
            elif self.abduction is not None:
                frame_range = [0, len(self.abduction)]
            elif self.rotation is not None:
                frame_range = [0, len(self.rotation)]
            else:
                raise ValueError('all three angles are None, cannot plot')
        if overlay is None:
            fig, ax = plt.subplots(3, 1, sharex=True)
        else:
            fig, ax = overlay
        angle_names = ['Flexion', 'H-Abduction', 'Rotation']
        # Convert angles to NumPy arrays if they are torch tensors.
        angles_to_plot = []
        for angle in [self.flexion, self.abduction, self.rotation]:
            if angle is not None and isinstance(angle, torch.Tensor):
                angles_to_plot.append(angle.detach().cpu().numpy())
            else:
                angles_to_plot.append(angle)
        for angle_id, angle in enumerate(angles_to_plot):
            ax[angle_id].axhline(0, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
            ax[angle_id].axhline(90, color='k', linestyle='dotted', alpha=0.5, linewidth=0.25)
            ax[angle_id].axhline(180, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
            ax[angle_id].axhline(-90, color='k', linestyle='dotted', alpha=0.5, linewidth=0.25)
            ax[angle_id].axhline(-180, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
            ax[angle_id].yaxis.set_ticks(np.arange(-180, 181, 90))
            ax[angle_id].set_ylabel(f'{angle_names[angle_id]}')
            ax[angle_id].set_xlim(frame_range[0], frame_range[1])  # set xlim
            ax[angle_id].margins(x=0)
            if angle is not None:
                ax[angle_id].plot(angle[0:frame_range[1]] / np.pi * 180, color=colors[angle_id], alpha=alpha, linewidth=linewidth, linestyle=linestyle, label=label)
            else:
                # plot diagonal line crossing through the chart
                ax[angle_id].plot([frame_range[0], frame_range[1]], [-180, 180], color='gray', linewidth=1)

        ax[0].set_title(f'{joint_name} (deg)')
        # plt.show()
        return fig, ax

    def plot_angles_by_frame(self, render_dir, joint_name='', alpha=1, linewidth=1, linestyle='-', label=None, frame_range=None, angle_names=['Flexion', 'H-Abduction', 'Rotation']):
        if self.is_empty:
            raise ValueError('JointAngles is empty, please set angles first')
        if frame_range is None:
            if self.flexion is not None:
                frame_range = [0, len(self.flexion)]
            elif self.abduction is not None:
                frame_range = [0, len(self.abduction)]
            elif self.rotation is not None:
                frame_range = [0, len(self.rotation)]
            else:
                raise ValueError('all three angles are None, cannot plot')
        print(f'Saving {joint_name} angle frames to {render_dir}')
        # Convert angles to NumPy if needed.
        flexion_np = self.flexion.detach().cpu().numpy() if self.flexion is not None and isinstance(self.flexion, torch.Tensor) else self.flexion
        abduction_np = self.abduction.detach().cpu().numpy() if self.abduction is not None and isinstance(self.abduction, torch.Tensor) else self.abduction
        rotation_np = self.rotation.detach().cpu().numpy() if self.rotation is not None and isinstance(self.rotation, torch.Tensor) else self.rotation

        for frame_id in range(frame_range[0], frame_range[1]):
            fig, ax = plt.subplots(3, 1, sharex=True)

            colors = ['r', 'g', 'b']
            for angle_id, angle in enumerate([flexion_np, abduction_np, rotation_np]):
                print(f'frame {frame_id}/{frame_range[1]}', end='\r')
                # horizontal line at zero, pi, and -pi
                ax[angle_id].axhline(0, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
                ax[angle_id].axhline(90, color='k', linestyle='dotted', alpha=0.5, linewidth=0.25)
                ax[angle_id].axhline(180, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
                ax[angle_id].axhline(-90, color='k', linestyle='dotted', alpha=0.5, linewidth=0.25)
                ax[angle_id].axhline(-180, color='k', linestyle='--', alpha=0.5, linewidth=0.25)
                ax[angle_id].yaxis.set_ticks(np.arange(-180, 181, 90))
                ax[angle_id].set_xlim(frame_range[0], frame_range[1])  # set xlim
                ax[angle_id].axvline(frame_id, color='k', linestyle='--', alpha=0.5, linewidth=0.25)  # vertical line at current frame
                # a dot with value at current frame
                ax[angle_id].set_ylabel(f'{angle_names[angle_id]}')
                ax[angle_id].margins(x=0)
                if angle is not None:
                    ax[angle_id].plot(angle[0:frame_id + 1] / np.pi * 180, color=colors[angle_id], alpha=alpha, linewidth=linewidth, linestyle=linestyle, label=label)
                    ax[angle_id].plot(frame_id, angle[frame_id] / np.pi * 180, color=colors[angle_id], marker='o', markersize=5)  # a dot with value at current frame
                    ax[angle_id].text(frame_id, angle[frame_id] / np.pi * 180, f'{angle[frame_id] / np.pi * 180:.1f}', fontsize=12, horizontalalignment='left',
                                      verticalalignment='bottom')  # add text of current angle value
                else:
                    ax[angle_id].plot([frame_range[0], frame_range[1]], [-180, 180], color='gray', linewidth=1)  # plot diagonal line crossing through the chart

            ax[0].set_title(f'{joint_name} (deg)')

            ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))  # set x ticks to integer only
            if not os.path.exists(render_dir):
                os.makedirs(render_dir)
            plt.savefig(os.path.join(render_dir, f'{joint_name}_{frame_id:06d}.png'))
            plt.close()


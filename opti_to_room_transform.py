from quaternion import quaternion
import numpy as np

x = -0.71020299
y = -1.89157128
z = -0.56325108

a = -0.49127844
b = -0.25602677
c = 0.76759422
d = 0.32232767  # scalar part of the quaternion, "qw"

# room origin in camera coordinates

ro_cc = [x, y, x]

# room frame rotation in camera coordinate system

rf_rot = [a, b, c, d]

# numpy-quaternion standard is scalar, w, first
q = quaternion(d, a, b, c)

q_inv = q.inverse()

# rotation matrix: room coords to camera coords
r11 = 1-2*(c**2)-2*(d**2)
r12 = 2*(b*c)-2*(d*a)
r13 = 2*(b*d)+2*(c*a)
r21 = 2*(b*c)+2*(d*a)
r22 = 1-2*(b**2)-2*(d**2)
r23 = 2*(c*d)-2*(b*a)
r31 = 2*(b*d)-2*(c*a)
r32 = 2*(c*d) + 2*(b*a)
r33 = 1 - 2*(b**2) - 2*(c**2)


R_rc = np.array([[r11, r12, r13],
                [r21, r22, r23],
                [r31, r32, r33]])


# Transformation matrix: room coords to camera coords

T_rc = np.array([[r11, r12, r13, x],
                 [r21, r22, r23, y],
                 [r31, r32, r33, z],
                 [0, 0, 0, 1]])


# Inverse transform: camera coordinates to room coordinates

T_cr = np.linalg.inv(T_rc)

print(T_cr)

print(q_inv)
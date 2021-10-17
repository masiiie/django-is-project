import math as m

PI = 2*m.acos(0.0)
EPS = 0.000000001

def tovec(p1_x, p1_y, p2_x, p2_y):
#    print((p2_x - p1_x, p2_y - p1_y))
    return (p2_x - p1_x, p2_y - p1_y)

def dot(vec1_x, vec1_y, vec2_x, vec2_y):
    return vec1_x * vec2_x + vec1_y * vec2_y

def norm_sq(v_x, v_y):
    return v_x * v_x + v_y*v_y

# return angle aob in rad
def angle(a_x, a_y, o_x, o_y, b_x, b_y):
    oa = tovec(o_x, o_y, a_x, a_y)
    ob = tovec(o_x, o_y, b_x, b_y)
    return m.acos(dot(oa[0], oa[1], ob[0], ob[1]) / m.sqrt(norm_sq(oa[0], oa[1]) * norm_sq(ob[0], ob[1])))

def cross(a_x, a_y, b_x, b_y):
    return a_x * b_y - a_y * b_x

# return true if point c is on the left side of line ab
def ccw(a_x, a_y, b_x, b_y, c_x, c_y):
    return cross(tovec(a_x, a_y, b_x, b_y)[0], tovec(a_x, a_y, b_x, b_y)[1], tovec(b_x, b_y, c_x, c_y)[0], tovec(b_x, b_y, c_x, c_y)[1]) > 0

# return true if point pt is in either convex/concave polygon P
def inpolygon(pt_x, pt_y, P):
    suma = 0
    if len(P) == 0:
        return False
    for i in range(len(P)-1):
        if ccw(pt_x, pt_y, P[i][0], P[i][1], P[i+1][0], P[i+1][1]):
            suma += angle(P[i][0], P[i][1], pt_x, pt_y, P[i+1][0], P[i+1][1])
        else:
            suma -= angle(P[i][0], P[i][1], pt_x, pt_y, P[i+1][0], P[i+1][1])
    return m.fabs(m.fabs(suma) - 2*PI) < EPS
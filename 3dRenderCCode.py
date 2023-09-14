import math
import time
import os

cash_map = {}

def render_cash(rd, _points):
    points = {(round(point[0]), round(point[1])): 'x' if ((point[0] / (math.sqrt(point[0]**2 + point[1]**2) if math.sqrt(point[0]**2 + point[1]**2) != 0 else 1) + point[1] / (math.sqrt(point[0]**2 + point[1]**2) if math.sqrt(point[0]**2 + point[1]**2) != 0 else 1)) >= 0.1) else '$' for point in _points}
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    buffer = '\n'.join(''.join(points.get((x, y), ' ') for x in range(min_x, max_x + 1)) for y in range(min_y, max_y + 1))

    cash_map[rd] = buffer



def func_toors(t, u):
    return [
        6*math.cos(t) + math.cos(u)*math.cos(t),
        6*math.sin(t) + math.cos(u)*math.sin(t),
        math.sin(u)
    ]

def mul_point(point, rotation_t_matrix_class):
    return [
        point[0]*rotation_t_matrix_class[0][0] + point[1]*rotation_t_matrix_class[0][1] + point[2]*rotation_t_matrix_class[0][2],
        point[0]*rotation_t_matrix_class[1][0] + point[1]*rotation_t_matrix_class[1][1] + point[2]*rotation_t_matrix_class[1][2],
        point[0]*rotation_t_matrix_class[2][0] + point[1]*rotation_t_matrix_class[2][1] + point[2]*rotation_t_matrix_class[2][2]
    ]

def rotate_x(point, degrees):
    radians = degrees * (math.pi / 180)
    cos = math.cos(radians)
    sin = math.sin(radians)
    rotation_t_matrix_class = [
        [1, 0, 0],
        [0, cos, -sin],
        [0, sin, cos]
    ]

    return mul_point(point, rotation_t_matrix_class)

def rotate_y(point, degrees):
    radians = degrees * (math.pi / 180)
    cos = math.cos(radians)
    sin = math.sin(radians)
    rotation_t_matrix_class = [
        [cos, 0, sin],
        [0, 1, 0],
        [-sin, 0, cos]
    ]

    return mul_point(point, rotation_t_matrix_class)

def scale_point(point, k):
    scalling_matrix = [
        [k, 0, 0],
        [0, k, 0],
        [0, 0, k]
    ]
    
    return mul_point(point, scalling_matrix)

def get_toors(steps, step=0.1):
    points = []
    
    for i in range(int(steps/step)):
        i *= step
        for j in range(int(steps/step)):
            j *= step
            new_point = scale_point(rotate_y(rotate_x(func_toors(i,j), 10), 15),3.5)
            points.append(new_point)

    return points

lines = []

for z in range(-5, 5):
    for y in range(-4, 4):
        for x in range(-5, 5):
            lines.append([x,y,z])

points_square = get_toors(math.pi*2)

for i in range(len(lines)):
	points_square.append(lines[i])

for i in range(360):
	for j in range(len(points_square)):
		points_square[j] = rotate_y(points_square[j], 1)
	render_cash(i, points_square)

clear = lambda: os.system('cls')

def main():
    while True:
        speed_out = 8
        for i in range(0, 360, speed_out):
            clear()
            print(cash_map.get(round(i)))
            time.sleep(10 * speed_out / 1000)

main()


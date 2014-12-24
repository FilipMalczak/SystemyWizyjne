import math


def distance(p1, p2):
    #todo: this is almost literal copy from tracker - refactor!
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def point_between(p1, p2, dl):
    '''
    :param p1: point 1
    :param p2: point 1
    :param distance between p1 and returned point
    '''
    dx = p2[0]-p1[0]
    dy = p2[1]-p1[1]
    d = distance(p1, p2)
    dx *= dl/d
    dy *= dl/d
    return (p1[0]+dx, p1[1]+dy)

def postprocess(points, new_len):
    '''
    Turn list of points into new one, with constant length and identical interval between next two points
    :param points: list of tuples(x, y)
    :param new_len: desired length of output list
    :return: list of tuples(x, y)
    '''
    out = [points[0]]
    #line_lengths[i] = distance(points[i], points[i+1])
    line_lengths = map(lambda x: distance(*x), zip(points[:-1], points[1:]))
    length_sum = sum(line_lengths)
    abs_interval = 1./(new_len-1)
    real_interval = length_sum*abs_interval
    last_idx = 0
    last_point = points[0]
    next_point = points[1]
    left_on_line = line_lengths[last_idx]
    left_until_result = real_interval
    while len(out) < new_len-1:
        while left_until_result - left_on_line >=0 and last_idx<(len(points)-2):
            left_until_result -= left_on_line
            last_idx += 1
            last_point = next_point
            next_point = points[last_idx+1]
            left_on_line = line_lengths[last_idx]
        out.append(point_between(last_point, next_point, left_until_result))
        last_point = out[-1]
        left_on_line -= left_until_result
        left_until_result = real_interval
    out.append(points[-1])
    return out

if __name__ == "__main__":
    print postprocess(
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (4, 1),
            (4, 2)
        ], 4)
   # should print smth like [(0,0), (2, 0), (4, 0), (4,2)], but float
    print postprocess(
        [
            (0, 0),
            (0, 4),
            (1, 4),
            (1.5, 4),
            (2, 4),
            (4, 4),
            (4, 3.5),
            (4, 3),
            (4, 1),
            (4, 0),
            (1, 0),
            (0, 0)
        ], 9)
    # expected: [ (0, 0), (0, 2), (0, 4), (2, 4), (4, 4), (4, 2), (4, 0), (2, 0), (0, 0) ]


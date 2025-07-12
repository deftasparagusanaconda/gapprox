def linear(points, step):
    from math import sqrt
    # Ensure points are sorted by x-coordinate
    points = sorted(points, key=lambda p: p[0])
    
    if len(points) < 2 or step <= 0:
        return points

    result = []
    x_min, y_min = points[0]
    x_max, y_max = points[-1]

    # Number of interpolated points
    num_points = int((x_max - x_min) / step) + 1

    for i in range(num_points):
        x = x_min + i * step
        
        # Find the two points that the x falls between
        if x <= x_min:
            result.append((x_min, y_min))
        elif x >= x_max:
            result.append((x_max, y_max))
        else:
            for j in range(1, len(points)):
                x0, y0 = points[j - 1]
                x1, y1 = points[j]
                
                if x0 <= x <= x1:
                    # Linear interpolation formula
                    t = (x - x0) / (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    result.append((x, y))
                    break

    return result


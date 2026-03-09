import timeit
import math

class DummyPoint:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.call_count = 0

    def x(self):
        self.call_count += 1
        return self._x

    def y(self):
        self.call_count += 1
        return self._y

def test_original():
    point_wgs84 = DummyPoint(45.0, 90.0)

    if not (point_wgs84.x() == point_wgs84.x() and point_wgs84.y() == point_wgs84.y()) or \
       abs(point_wgs84.x()) == float('inf') or abs(point_wgs84.y()) == float('inf') or \
       not (-90 <= point_wgs84.y() <= 90 and -180 <= point_wgs84.x() <= 180):
         pass

def test_optimized():
    point_wgs84 = DummyPoint(45.0, 90.0)

    x = point_wgs84.x()
    y = point_wgs84.y()

    if math.isnan(x) or math.isnan(y) or \
       math.isinf(x) or math.isinf(y) or \
       not (-180 <= x <= 180 and -90 <= y <= 90):
         pass

if __name__ == "__main__":
    n = 1000000

    t_original = timeit.timeit(test_original, number=n)
    print(f"Original execution time for {n} runs: {t_original:.4f} seconds")

    t_optimized = timeit.timeit(test_optimized, number=n)
    print(f"Optimized execution time for {n} runs: {t_optimized:.4f} seconds")

    improvement = (t_original - t_optimized) / t_original * 100
    print(f"Improvement: {improvement:.2f}%")

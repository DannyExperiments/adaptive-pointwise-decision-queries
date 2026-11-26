"""Exact finite checks of the open polyhedral, box and ellipsoid examples."""

from fractions import Fraction as F
from itertools import product
from random import Random


def floor(t, i):
    return max(3 * i - t, t - (3 * i + 2))


def interval(t, m):
    active = [i for i in range(1, m + 1) if 3 * i < t < 3 * i + 2]
    assert len(active) <= 1
    return active[0] if active else None


def check_optimum(vertices, gaps, decision):
    def cost(x):
        return sum(a * b for a, b in zip(x, gaps))

    assert cost(decision) == min(map(cost, vertices))


def open_cases():
    rng = Random(439)
    count = 0
    for m in range(2, 7):
        vertices = list(product((0, 1), repeat=m + 1))
        for tick in range(1, 2 * (3 * m + 4)):
            t = F(tick, 2)
            values = [floor(t, i) + F(rng.randint(1, 12), 8) for i in range(1, m + 1)]
            i = interval(t, m)
            alternatives = [values]
            if i:
                for response in (F(0), floor(t, i) / 2):
                    new = list(values)
                    new[i - 1] = response
                    alternatives.append(new)
            for z in alternatives:
                assert t > 0 and all(v > floor(t, j) for j, v in enumerate(z, 1))
                x = tuple(int(j == i and z[j - 1] < 0) for j in range(m + 1))
                check_optimum(vertices, [t] + z, x)
                count += 1
        # At each pivot, changing just that gap changes the unique optimizer.
        for i in range(1, m + 1):
            t = 3 * i + 1
            base = [max(1, floor(t, j) + 1) for j in range(1, m + 1)]
            for sign in (-1, 1):
                z = list(base)
                z[i - 1] = F(sign, 2)
                assert all(v > floor(t, j) for j, v in enumerate(z, 1))
                assert tuple(int(v < 0) for v in z) == tuple(int(j == i and sign < 0) for j in range(1, m + 1))
    return count


def bounded_cases():
    box_count = ellipsoid_count = 0
    for m in range(2, 7):
        vertices = list(product((0, 1), repeat=m))
        center = F(m + 1, 2)
        for tick in range(int(8 * (center - m)) + 1, int(8 * (center + m))):
            z = F(tick, 8)
            assert abs(z - center) < m
            near = [i for i in range(1, m + 1) if abs(z - i) < F(1, 4)]
            assert len(near) <= 1
            i = near[0] if near else None
            for offset in (F(-1, 8), F(0), F(1, 8)):
                u = [offset if j == i else offset / 2 for j in range(1, m + 1)]
                gaps = [z - j + u[j - 1] for j in range(1, m + 1)]
                decision = tuple(int((gaps[j - 1] if j == i else z - j) < 0) for j in range(1, m + 1))
                assert all(abs(v) < F(1, 4) for v in u)
                check_optimum(vertices, gaps, decision)
                box_count += 1
                if ((z - center) / m) ** 2 + 16 * sum(v * v for v in u) < 1:
                    ellipsoid_count += 1
        for i in range(1, m + 1):
            # Equal center coordinate, sign-changing neighbors strictly inside both priors.
            assert ((i - center) / m) ** 2 + F(1, 16) < 1
            for sign in (-1, 1):
                gaps = [i - j if j != i else F(sign, 16) for j in range(1, m + 1)]
                assert all(gaps)
                decision = tuple(int(gap < 0) for gap in gaps)
                check_optimum(vertices, gaps, decision)
    return box_count, ellipsoid_count


def explorer_cases():
    count = 0
    for tick in range(8, 49):
        t = F(tick, 4)
        active = interval(t, 3)
        for sign in (-1, 0, 1):
            gaps = [floor(t, i) + 1 if i != active else
                    (floor(t, i) / 2 if sign < 0 else F(sign, 2)) for i in range(1, 4)]
            assert all(v > floor(t, i) for i, v in enumerate(gaps, 1))
            decision = [int(v < 0) for v in gaps]
            assert decision == [int(i == active and sign < 0) for i in range(1, 4)]
            count += 1
    return count


def main():
    print(f'Open polyhedron: {open_cases()} exact optimizer checks for m=2 through 6.')
    box, ellipsoid = bounded_cases()
    print(f'Bounded variants: {box} box checks, including {ellipsoid} ellipsoid members.')
    print(f'Explorer: {explorer_cases()} exact sign-and-route states, including interval endpoints.')
    print('Finite diagnostics only; the exact general query-count algorithm is proved in the manuscript.')


if __name__ == '__main__':
    main()

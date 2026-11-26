# Problem and proof

Given a rational linear program and an open rational convex prior on its cost, an adaptive policy chooses an exact linear measurement after seeing earlier answers. The goal is a point that minimizes cost for the entire remaining fiber.

The predicate Win0 says that one feasible point beats every other point at every consistent cost. To win with one additional query, either stop now or choose a query whose every feasible answer leaves a winning shorter history. The resulting formulas are first-order over the reals with polynomial input length at depths up to the ambient dimension. Quantifier elimination computes the first winning depth, and semialgebraic selection yields policy choices on winning histories.

A single fixed measurement set that gives a common optimum on each open-prior fiber recovers the full optimal face. Equal-answer costs with different optimal faces would retain equal answers under a common perturbation exposing one different vertex, but would then have no common optimum. Thus the fixed benchmark is the dimension of the span of differences of reachable optimal vertices.

In the cube example, query t. The inequalities on costs force all but at most one gap to be positive. When t lies in an open interval, query the one gap that can change sign. A fixed query system must separate both sides of each gap’s interior sign-change point. This requires all m independent gap directions. A bounded rational box with shifted gap coordinates gives the same separation. The ellipsoid version is a separate extension.

[Full proof](../paper/manuscript.pdf) · [Exact replay](../verification/src/replay.py)

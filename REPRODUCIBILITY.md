# Reproducibility

Run both commands from the repository root with Python 3.11 or later and Git.

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The exact standard-library replay verifies 275 open-polyhedral costs and 945 bounded-box costs, of which 853 also lie in the ellipsoid. It compares each returned decision to all cube vertices. It separately verifies 123 exact explorer states, including ties and interval endpoints. The manuscript proves the general query-count procedure using real quantifier elimination. [Expected output](verification/logs/replay.txt)

[Build the manuscript](paper/BUILD.md) · [Rebuild the figure and open the explorer](visualization/README.md)

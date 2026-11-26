# Worked cost windows

The 3D plot maps each gap index to a separate lane. Its horizontal coordinate is t, the third axis separates the lanes, and the height on lane i is z_i. Each V is a displayed piece of the exact lower bound max(3i − t, t − 3i − 2). Points strictly above the lower bound are allowed. The colored area between each V and height zero shows where that gap can have a negative value.

The GIF shows three interior t values and an endpoint. At the endpoint all gaps are strictly positive. At each interior point the policy queries the one lane whose negative wedge contains that t. A negative second response selects that cube coordinate. A positive or tied response permits the all-zero decision.

Extract the [offline explorer](adaptive-cost-windows-explorer.zip) and open index.html. Drag the canvas or use the rotation slider. Move t in quarter steps and choose an allowed sign for the second response. The [replay](../verification/src/replay.py) verifies the exact choices for all 123 displayed state combinations.

Rebuild the ZIP and the 704 × 840 GIF by running python3 visualization/render.py with Python 3.11 or later, Pillow 13 and the Arial faces supplied with macOS. The optional --output argument rebuilds to another folder.

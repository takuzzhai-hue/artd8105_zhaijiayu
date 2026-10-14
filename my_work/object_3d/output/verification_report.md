# STL check

```
[PASS] Header 80 bytes  text=b'parametric jar / ARTD8105'
[PASS] Triangle count field uint32 count=61056
[PASS] File size filesize=3052884 expected=3052884 (= 84 + 50*61056)
[PASS] Triangle count triangles=61056
[PASS] Bounding box min=[-41.9333, -49.9103, 0.0] max=[72.7476, 58.6828, 170.9318]
[PASS] Dimensions size=[114.6808, 108.5931, 170.9318] mm
[PASS] Signed volume 179276.5576 mm³  (must be > 0)
[INFO] Vertex welding welded_vertices=30530 from 183168  q=0.0001 mm
[PASS] Degenerate triangles count=0
[PASS] Boundary edges count=0 (must be 0)
[PASS] Non-manifold edges count=0 (must be 0)
[PASS] Each edge used twice unique_edges=91584 twice=91584
[PASS] Opposite winding on shared edges disagreeing edges=0 (must be 0)
[PASS] Shells (union-find) count=1 (must be 1)  triangles per shell=[61056]
[PASS] Euler V-E+F V=30530 E=91584 F=61056  χ=2 (must be 2)
[PASS] Wall thickness (ray) K=2500 hits=2461 misses=39  min=3.647 p1=3.712 median=3.991 mm  (min must be ≥ 1.6 mm). Sample of centroids, not a global proof.
SUMMARY ALL PASS
```

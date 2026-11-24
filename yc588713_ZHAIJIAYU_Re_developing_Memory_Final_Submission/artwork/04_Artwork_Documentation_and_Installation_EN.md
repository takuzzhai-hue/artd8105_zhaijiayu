# Artwork documentation and installation requirements

Re-developing Memory. Artist: Zhai Jiayu (yc588713). Documentation updated 24 November 2026 from the files now in this package.

## 1. Work identification

| Field | Description |
|---|---|
| Title | Re-developing Memory |
| Type | Narrative-driven photographic reworking; cumulative stages recombined as a vertical-strip test print, shown with the running system |
| Medium | Photographs, written recollection, RAW and display-image processing, constrained local generation, intermediate images, strip composites |
| Artist / year | Zhai Jiayu (yc588713); 2026 |
| Shown | B15 exhibition record, photographed 18 November 2026. See section 5. |

## 2. Artistic concept

The work begins with a personal photograph and a written recollection and lets the photograph enter a process of formation again. Brightness, movement, disappearance, touch, and uncertain space become visible operations. It distinguishes renderings grounded in captured data, non-generative changes to an existing photograph, and speculative additions where something was never recorded. Stages stay available and are recombined as aligned vertical strips, so one frame can hold several processing times. The result does not recover an authentic memory.

## 3. Executable RAW-reworking workflow

The runnable program is `Memory_Reconstruction_system_20261124/` in this submission folder. Install from its `README.md`. `src/engine.py` develops a RAW file once with rawpy (`use_camera_wb`, linear gamma, 16-bit output) and then applies each JSON operation to the previous image. It writes 16-bit PNG stages and `log.json`. It does not call a generative model. The browser interface is started with `src/app.py` and opens at `http://127.0.0.1:7860/`. Language and generation calls need a DashScope key in a local `.env`. That key is not in the repository.

Provenance classes in the program: R is RAW-derived development, E is another non-generative operation, G is generative supplementation. JPEG and PNG inputs are display-image processing, not sensor measurements.

One saved run is `memory-reconstruction /`, logged in `series.json` on 17 November 2026. The recollection asks for a darker, greener forest, sharp foreground branches, and a blurred background. Six stages were saved. The log states that this run used a reduced 8-bit preview and is not a full-size RAW finish. Masks are in `memory-reconstruction /run_01/`. A reduced copy of the log and the composite is in `my_work/prints/`.

## 4. Final test-print series

| Plate | File | What it shows |
|---|---|---|
| Figure 1. Pendulum | `figures/Figure_1.png` and `my_work/paper/figures/figure_01_case.png` | Original, four cumulative stages, strip composite. Exposure −0.35 EV; light-ring exposure −0.42 EV; sphere blur amount 0.11 at 0°; vignette 0.12. |
| Figure 2. Vanishing hand | `figures/Figure_2.png` and `my_work/paper/figures/figure_02.png` | Source and local whiteout. The white region keeps the space of the hand. |
| Figure 3. Index finger | `figures/Figure_3.png` and `my_work/paper/figures/figure_03_case.png` | Waterfront source and a generated finger. The finger is conjecture. |
| Figure 4. Forest | `figures/Figure_4.png` and `my_work/paper/figures/figure_04.png` | Stages and a composite with stretching and hard seams. |
| Forest test print | `my_work/prints/forest_testprint.jpg` | Composite from the 17 November run. Stages: `forest_step_01.jpg`, `forest_step_06.jpg`. Log: `forest_series.json`. |

## 5. B15 exhibition

Photographs taken 18 November 2026, 11:54, supplied as the B15 exhibition record:

- `artwork/exhibition/b15_01.jpg` (from `IMG_1865.HEIC`)
- `artwork/exhibition/b15_02.jpg` (from `IMG_1866.HEIC`)
- Copies: `my_work/prints/b15_exhibition_01.jpg` and `b15_exhibition_02.jpg`

The table holds a poster titled *Redeveloping Memory*, printed pages, and a laptop running the system. The screen shows a forest image. A wall mark near the elevator reads “1 A”. The image files do not print the characters “B15”; they are the installation photographs provided for that exhibition. Neighbouring posters and the white wire sculptures are other displays. Paper size, screen size, and illuminance were not measured.

## 6. What a later installation still needs

| Element | In this package | Not measured here |
|---|---|---|
| Computer | The laptop in the B15 photographs was running the interface | Operating system, GPU, and VRAM of that machine |
| Software | Source, `requirements.txt`, `Start_Mac.command`, `Start_Windows.cmd` | A fresh install on another machine, including model download |
| Network | Required for DashScope calls | Offline behaviour |
| Prints | The four plates and the forest test print | Paper stock, physical dimensions, colour management |
| Privacy | Demonstration images are in the run folder | A consent notice is still required before a visitor’s own photograph is uploaded |

## 7. Limits

The work shows more than one visual version of a photograph directed by a written recollection. It does not prove that a personal memory was recovered. The 17 November forest run is a preview log, not a full-size RAW finish. Blur, whiteout, and broken space are pictorial operations, not measurements of psychology.

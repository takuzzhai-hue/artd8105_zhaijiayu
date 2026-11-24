# Test-print series, RAW workflow, and B15 exhibition

## Final test-print series

The finished plates are the vertical-strip composites in `my_work/paper/figures/`:

- `figure_01_case.png`, pendulum
- `figure_02.png`, vanishing hand
- `figure_03_case.png`, added index finger
- `figure_04.png`, forest rupture

A separate forest run, saved 17 November 2026, is the test-print series for one recollection. The wording is in `forest_memory.txt`. The operation log is `forest_series.json`. Six stages run from exposure, saturation, local exposure, local contrast, and local sharpen on the foreground branches, to local blur on the background. `forest_step_01.jpg` and `forest_step_06.jpg` are the first and last stages. `forest_testprint.jpg` is the saved composite. The log says these steps were applied to a reduced 8-bit preview and are not a full-size RAW finish. The full-size files and masks remain in `yc588713_ZHAIJIAYU_Re_developing_Memory_Final_Submission/memory-reconstruction /`.

## Executable RAW-reworking workflow

The program that can be installed and run is `yc588713_ZHAIJIAYU_Re_developing_Memory_Final_Submission/Memory_Reconstruction_system_20261124/`. Follow `README.md` in that folder. `src/engine.py` is the RAW path: it develops a RAW file once with rawpy, then applies a JSON list of operations to the previous result and writes 16-bit PNG stages plus `log.json`. It does not call a generative API. The web interface is `src/app.py` at `http://127.0.0.1:7860/`. A DashScope key belongs in a local `.env` and is not in the repository.

## B15 exhibition

Two photographs supplied as the B15 exhibition record, taken 18 November 2026 at 11:54:

- `b15_exhibition_01.jpg`
- `b15_exhibition_02.jpg`

Original camera files: `yc588713_ZHAIJIAYU_Re_developing_Memory_Final_Submission/IMG_1865.HEIC` and `IMG_1866.HEIC`.

What the photographs show: a poster titled *Redeveloping Memory* on a board, printed pages on the table, and a laptop running the system with a forest image on screen. The wall near the elevator is marked “1 A”. The photographs do not themselves print the characters “B15”; they are filed here as the B15 installation record that was supplied. The white wire sculptures and the other posters in the room belong to neighbouring displays. Print size, screen size, and lighting were not measured from these photographs.

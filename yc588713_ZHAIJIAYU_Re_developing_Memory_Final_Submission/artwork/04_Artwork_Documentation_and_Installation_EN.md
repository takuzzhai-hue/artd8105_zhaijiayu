# Artwork documentation and installation requirements

Re-developing Memory. Artistic prototype and proposed display specifications. Converted from the Word file. The artist line now names Zhai Jiayu (yc588713). The PDF beside this file is older and still has the blank artist line.

## 1. Work identification

| Field | Description |
|---|---|
| Title | Re-developing Memory |
| Type | Narrative-driven interactive photographic re-creation prototype; cumulative stage images recombined as a vertical-strip photographic work |
| Medium | Existing photographs, recollection text, computational image processing, constrained local AI generation, intermediate images, final composites |
| Documented status | Artist manuscript, prototype claims, and four sets of case-study output supplied; public deployment and actual installation not documented |
| Artist / year | Zhai Jiayu (yc588713); 2026 |
| Documentation version | 24 November 2026; retrospective record with unverified installation fields |

## 2. Artistic concept

The work begins with a personal photograph and a written recollection and allows the photograph to enter a process of formation again. Descriptions of brightness, movement, disappearance, touch and uncertain space are translated into visible image operations. The work distinguishes alternative renderings grounded in captured data, non-generative interventions in an existing photograph, and speculative additions where something was never recorded. Stages do not replace each other to reveal one correct image: they remain available and are recombined as aligned vertical strips so a single frame can contain several processing times. The result does not recover an authentic memory; it makes choices, losses, additions and speculation visible as a photographic poem.

## 3. Interactive and export workflow

Upload a photograph (RAW, JPEG, or PNG) and enter recollection text. The system analyzes the scene and narrative, plans operations and scope, segments regions where needed, applies successive changes to the preceding stage, saves and shows those stages, takes aligned vertical strips, and exports a final image with whatever process record is available.

Provenance classes: R means genuine RAW-derived development; E means a non-generative photographic operation; G means generative supplementation. Whether the running program can export that record directly still has to be confirmed from the repository. The disclosure names the current Qwen services, SAM 2.1 Hiera Tiny, Depth Anything V2 Small, and rawpy/LibRaw. Which model ran on each earlier example still needs the execution record.

## 4. Case images

**Figure 1. Pendulum: time within an instant.** Original scene, tonal adjustment, blur and vignette stages, and the final strip composite. Reported values: global exposure −0.35 EV; light-ring exposure −0.42 EV; sphere blur amount 0.11 at 0°; vignette amount 0.12.

**Figure 2. Vanishing hand: the shape of forgetting.** Source image versus local whiteout. The white region keeps the space the hand occupied. It does not invisibly rebuild the background.

**Figure 3. Adding an index finger: touch beyond the frame.** Chicago waterfront compared with an image that has a foreground index finger. The added gesture is speculative generation, not evidence from the source photograph.

**Figure 4. Forest: spatial rupture beyond framing.** Forest source, fragmentation stages, and composite. Extension, duplicated fragments, and visible joins show uncertainty. They do not repair the scene seamlessly.

## 5. Installation requirements

This is a proposed checklist. Print size, the actual computer, and any public installation were not measured.

| Element | Known or proposed | Still needs testing |
|---|---|---|
| Interactive station | A computer and display that can run the project, with a keyboard and mouse or the equivalent | Operating system, browser, GPU and VRAM, model-service limits |
| Software | The real frontend, backend, and image-processing dependencies | Environment variables, lockfiles, supported RAW formats, startup commands |
| Connectivity | Needed if remote model or API calls are turned on | Whether it can run offline, and the exact service domains |
| Visitor workflow | Upload, enter a recollection, see stages, export the composite | File limits, waiting time, errors, and export, tested on site |
| Static alternative | Show the final strip composite and the stage comparisons | Print medium, mounting, physical size, color management |
| Sound, projection, sensors | The manuscript does not require them | Add them only if a later version actually uses them |
| Privacy and rights | A consent notice for personal photographs and memories. Do not show private test data | How long files are kept, deletion, any training use, licenses, and permission to exhibit |

## 6. Setup sequence

Before setup, check the computer and display, use a real project commit, install dependencies, and test the configured models or APIs. Use demonstration images and text that are not private.

To launch, follow the project README, open the interface, and test an upload and the stage viewer. Copy the launch commands from the actual codebase.

To test, reproduce one supplied example: the same input, the same stage order, and the same final composite. If the setup needs the network, also test what happens when a request fails.

While it is in use, say clearly that generated additions are not recovered historical evidence. Do not leave a visitor's photograph or recollection on a public computer.

Afterwards, keep only the documentation you are allowed to keep, and delete visitor inputs according to the project's real retention rule.

## 7. Files in this package

The manuscript source is `paper/Re_developing_Memory_SIGGRAPH_ACM_Review.tex`, with PDFs beside it. Case figures are `figures/Figure_1.png` through `figures/Figure_4.png`.

The program source, dependency locks, RAW files, execution JSON, masks, prompts, per-run model names, a demonstration video, interface screenshots, and installation photos are not in this folder.

## 8. Limits

The work shows more than one visual version of a photograph directed by a written recollection. It does not prove that a personal memory was recovered accurately. RAW stages, ordinary edits, and generated additions need different labels. Blur, whiteout, and broken space should not be described as psychological mechanisms. The display sizes above stay proposals until they are tested in the actual room.

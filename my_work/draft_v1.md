# Re-Developing Memory: The Boundaries of Photographic Records and the Labeling of Generative Content in RAW-Based Photographic Reworking

Submission manuscript: `paper/Re_developing_Memory_SIGGRAPH_ACM_Review.tex`, ACM `acmart`, options `manuscript`, `review`, `anonymous`, `authoryear`. This file is the shortened working text for the SIGGRAPH 2027 Art Papers long track (3,500 words maximum). The author name is omitted for anonymisation. Figures cited below are in `my_work/paper/figures/`.

## Abstract

Photographs organize a scene through exposure, optics, and computational processing. Personal recollections are shaped by attention, emotion, and time. This study proposes a method of photographic reworking driven by written recollections. Where the existing record can support a request, the response is RAW re-development or another named non-generative operation. Where it cannot, the work uses an explicitly labeled generative addition or leaves the gap. Original wording, interpretation, operation, and affected region stay attached to the image. Saved stages are then assembled, in the manner of darkroom test prints, into one photographic image. The result does not claim to recover the past.

## 1. Introduction

At the instant of pressing the shutter, the body occupies a space: temperature, the movement of light, and the memory of having stood there overlap. The camera records only the light inside one exposure and processes it through a program. For Bergson (1991 [1896]), the past has already entered present perception before the shutter is pressed. This gap is the starting point. The aim is not to prove that the camera was wrong, but to let a written recollection re-enter the formation of the photograph.

Both sides select. The sensor signal passes through white balance, demosaicing, color transformation, denoising, and tone mapping before it becomes a viewable image. Recollection, by contrast, brings some details forward and drops others. A mismatch is therefore treated as a creative prompt. “I remember the light being warmer” may guide a color adjustment. It cannot prove that the camera’s white balance was incorrect.

Generative tools can rewrite a photograph seamlessly, and a seamless result hides which parts come from the record, which from a processing choice, and which from a model. The question is: **How can personal narratives intervene in RAW re-development, and how can the artwork make visible the relationships among record-derived processing, authorial interpretation, and generative additions?** The contribution is a traceable artistic form, not a verification of memory.

## 2. Theoretical and Artistic Context

This study approaches photography through two dimensions: the photographic apparatus and digital imaging. Flusser (2000 [1983]) describes the camera as an apparatus that executes a “program.” The photographer operates within the possibilities predefined by that program, and images result from the realization of those possibilities. Flusser also suggests that photographic freedom lies in working against the apparatus's program, deliberately producing outcomes the program did not anticipate. Research on imaging pipelines makes this “program” concrete. Karaimer and Brown (2016) observe that internal camera-processing stages are often embedded in hardware, rely on proprietary manufacturer algorithms, and are difficult to access. They therefore developed a software platform that allows RAW images to pass step by step through black-level correction, white balance, demosaicing, color-space conversion, denoising, and tone mapping, while enabling intermediate images and parameters to be inspected and modified at each stage. Together, these perspectives indicate that “development” in digital photography involves choosing among multiple possible renderings rather than revealing an already complete image. This is precisely why this paper uses the term **“re-development”**: RAW data are not yet a viewable image; they become a photograph only through a series of rendering decisions, and those decisions can be made again. Yet re-development has limits. Exposure time, aperture, and the actual plane of focus have already determined what information reaches the sensor. Subsequent adjustments can work only within the constraints of the existing record and available processing. This study therefore limits its interventions to accessible development and image-processing stages and explicitly distinguishes reprocessing from content generation.

Recollection follows a different organizational logic. In “Photography,” Kracauer (1995 [1927]) distinguishes photographs from “memory images”: photography grasps what is given as a spatial (or temporal) continuum, whereas memory images retain what is given only insofar as it has significance. Memory images and photographic representations are therefore in conflict. This distinction corresponds directly to a statement such as “I only remember her face”: what recollection preserves is what matters to the person remembering, not the entire field of vision. Bartlett's (1932) experiments likewise show that remembering is not the reactivation of a fixed trace but a form of “imaginative reconstruction,” shaped by the rememberer's existing schemas and attitudes (p. 213). Kuhn's (1995) concept of “memory work” further treats family photographs as sites where recollections are produced rather than as evidence of memory: looking at photographs itself contributes to the construction of narratives about the past. These arguments support a premise of the present method: statements such as “brighter,” “colder,” or “I only remember one person” may refer to visual attributes, but they may also express feelings that cannot be translated directly into image parameters. Narrative statements cannot be treated as determinate technical instructions. A single statement may correspond to several processing approaches, and the artist must interpret the available possibilities and document how that interpretation affects the resulting image.

The influence between photographs and recollections also works in both directions. Wade et al. (2002) showed participants manipulated childhood photographs in which they had been composited into a hot-air balloon ride that had never taken place. Approximately half subsequently reported full or partial memories of the event in interviews. Pataranutaporn et al. (2025) revisited this issue in the context of generative AI. Two hundred participants first viewed 24 original images and, after a distraction task, were assigned to four groups that viewed either the original images again, AI-edited images, videos generated from the original images, or videos generated from AI-edited images. All three AI conditions produced more false memories than the control condition, with the strongest effect in the edited-image-to-video condition; participants' confidence in inaccurate memories also increased. These findings suggest that modifying one's own photographs in this study might likewise reshape subsequent recollections. They do not, however, establish that labeling generated content would prevent such effects.

Art and design practices have already addressed relationships between generated images and memory. Zhang, Cheng, and Luo's *ReCollection* (Zhang et al. 2024; first exhibited in 2023) grew out of an author's experience of witnessing their grandmother's memory decline due to dementia. Participants whisper a fading memory of approximately seven seconds into a microphone. Through speech recognition, automatic text completion, and text-to-image generation, the system assembles an evolving “collective visual memory” in real time, blurring the boundary between “remembering” and “imagining.” Domestic Data Streamers' *Synthetic Memories* project, underway since 2023, uses interviews and generative AI to help people living with dementia, migrants, and others reconstruct visual memories of scenes never photographed or of images that have been lost. Interviewers and narrators iteratively revise the images together. In 2024, the project operated as the “Citizen Office of Synthetic Memories” at the Barcelona Design Museum; it is currently exhibited in MoMA's *Full Disclosure* exhibition in New York. Both projects begin with verbal narratives and generate whole images; an original visual record either does not exist or does not participate in the generation. A CHI study by Wu et al. (2026), by contrast, focuses on existing photographs. Twelve participants used generative AI to edit their own photographs and then took part in semi-structured interviews. The study found that participants valued “felt memories” more than factual accuracy and were willing to modify environments but were reluctant to accept edits that changed people's identities. The editing process itself also became an experience of remembering. The authors further note that, when photographs circulate outside their original contexts, editing intentions and histories may not travel with them. This observation directly informs the present study: its annotations are intended to keep editing histories attached to the image.

In contrast to these works, this study takes the RAW data of an existing photograph as both its creative material and its constraint, rather than generating an entire image directly from language. It translates personal narratives into traceable processing choices and incorporates insufficient records, generative additions, and unresolved absences into the final work. The artwork presents not only the modified image but also why it was modified, what materials those modifications relied upon, and which parts involve speculation.

## 3. Method

The material is a photograph plus a written recollection. The running system accepts RAW, JPEG, PNG, or HEIC, reads the text, proposes an operation and a region, applies that operation to the previous stage, and saves the stage. Three kinds of response are distinguished. RAW-derived development (R) reorganizes information the file still holds. Other non-generative operations (E), such as local whitening, blur, or a vignette, change how the existing image is seen and add no new object. Generative supplementation (G) is used only for content the photograph never recorded, and the region is labeled as an addition. If the record’s status is uncertain, the gap is kept rather than filled automatically.

Each change is stored as original wording, interpretation, operation, parameters, and region. A JPEG or PNG example is display-image processing. It is not described as a sensor measurement. The four cases below are the artist’s own tests. No separate participant sample was collected, and no claim is made about how other viewers would remember the images.

The final presentation borrows the darkroom test print. Vertical strips from the original and from successive stages are placed side by side, so one frame holds several processing times. The exhibition form actually used is documented separately: a poster, printed pages, and the system running on a laptop.

## 4. Artwork and Case Analysis

**Case 1, pendulum (Figure 1).** The recollection asked for a darker image, a less bright ring of lights, a moving pendulum, and a vintage vignette. The saved order is global exposure −0.35 EV, local exposure of the light ring −0.42 EV, motion blur on the sphere (amount 0.11, angle 0°), and vignette amount 0.12. The blur is an algorithmic setting. It is not a measurement of the pendulum’s path. The still photograph is set against a recollection of duration, and the stages remain in the strip composite.

**Case 2, vanishing hand (Figure 2).** The wording was “I want to forget her; I want her hand to disappear.” Local whitening occupies the space of the hand and ring. It does not rebuild the background. Absence stays visible.

**Case 3, index finger (Figure 3).** A waterfront photograph was paired with “I used my index finger to trace the outlines of these buildings.” No hand is in the source frame, so a foreground finger was generated. The image is conjecture, not a recovered exposure.

**Case 4, forest (Figure 4).** The wording asked for a slight shift of viewpoint, misalignment, and rupture. The result extends the forest and sets slices back into the frame with stretching and hard seams. The seams are the point of contact between the record and the conjecture. They are not a repaired scene.

## 5. Discussion and Limitations

The work brings development choices and the boundary of generation into the image a viewer can inspect. Traceability also shows the artist’s authority: the same sentence can lead to more than one operation, and the chosen one is an interpretation.

RAW is a material and a limit. It can reorganize recorded information. It cannot restore detail the sensor never captured, and it cannot decide whether a memory is true. A file that is only a JPEG, a missing metadata field, or a sentence that will not become an image all narrow what the method can do. A generative label tells where new content came from. Wade et al. (2002) showed that a false photograph can be taken up into later recollection. The label does not prove that a viewer will refuse that content.

These four cases describe one working process. They do not generalize to other people’s memory, and no study here measured whether the images changed what someone later recalled. That question remains untested.

## 6. Conclusion

The study offers a narrative-driven reworking of photographs that keeps RAW re-development, non-generative operations, and labeled generation distinct. The pendulum turns a frozen instant toward remembered duration. The whitened hand keeps the shape of a disappearance. The added finger crosses the frame and is marked as speculation. The forest leaves spatial uncertainty as a visible break. The work does not select the one image closest to the past. It keeps the original, the stages, and their provenance together.

## Why It Matters

Photographs usually appear as finished outputs, concealing the computational choices through which they become visible. Re-developing Memory turns those choices into artistic material and connects them to personal recollection. By distinguishing RAW-derived renderings, non-generative photographic interventions, and AI-generated additions, the work makes image provenance part of its visual language. Its staged, strip-based composition invites the SIGGRAPH community to reconsider photographic finality and the boundary between recorded evidence and computational imagination.

## AI use disclosure

AI assistance was used as follows. Inside the artwork, Qwen Plus turns a recollection into an operation plan inside a fixed catalogue; Qwen3-VL-Plus looks at the photograph and checks proposed additions; Qwen Image 2.0 Pro supplies a constrained addition or extension only when that path is authorized. SAM 2.1 Hiera Tiny estimates masks locally. Depth Anything V2 Small estimates relative depth for synthetic defocus. RAW decoding uses rawpy/LibRaw. Compositing uses NumPy, OpenCV, and Pillow, which are not generative models. A generated region is a speculation, not evidence of the remembered event. The model name on a particular earlier example is the one in that run’s record, where a record exists.

For the manuscript and the program, Cursor and Codex assisted with implementation, tests, and debugging. ChatGPT assisted with English wording, layout, and a first pass over references. Every cited source used below was checked against the publication or the project page. The argument, the choice of operations, and the selection of figures are the author’s. A reconstructed research log, marked as reconstructed, is kept in `my_work/_research_log/`. It is not a live transcript of every working session.

## Implementation and Process Documentation

The executable system is `yc588713_ZHAIJIAYU_Re_developing_Memory_Final_Submission/Memory_Reconstruction_system_20261124/`. `src/engine.py` develops a RAW file once with rawpy (`use_camera_wb`, linear gamma, 16-bit) and then applies a JSON list of operations, in order, to the previous result. It writes 16-bit PNG stages and a `log.json`. It does not call a generative API. `src/app.py` serves the web interface at `http://127.0.0.1:7860/` after the steps in that folder’s README. A DashScope key is required for the language and generation calls and is not stored in the repository.

One completed run is stored at `memory-reconstruction /` in the same submission folder, with a copy of its log at `my_work/prints/forest_series.json`. The recollection was “整个森林会更按一点，绿色会更加浓郁，当时我关注的焦点在最前面的树上，后面一片模糊.” Six stages were saved on 17 November 2026: exposure −0.25 stops; saturation 0.13; local exposure 0.22, local contrast 0.23, and local sharpen 0.16 on the foreground conifer branches; local blur 0.08 on the background. The log states that these steps were applied to a reduced 8-bit preview and are not a full-size RAW finish. The strip composite is `my_work/prints/forest_testprint.jpg`. Masks from that run are in `memory-reconstruction /run_01/`.

The four case plates are `my_work/paper/figures/figure_01_case.png` through `figure_04.png`. Installation photographs from the B15 exhibition, taken 18 November 2026, are `my_work/prints/b15_exhibition_01.jpg` and `b15_exhibition_02.jpg`.

## References

Bartlett, F. C. (1932). *Remembering: A Study in Experimental and Social Psychology*. Cambridge University Press.

Bergson, H. (1991). *Matter and Memory* (N. M. Paul and W. S. Palmer, Trans.). Zone Books. (Original work published 1896).

Domestic Data Streamers. (2023). *Synthetic Memories* [Art and research project]. https://www.domesticstreamers.com/work/synthetic-memories/

Flusser, V. (2000). *Towards a Philosophy of Photography* (A. Mathews, Trans.). Reaktion Books. (Original work published 1983).

Karaimer, H. C., and Brown, M. S. (2016). A software platform for manipulating the camera imaging pipeline. In *Computer Vision, ECCV 2016* (pp. 429–444). Springer. https://doi.org/10.1007/978-3-319-46448-0_26

Kracauer, S. (1995). Photography. In *The Mass Ornament: Weimar Essays* (T. Y. Levin, Ed. and Trans., pp. 47–63). Harvard University Press. (Original work published 1927).

Kuhn, A. (1995). *Family Secrets: Acts of Memory and Imagination*. Verso.

Pataranutaporn, P., Archiwaranguprok, C., Chan, S. W. T., Loftus, E., and Maes, P. (2025). Synthetic human memories: AI-edited images and videos can implant false memories and distort recollection. In *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems*. ACM. https://doi.org/10.1145/3706598.3713697

Wade, K. A., Garry, M., Read, J. D., and Lindsay, D. S. (2002). A picture is worth a thousand lies: Using false photographs to create false childhood memories. *Psychonomic Bulletin & Review*, 9(3), 597–603. https://doi.org/10.3758/BF03196318

Wu, Y., Li, Q., van den Hoven, E., and Kocaballi, A. B. (2026). “I'm happy even though it's not real”: GenAI Photo Editing as a Remembering Experience. In *Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems*. ACM. https://doi.org/10.1145/3772318.3790927

Zhang, W., Cheng, L., and Luo, J. (2024). ReCollection: Creating synthetic memories with AI in an interactive art installation. *Proceedings of the ACM on Computer Graphics and Interactive Techniques*, 7(4), Article 51, 1–10. https://doi.org/10.1145/3664207

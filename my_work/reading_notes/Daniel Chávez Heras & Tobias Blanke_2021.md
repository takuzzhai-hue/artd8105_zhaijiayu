Reading Notes: On Machine Vision and Photographic Imagination
Daniel Chávez Heras & Tobias Blanke (King's College London / University of Amsterdam), AI & Society, 36, 1153–1165 (2021). DOI: 10.1007/s00146-020-01091-y.

1 · Why I Read This Paper
Rather than understanding machine vision exclusively as an image recognition technology, this paper investigates the photographic media through which machines see the world.

Drawing on photographic philosophy, the history of optical technologies, dataset analysis, and neural network experiments, the authors develop a research approach centred on implied optical perspectives.

Among these three papers, it offers the greatest theoretical relevance to my long-term investigations into the locus of photographic existence, the camera's gaze, machine vision, and imaging mechanisms.

Of particular importance is its transformation of photographic properties, such as focal length, aperture, and exposure, from seemingly technical parameters into theoretical questions concerning vision and knowledge production.
2 · Summary
- What the paper is about: Taking the BBC's 2018 experimental television programme Made by Machine: When AI met the Archive as a case study, the authors investigate how machine vision systems inherit photographic practices and optical modes of seeing embedded within their training data.
- Main contributions: The paper introduces the concepts of the implied optical perspective and the latent camera, examining the technological foundations of machine vision through the EXIF metadata of photographic datasets.
- What problem it addresses and why it matters: Critical studies of machine vision frequently focus on data annotation, object classification, and social biases, while overlooking the fact that photographic images used as training materials are already technologically and culturally mediated.
- Innovation and benefits: The study incorporates photographic equipment, imaging parameters, and visual forms into the critical investigation of machine vision.
- What it advances: The authors develop a convolutional neural network prototype capable of distinguishing between wide-angle and telephoto photographs. This enables machines to investigate not only what an image depicts but also how the image was produced.
3 · Critical Thinking
- Photographic parameters do not constitute a complete mode of seeing. Focal length, aperture, and exposure can partially explain the visual forms of photographs. However, the photographer's physical position, intentions, temporal experiences, and post-processing decisions also contribute to the mechanisms of viewing.
- The concept of the latent camera could be further expanded. The paper primarily discusses the latent camera through the optical characteristics of conventional lenses. Nevertheless, computational processes in contemporary smartphone photography, including HDR, multi-frame fusion, semantic segmentation, and local colour processing, also constitute a form of latent algorithmic camera.
- Focal length classification may be influenced by image content. Wildlife photographs, for example, are frequently captured with telephoto lenses, while architectural photographs often employ wide-angle lenses. If the neural network recognises subject-specific characteristics rather than optical properties, its ability to explain photographic modes of seeing requires further examination.
- Difficulties in establishing causal relationships between datasets and machine vision. The predominance of particular photographic practices within training datasets does not necessarily mean that all visual judgements produced by a model are directly determined by those optical practices.
- A distinction remains between seeing and perceiving. Machines may be capable of analysing photographic imaging parameters, but whether such analysis constitutes perception remains an unresolved philosophical question.
4 · Creative Thinking
- New ideas inspired by the paper: Machine vision does not encounter an unmediated world. Rather, it encounters a world that has already been mediated through cameras, photographers, and image-processing systems.
- Methodological transfer: The paper's EXIF-based research could be extended to camera Image Signal Processing (ISP) pipelines, investigating whether different denoising, sharpening, colour mapping, and HDR strategies produce visual characteristics that can be distinguished by machines.
- Alternative approaches to the same problem: The authors work backwards from completed images to infer their imaging mechanisms. My artwork could instead work forwards from the imaging process, revealing the various forms that a photograph could potentially assume. These approaches constitute two complementary ways of opening the photographic black box: reverse analysis and processual unfolding.
- New research directions: The concept of the Latent Camera could be theoretically extended into a concept of the Latent Pipeline. A camera's mode of seeing is concealed not only within its lenses and sensors but also within the algorithmic processing rules that determine the final form of an image.
- Further artistic experiments: The same RAW data could be processed through different imaging pipelines, with each resulting image subsequently interpreted by a machine vision model. Comparing whether the model's semantic judgements change according to different imaging methods could constitute both a photographic artwork and a machine vision experiment.
5 · Form (Reading the Paper as a Genre)
- Overall length: 13 pages, with official journal pagination from 1153 to 1165.
- Structural characteristics: The paper begins with a specific case of machine vision misrecognition, proceeds to epistemological discussions of photography and analyses of optical technologies and photographic practices, and ultimately returns to its original theoretical questions through dataset analysis and classifier experiments.
- First appearance of the contribution claim: The abstract introduces the implied optical perspective. The Introduction subsequently extends the research problem from data annotation biases to photography as a medium.
- Technical description vs. analysis: Theoretical analysis occupies a significant position. The purpose of the technical experiments is not merely to achieve classification performance but to operationalise theoretical propositions.
- Approach to related work: Related literature is embedded throughout the argument. Photographic philosophy and critical machine vision studies are not presented as two separate literature reviews; instead, they jointly participate in constructing the research problem.
- How the process is evidenced: The authors establish a chain of evidence connecting theory and experimentation through recognition examples from the BBC programme, distributions of photographic parameters, neural network architectures, and classification results.
- Figures: Figs. 1–3 present examples of machine vision recognition. Figs. 5–7 examine the distribution and combinations of photographic parameters. Figs. 8–9 present classifier training samples and network architecture. Subsequent images compare different optical imaging conditions and modes of machine recognition.
- Person and tense: The first-person plural articulates the authors' research positions and theoretical claims, while the past tense is employed to describe completed data analyses and experiments.
- Limitations: The classifier is positioned as a preliminary proof of concept rather than a mature, general-purpose visual analysis system. The authors identify opportunities for expanding datasets, improving training methods, and investigating additional photographic parameters.
6 · Venue Signal
This paper published in AI & Society demonstrates an effective approach to integrating technological research with humanities-based theory. Technical experiments do not constitute engineering achievements independent of theory; instead, they serve as methods for investigating, developing, and materialising theoretical questions.

Its writing conventions differ from those of both SIGGRAPH demonstration papers and empirical CHI studies.

The central contribution lies in redefining the object of machine vision research: investigating not only what machines see but also the media through which they see.

This structure is particularly relevant to the future development of my photographic media research.
7 · Take-home
- What I learned: Technical photographic parameters can become objects of media-theoretical and epistemological investigation.
- What was new to me: The concept of the Latent Camera establishes a direct relationship between machine vision and the history of photographic optics.
- What I can apply to my research: Developing a theoretical framework of the Latent Pipeline to investigate how algorithmic imaging determines the modes of visual existence of photographs.
- Whether the structure is worth emulating: Highly recommended. The paper integrates photographic philosophy, media archaeology, technological mechanisms, and practical experiments within a single argumentative structure. This approach closely corresponds to my disciplinary background and doctoral research methodology.
8 · Quotable (Verbatim, with Page Numbers)
- p. 1162: “a machine that tells us about the becoming of images; not only what they depict but how.”

This statement is particularly relevant to my research: photographic research should investigate not only what a photograph depicts, but also how a photograph becomes a photograph.

Comparative Reflection: Relevance to My Own Research
Dimension	Paper 1	Paper 2	Paper 3
Research focus	Remembering	Sensory experience	Imaging mechanisms
Research genre	Qualitative HCI research	Practice-based creative research	Critical technological research
Key theoretical concept	Felt Memory	Synthetic Memory	Latent Camera
Forms of evidence	User interviews and photographic images	Tangible installation and system implementation	Theory, data, and experiments
Application to my research	Memory sovereignty	Cross-modal photographic transformation	Image becoming and non-finality
Publication venue	CHI	NeurIPS Creative AI	AI & Society

Together, these three papers provide complementary methodological perspectives for my doctoral research.

The first demonstrates how subjective photographic experiences can be investigated through empirical user research. The second illustrates how abstract concepts concerning memory and perception can be materialised through artistic systems and multimodal interaction. The third establishes a theoretical and technological framework for investigating the mechanisms through which photographic images are produced.

Rather than treating photography exclusively as a completed visual representation, these papers collectively suggest the possibility of understanding photography as an ongoing process of technological mediation, sensory transformation, and subjective reconstruction.

This perspective provides a foundation for further developing my research into the locus of photographic existence, the non-finality of photographic images, and the relationship between imaging processes and personal memory.
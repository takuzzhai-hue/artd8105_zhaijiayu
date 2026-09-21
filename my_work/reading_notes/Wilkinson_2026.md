Reading Notes on Flashover: Spatial Storytelling of Wildfire from Memory to Spatial Experience

Wilkinson, Walton, Jeong & Rhee (University of Melbourne), SIGGRAPH Spatial Storytelling ’26. DOI: 10.1145/3799822.3812458

1 · Why I Read This Paper

This paper translates documentary memories of disaster—the 2019–20 Australian “Black Summer” bushfires—into a navigable spatial experience for wearable devices through photogrammetry, point clouds, and 3D Gaussian Splatting (3DGS). As a practice-based paper, it establishes a clear trajectory from photographic material → volumetric imagery → embodied viewing.

It is directly relevant to my research on image phenomenology and the perceptual logic of the “molecular” and the “porous” (discussed below). It also provides a useful example of how practice-based venues structure and articulate research, offering a point of comparison with writing conventions outside journals such as JVC and Visual Studies.

2 · Summary
What the project is about:
Flashover is a spatial storytelling project that addresses the experience, memory, and repeated destruction associated with wildfire. It translates an earlier large-scale multi-screen / LED-volume installation—exhibited for ten days at the VCA LED Volume Studio and visited by more than 1,700 people—into an XR framework that can be interactively navigated using an HMD. Central to the work is a firefighter’s perspective, through which the landscape is treated not as a background but as a spatial narrative environment constructed from point clouds.
Main contributions:
(1) A content-production pipeline moving from expanded landscape photography → photogrammetry → point-cloud compositing → 3DGS → Unity XR (Fig. 2);
(2) the transformation of an originally site-specific installation into a portable HMD experience, while attempting to preserve its sense of scale, fragmentation, and “molecular” vision;
(3) a point-cloud aesthetic that merges humans, animals, and environments through overlapping and variably scaled splats, resisting the visual closure of conventional portraiture and landscape imagery.
What problem does it address, and why does it matter?
Conventional media representations of wildfire often rely on cinematic tropes of heroes, villains, and spectacle. The authors argue that these visual conventions can dull the traumatic reality of a “flashover”—a sudden transition in which accumulated heat causes near-simultaneous ignition and rapidly engulfs an environment. The challenge is therefore threefold: to hold traumatic memory, to encourage renewed reflection on the climate crisis, and to allow a site-specific work to survive beyond the duration of its original exhibition.

Innovation and benefits:
Rather than treating 3DGS and point clouds simply as reconstruction technologies, the project employs them as aesthetic strategies for shaping attention, scale, fragmentation, and spatial distance. The point cloud renders entities through similarly sized visual units, making them visible with a certain indifference. In the context of wildfire, life is reduced to combustible matter—to homogeneous carbon fuel. From this emerges an alternative perceptual logic that the authors describe as “molecular vision.”

The partial and porous qualities of the point clouds—their fragmentation and coarse spatial distribution—also demand active perception: forms are not fully given in advance but instead emerge and dissolve according to the viewer’s movement, distance, and proximity.

What does it advance?
In contrast to conventional uses of 3DGS that prioritize photorealistic reconstruction, Flashover deliberately exploits the imperfections, porosity, and abstraction produced by its image-based reconstruction tendencies. The project also makes several technical adaptations: decoupling point size from depth scaling, readjusting transparency and blending parameters, and developing custom shaders that turn the covariance scale of individual splats into an interactive visual property. These modifications allow the experience to shift in real time between volumetric reconstruction and particulate abstraction.
3 · Critical Reflections

The authors acknowledge several limitations: performance and visual consistency still require optimization; visual cues and navigational behaviors need further development; and the XR scenes require greater structural complexity. Beyond these stated limitations, I see several additional issues:

There is no evaluation.
The paper mentions more than 1,700 visitors and interviews with firefighters, yet provides no evidence concerning audience experience, embodied effects, or whether “molecular vision” actually generates new forms of reflection. The paper largely consists of authorial accounts of intention and aesthetic claims. Statements that the work “encourages active perception” or “holds traumatic memory” remain assertions rather than findings.
A questionable assumption:
The “molecular vision” that reduces living beings to homogeneous carbon fuel is framed simultaneously as a critical revelation—the indiscriminate perspective of fire—and as an ethical means of holding traumatic memory. There is a tension between these two positions. Could aesthetic homogenization and abstraction dilute traumatic experience rather than respect it? The authors do not address this contradiction, which recalls the longstanding problem of the aestheticization of disaster.
The cost of portability is not quantified.
The original material consists of a 12-minute, 6K sequence containing approximately 130 million points, which had to be substantially reduced to run on an HMD. What exactly is lost in this translation? The claim that the XR version “preserves” scale and fragmentation remains qualitative and is not supported by a systematic comparison.
Firefighter agency:
Interview materials are used to generate environments and are projected onto LED walls, but it is unclear whether the participants had any right to reject, revise, or participate in shaping their final representation. This point connects directly to my idea of memory sovereignty, particularly the possibility of “refusable” or vetoable intelligent memory. Flashover lacks this layer of participant agency.
Scalability:
The pipeline depends heavily on RealityCapture, manual point-cloud refinement, and scene-by-scene shader adjustment. It is therefore fundamentally an artist-intensive, handcrafted workflow rather than a readily scalable system. This is not necessarily a problem for a practice-based artwork, but it weakens the argument when the workflow itself is presented as a significant pipeline contribution.
4 · Creative Reflections
A new idea prompted by the paper:
“Molecular vision” is compelling as a non-anthropocentric perceptual apparatus. It could be connected to my discussion of shashin, the nonhuman eye, and machine vision. The point cloud’s “indifference” toward what it renders can itself be understood as a photographic-ontological proposition, allowing the camera’s eye, the fire’s eye, and the algorithmic eye to be placed alongside one another.
Methodological transfer:
The same logic—porous point clouds requiring active perception—could be applied to personal memory and family imagery rather than disaster. Private photographs could be reconstructed as navigable point-cloud environments whose forms appear and disappear according to the viewer’s movement. This directly connects to my concept of a memory-sovereignty camera: the emergence and dissolution of form could become an experiential model of memory accessibility and forgetting.
A different approach to the same problem:
Their strategy can be described as “defect as aesthetic.” Another approach would be to work through temporality. Rather than creating a static point-cloud environment, splats could gradually degrade, erode, or weather according to viewing duration, turning “repeated destruction” into an experience rather than merely a representation. Alternatively, embodied physiological feedback, such as heart rate or breathing, could drive the behavior of the fire, shifting trauma from a primarily visual register toward bodily experience.
A direction worth developing:
The use of 3DGS covariance as a performable visual property seems particularly underexplored. Statistical parameters within point-cloud representation could be treated as performative and narrative variables rather than merely technical parameters. This possibility may be substantial enough to support a separate theoretical paper.
5 · Form: Reading the Paper as a Genre
Length of main text (excluding references): approximately 3 pages, with slightly over 2 pages of continuous main text.

Approximate distribution by section:
Introduction ~12% / Spatial Design & Point-based Landscape ~28% / Volumetric Portraits ~12% / XR Framework ~22% / Demo ~10% / Conclusion ~10% / Acknowledgements + References ~6%.

The technical pipeline and aesthetic discussion dominate the paper, while relatively little space is devoted to the demo itself.

Where the contribution claim first appears:
The first contribution claim appears in the final part of the Introduction. A clearer statement of the contribution—the translation of the work into a portable XR format—appears in the overview of §2 under “Spatial storytelling contribution,” around the second paragraph of page 2.
Contribution statement, verbatim:
“For the SIGGRAPH Spatial Storytelling demonstration, we translate Flashover into an interactive XR framework that preserves its spatial structure, volumetric assets, and embodied mode of engagement while enabling real-time interaction with point-cloud data and navigation through the environment.”
Description vs. analysis:
Descriptions of the work and production process occupy most of the paper: how the point clouds were produced, how the shaders were adjusted, and how the installation was exhibited. Analytical and theoretical ideas such as “molecular vision” and “active perception” appear intermittently rather than forming a systematic theoretical argument.
Approach to related work:
The paper neither provides a conventional literature survey nor constructs a research “gap.” In fact, there is almost no related-work section. The bibliography contains only six references, most of which concern technical sources such as 3DGS and UnityGaussianSplatting, or contextual material related to wildfire ecology and reporting. There is little attempt to establish a broader scholarly genealogy. This is characteristic of the practice-based/demo paper format.
How the process is evidenced:
Evidence is provided primarily through images—Fig. 1, a six-panel presentation of the work, and Fig. 2, a production-pipeline diagram—and through technical description. There are no quoted logs or systematic quantitative metrics, apart from scale-related figures such as “130M points,” “12 minutes,” “6K,” “10 days,” and “1,700 visitors.”
Figures:
There are two figures. Fig. 1 consists of six images showing the installation panorama, volumetric portraiture, point-cloud landscape, fire vortex, point-cloud forest, and XR headset use. Its function is to establish the work’s credibility and aesthetic language. Fig. 2 presents the four-stage production pipeline and therefore carries much of the methodological explanation. Together, the figures perform a substantial portion of the paper’s evidentiary work.
Person and tense:
Usage is mixed. The history and production of the artwork are generally described using the passive voice and past tense (“was configured,” “were produced”), while the demo contribution is articulated through the first-person plural and present tense (“we translate,” “we present”).
Limitations:
Limitations are present but extremely brief. They are integrated into the final two sentences of the Conclusion (“while current implementation…future work will…”), occupying less than 10% of the paper. They address technical optimization only, leaving ethical questions and evaluation unexamined.
6 · Venue Signals

The acceptance of this paper by SIGGRAPH Spatial Storytelling suggests that the venue values live-demonstrable technical–aesthetic works supported by a clear production pipeline, without necessarily requiring extensive evaluation, theoretical dialogue, or a developed related-work genealogy.

The contribution can therefore take the form of an engineering–creative translation, such as adapting or reconfiguring an existing artwork into a new immersive format. Visual evidence carries considerably more weight than extended textual argumentation.

This constitutes a very different writing contract from theory-oriented journals such as October or Screen, where sustained theoretical construction and scholarly positioning are generally much more central.

7 · Take-Home Points
What I learned:
The “defects” of 3DGS—porosity, fragmentation, and image-like collapse—can be systematically treated as aesthetic and phenomenological tools, rather than errors that need to be eliminated. Covariance, in particular, can become an interactive narrative variable.
What was new to me:
The concept of “molecular vision”—the eye of fire perceiving everything as homogeneous fuel—offers an interesting way of ethicalizing and phenomenologizing the apparent indifference of the photographic or machine eye.
How it can inform my own research:
The language of forms emerging and dissolving through active perception can be directly connected to my framework of memory sovereignty, where the accessibility and disappearance of form can model the accessibility and forgetting of memory. My own research could also introduce the layer that Flashover lacks: the agency of the person whose memory or testimony is being represented.

Is its structure worth imitating?
As a model for an October or JVC submission: no. It contains little theoretical development or evaluation, and almost no engagement with related scholarship.
As a model for SIGGRAPH or another practice-based/demo venue: yes. It demonstrates how minimal text, strong visual material, a clear pipeline, and intention-driven aesthetic discourse can function effectively within this genre.

I would therefore use it as a genre comparison, rather than as a model of scholarly argumentation.

8 · Quotable Passages (Verbatim, with Page Numbers)
p. 1 (Introduction):
“familiar visual tropes risk dulling the intense lived experience of a flashover … instead of cinematic spectacle with heroes and villains, the work aims to use spatial and visual storytelling to hold traumatic memory while inviting renewed reflection on the broader impacts of the climate crisis.”
p. 2 (§2):
“To wildfire, we are all made of the same stuff and are ‘seen’ with the same indifference: molecular fuel. … this ‘molecular’ vision introduces an alternative perceptual logic and opens a space for renewed contemplation.”
p. 2 (§2):
“the partial, porous nature of the point clouds — fragmented and coarsely distributed through 3DGS training — encourages active perception: forms are not readily given, but emerge and dissolve through movement and proximity.”
p. 3 (§3):
“Person, place, and event smear into one another, resisting the closure of conventional portraiture and aligning with the project’s broader meditation on trauma and memory.”

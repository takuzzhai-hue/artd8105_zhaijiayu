Embodied Visions: Interactive Installations That Reimagine Bodily Presence in Digital Imaging Apparatuses as Shadows

1 · Why This Paper

This paper builds directly on the media archaeology developed in Jonathan Crary’s Techniques of the Observer. Taking the shadow as an index or surrogate of the body, it critiques the disembodying tendency of digital imaging, in which the viewer’s physical body is increasingly removed from the imaging process.

The project consists of three installations. What makes it particularly useful is the way it translates a theoretical argument into a progressive sequence of embodied experiences, allowing the same conceptual problem to be examined through three different technical and perceptual configurations.

2 · Summary

Theme:
Embodied Visions consists of three interactive installations using cameras, projectors, and machine vision to reinsert the viewer’s body into the pipeline of digital imaging and display. Using the shadow as its central metaphor, the project attempts to resist the disembodying tendency of contemporary digital imaging.

Research Question and Significance:
Following Crary, the authors argue that nineteenth-century optical devices such as the stereoscope began a historical process in which vision was increasingly detached from the observer’s physical body and relocated into technical systems and screens. In the age of VR and digital photography, the body has become almost entirely absent from the dominant model of imaging, reducing the viewer to a passive receiver.

The central question is therefore: Can we design an imaging system today in which the physical presence of the viewer becomes relevant again?

The authors also draw on the myth of Dibutades in Western media archaeology, in which the traced shadow functions as a surrogate and visual proxy for the body.

Method / Innovation — Three Progressive Installations:

Disembodied Imaging
The viewer first sees a real-time segmented silhouette of their own body. After several seconds, the system uses MediaPipe Pose to match their pose with archived video footage of previous visitors. The silhouette gradually and almost imperceptibly “becomes someone else” and stops following the viewer’s actual movements. The installation exposes the unreliability and disembodied nature of digital images.
Embodied Imaging
Three projectors produce images that appear individually as meaningless “noise.” Only when the viewer blocks one of the projectors with their body does a meaningful image become visible inside their own cast shadow. This is achieved through planar homography and video decomposition. Here, the viewer’s physical body becomes part of the display pipeline itself.
Multi-body Imaging
Two viewers are separated by a wall and can initially see only each other’s silhouettes. They must cooperate by matching each other’s poses. Once their poses match, the wall appears to become transparent, allowing them to see one another. Bodily presence thus becomes a medium for interpersonal connection.

Key Contribution Claimed by the Authors:
The project attempts to transform the passive viewer into an active observer who can control and produce visual effects. By contrasting “optical shadows” with “computational shadows,” it also reveals a gap between machine perception and human perception: MediaPipe recognizes poses rather than particular embodied individuals, whereas in the myth of Dibutades, the shadow is inseparable from a specific body and its emotional significance.

The authors further claim that the installations can increase bodily awareness, awareness of shared public space, and interpersonal empathy.

Development Beyond Previous Works:
Artists such as Olafur Eliasson, Rafael Lozano-Hemmer, and Joon Moon have also used projection and shadows to explore bodily co-presence. However, according to the authors, these works generally take existing optical and digital imaging pipelines as given conditions. Embodied Visions, by contrast, attempts to critique and reconstruct the imaging pipeline itself.

The project was evaluated during a four-day exhibition with 31 visitors. Twenty-eight participants completed background questionnaires and interviews. Table 1 reports participants’ self-assessed familiarity across four professional or technical areas.

3 · Critical Thinking
The diagnosis of “disembodiment” is quietly contradicted by the project’s own implementation.
All three installations depend heavily on MediaPipe Pose, a system that compresses the body into a vector of skeletal keypoints. In other words, while the authors claim to “write the body back into imaging,” what actually enters the computational system is an abstracted pose representation. This could itself be understood as another form of abstraction or detachment in Crary’s sense: the body does not enter the system primarily as material presence, but as computable bodily data. The project partially acknowledges this contradiction in Installation #1, where computational abstraction becomes an object of critique, but it does not fully recognize that the “embodiment” of the later installations remains dependent on related forms of computational representation.

The shadow here is not always an index; in some cases, it is a simulated index.
A physical shadow is an optical index: the body blocks light, producing a direct causal trace in the here and now. However, the “shadows” in Installations #1 and #3 are computational silhouettes produced through machine vision, whereas Installation #2 involves an actual optical shadow. The paper nevertheless places all three under the same concept of “shadow” and unifies them through the myth of Dibutades.

This creates an important conceptual problem: a computational shadow is not necessarily an index of the body; it is a model’s inference about the body. Dibutades traces an actual projection produced through physical contact with a light path. The project therefore uses a myth grounded in indexicality to support technologies that may no longer be indexical in the same sense. Installation #1, in which one person’s shadow can become someone else’s, could have developed this issue much further. Instead, the authors mainly frame it as evidence of the unreliability of digital images rather than as a fundamental problem of indexicality.

Only Installation #2 fully delivers on the project’s central claim.
Strictly speaking, Installation #2 is the only work that genuinely incorporates the viewer’s physical presence into the imaging process, because the viewer’s body actually interrupts the path of light. Installation #1 demonstrates disembodiment rather than overcoming it, while in Installation #3 the body primarily functions as an input signal or collaborative trigger; the displayed image does not maintain a direct causal relationship with bodily presence.

The three works are presented as a progressive movement toward embodiment, but the strongest form of embodiment actually occurs in the middle installation. The other two remain much closer to the computational logic that the project claims to critique. This internal inconsistency is not sufficiently acknowledged.

The evaluation is suggestive and lacks a control condition.
The authors explicitly state that the installations were intentionally designed to feel eerie or unexpected, encouraging viewers to gradually recognize that something was wrong. They then cite responses such as participants being “positively shocked” when the shadows violated their expectations. Yet these reactions are partly produced by the design itself, making them weak evidence for the broader theoretical claims.

Table 1 reports only participants’ self-assessed background knowledge, with relatively low averages in areas such as computer vision/imaging (2.46) and digital art (2.78). It does not provide quantitative measurements of the actual effects of the installations. Claims that the project increases bodily awareness or empathy therefore remain largely anecdotal and are not tested against a control condition. The paper also does not sufficiently explain the difference between the 31 exhibition visitors and the 28 participants included in the questionnaire/interview data.

The cultural assumptions behind the argument remain unexamined — particularly relevant to my own research direction.
The paper’s theoretical framework—Crary combined with the myth of Dibutades—is rooted almost entirely in a Western genealogy of visuality. It treats the idea of the shadow as a surrogate for the body as if it were broadly applicable to human perception. However, relationships between shadow, body, image, and representation may operate differently across visual cultures. East Asian concepts of shadow/image (影), form (形), and light, for example, do not necessarily follow the Dibutades logic of tracing a contour as a means of capturing or possessing a bodily surrogate.

The paper therefore risks universalizing a culturally specific history of visuality into a general theory of “human perception.” This unexamined universalization is particularly striking because media archaeology itself should remain attentive to the historical and cultural specificity of media formations.

4 · Creative Thinking
Turn “the computational shadow is not an index” into the central subject of an artwork.
The moment in Installation #1 when the viewer’s shadow becomes someone else’s is arguably the sharpest conceptual point in the entire project. It could be expanded into an independent work in which viewers directly experience their bodies being replaced, misrecognized, or reassigned by a computational model. The central question would then become: What exactly does the machine recognize when it claims to recognize “me”? This would bring the problem of the “non-indexical pseudo-shadow” from a hidden implication to the explicit conceptual center of the work.
Transfer this distinction into my own research.
The contrast between optical shadow and computational shadow could be transferred to my research on shashin and embodiment. Rather than using MediaPipe to abstract the body into skeletal data, I could allow actual optical traces—real obstruction of light, real exposure, and singular physical events—to drive the image. A mechanism similar to Installation #2, in which an image becomes visible only through the physical presence of a body, could provide a concrete way to address indexicality, embodiment, and irreproducibility.
7 · Take-home

What I learned:
The paper demonstrates how an abstract theoretical proposition—Crary’s account of the disembodiment of the observer—can be translated into three experiential installations, each addressing a different sub-question: disembodiment, embodiment, and multi-body interaction. This structure of using a group of artworks to progressively develop and test a theoretical argument is particularly useful for practice-based research.

What was new/useful for me:
Installation #2 uses three projectors, planar homography, and video decomposition to create an image that becomes visible only within the viewer’s shadow. This offers a concrete technical model for making physical bodily obstruction a condition of image appearance, which is directly relevant to installation practices concerned with indexicality.

As a model for academic writing:
This is a useful example of a paper that combines a strong theoretical framework with clear technical implementation: it moves from Crary to three progressively structured installations, explains technical mechanisms such as homography in reproducible detail, and concludes with an audience evaluation.

Its overall structure—theory → progressive installations → technical implementation → evaluation—is highly adaptable to practice-based research publications.

However, the evaluation remains weak and partly suggestive, while the paper does not critically examine its central metaphor of the shadow as index. In a more theoretically demanding venue such as October, Screen, or Visual Studies, a likely question would be: On what grounds can a computational shadow be treated as an index of the body?

The paper is therefore particularly valuable as a model for connecting theoretical argument with technical practice, but its central conceptual metaphor would require much more rigorous critical examination.

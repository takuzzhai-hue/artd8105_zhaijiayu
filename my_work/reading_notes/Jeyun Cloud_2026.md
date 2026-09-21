Reading Notes on Are We Gazing at the Same Moon?

Jeyun Cloud & Ziqian Yin (Los Angeles). SIGGRAPH Art Gallery ’26. DOI: 10.1145/3799824.3812689

1 · Why I Read This Paper

This work uses an image shared by almost everyone—the Moon—as a testing ground for the question of whether a “consensual image” can truly exist.

The project reverses the Lunar Mosaic technique used in astronomical photography. Instead of stitching multiple lunar images together to produce a single high-resolution representation, it fragments a single archival image of the Moon and uses generative AI to independently out-paint each segment, allowing every fragment to develop into a different imagined planet.

This directly connects to my interests in image phenomenology, particularly the mediation of vision and the destabilization of the photographic “that-has-been,” as well as media archaeology, through its reversal of an established imaging technique. Its tension between individual and collective memory also parallels the questions underlying my framework of memory sovereignty.

Read alongside Flashover and A Walled City, it also provides a useful third example for comparing different SIGGRAPH venue conventions.

2 · Summary

What the project is about:
The artwork constructs a kind of moon-gazing ritual, reimagining the Moon as an entity that coexists across parallel realities and questioning the relationship between individual and collective memory.

Its central method is to reverse the logic of the “Lunar Mosaic.” Rather than combining photographs taken at different times or depicting different areas into a single high-resolution composite image of the Moon, the artists begin with a single archival lunar image captured by NASA’s Galileo spacecraft in 1992. They divide this image into fragments and use a diffusion model to independently out-paint each fragment beyond its original boundaries.

The recomposed result therefore no longer represents different moments or sections of one Moon, but instead becomes a mosaic of multiple coexisting moons.

The project is presented across several media, including audiovisual work, sculpture, and public installation.

Main contributions / innovations:
(1) A conceptual operation of reversed stitching. An astronomical imaging technique originally designed to construct a singular, unified celestial body is inverted so that the geological, lighting, and spatial logics of individual fragments become mutually incompatible. The relationship between part and whole, and between individual perception and collective reference, consequently dissolves into an irreconcilable mosaic.

(2) Two technical strategies: image dislocation and timeline operation.

In image dislocation, each lunar fragment is treated as part of an independently imagined planet. The diffusion model receives only that individual fragment as its conditioning input, with no contextual information shared between adjacent segments. The generated terrains therefore diverge from one another.

In timeline operation, AI-generated depth data is used to extrude the lunar surface into a 3D form through which a virtual camera performs a fly-through. The first and final frames are then selected and passed through image-to-video generation to create multiple variants of parallel timelines. These are subsequently recombined, producing a continuous journey across parallel realities in which temporal paths repeatedly diverge and reconverge.

What problem does it address, and why does it matter?
The Moon has long functioned as a symbol of shared human experience: a familiar presence connecting people across geographical distance, historical periods, and cultural contexts.

Yet individual perceptions of the Moon are always mediated by personal memory, cultural context, and conditions of observation. The project therefore questions both the authenticity of lunar imagery and the assumption of a genuinely shared experience of moon-gazing: are we, in fact, looking at the same Moon?

What does it advance?
The work reformulates, through generative AI, a longstanding problem that extends across Cubism, panography, and contemporary computational imaging: how can multiplicity be represented within a single visual field?

Cubism combined incompatible viewpoints, while panography assembled multiple exposures. In this work, however, a single source image is fragmented through independent AI sampling processes, causing one ostensibly unified subject to proliferate into multiple incompatible versions.

On the temporal level, the branching timelines generated through image-to-video make visible a condition of collective experience that is shared in principle but irreconcilable in practice.

3 · Critical Reflections

The paper contains no dedicated limitations section and acknowledges almost no explicit limitations. I see several significant issues:

Extremely thin, with almost no evaluation:
The substantive text occupies approximately two pages—the remaining pages in the four-page layout contain little or no content. There is no audience study, exhibition documentation, or evaluation of the generated results.

The paper consists almost entirely of conceptual statements and descriptions of technique, making it closer to a lightweight artist statement than a conventional research paper.

A gap between the conceptual claim and its execution:
The central question—“Are we gazing at the same Moon?”—concerns differences between viewers, particularly the relationship between individual and collective perception.

Yet the technical implementation produces variation entirely within the image itself, through divergent AI out-painting. The viewer’s position, perceptual conditions, and participation in the proposed “ritual” are almost entirely absent.

In other words, the project demonstrates that AI can generate many different moons from one lunar image, but it does not substantially engage with the actual problem of gazing: who is looking, how their ways of looking differ, and where those differences originate.

The conceptual proposition is stated, but not fully enacted through the method.

Limited technical novelty:
Out-painting, image-to-video generation, and depth-to-3D reconstruction are all existing techniques assembled relatively directly.

The reversal of Lunar Mosaic provides an elegant conceptual framework, but there is little methodological innovation at the technical level. The paper also provides almost no information about models, parameters, implementation decisions, or failed outputs.

Thin theoretical grounding:
The paper invokes Cubism, panography, NASA imagery, individual memory, collective memory, and authenticity, but provides almost no scholarly grounding for these humanistic claims. Its bibliography contains only one reference, to the NASA image archive.

In comparison with A Walled City, which explicitly engages Deleuze, Latour, Tsing, and Novak, the theoretical framework here remains extremely underdeveloped.

“Irreconcilability” is a designed outcome rather than a finding:
Because each fragment is deliberately generated without neighboring context and through independent sampling, divergence between the resulting terrains is structurally inevitable.

The paper nevertheless interprets this technically predetermined result as a broader philosophical statement about collective experience. There is therefore a risk of over-interpreting an artifact of the system’s design as a philosophical discovery.

4 · Creative Reflections

A new idea prompted by the paper:
The act of reversing an established imaging technique is itself an extremely transferable creative methodology—a form of media-archaeological reverse-engineering aesthetics.

Any imaging technology designed to produce unity, seamlessness, or higher fidelity could potentially be reversed: HDR compositing, panoramic stitching, super-resolution, multi-frame noise reduction, and similar techniques.

Instead of hiding seams and inconsistencies, such works could expose the assumptions underlying acts of computational stitching and reveal that the unity of an image is itself technically produced.

This methodological principle could be particularly useful for my research on machine vision and the ontology of shashin.

Methodological transfer to my own research:
The same operation of single source → independent sampling → divergence could be applied to personal and family photographs.

A family photograph could be divided into fragments, with each fragment independently expanded into an incompatible version of the remembered event. This would provide a visual model for the proposition that memory does not constitute a single, stable truth, connecting directly to the idea of memory sovereignty and the possibility of multiple retellings of memory.

A different approach to the same problem:
In this project, it is the image that diverges. A method that more fully responds to the title would instead make the viewer a variable.

For example, oral accounts, photographs, or descriptions of the Moon collected from people in different regions and cultural contexts could be used as conditioning inputs for different lunar fragments. The resulting “different moons” would then genuinely emerge from different people and situated modes of perception, rather than from stochastic model sampling.

This would move “gazing” from the level of rhetoric into the structure of the data itself.

A direction worth developing:
The trajectory from Cubism → panography → generative AI could be developed into a media-archaeological genealogy of technologies for representing multiplicity within a single visual field.

The paper only gestures toward this lineage, leaving substantial room for deeper historical and theoretical investigation.

5 · Form: Reading the Paper as a Genre
Length of main text (excluding references):
Approximately two pages of substantive text. Although the paper uses a four-page layout, roughly two pages contain little or no actual content.

Approximate distribution by section:
Abstract ~10% / Introduction ~20% / §2 Process and Technique ~50% / §3 Significance ~18% / Acknowledgements + References ~2%.

Technical and process description occupies roughly half of the paper, while the theoretical and interpretive conclusion is very brief.

Where the contribution claim first appears:
The central contribution is already stated in the second and third sentences of the Abstract:

“reversing the process and expanding image segments … with generative AI, it questions the notion of a singular, unified human experience of moon-gazing.”

This proposition is expanded further at the end of the Introduction.

Contribution statement, verbatim:
“Challenging the process of ‘Lunar Mosaic’ by reversing the process and expanding image segments of the collaged moon with generative AI, it questions the notion of a singular, unified human experience of moon-gazing.”

Description vs. analysis:
Descriptions of the artwork and its techniques dominate the paper. §2 explains the two technical approaches in some detail, whereas the analytical section, §3 Significance, is short.

Its primary analytical move is to situate the work in relation to Cubism and panography rather than to develop an independent theoretical argument.

Approach to related work:
The paper neither presents a conventional related-work list nor constructs an explicit research gap. Instead, it uses a genealogical analogy, positioning Cubism and panography as historical precedents for its own treatment of multiplicity.

There are no scholarly citations supporting this genealogy; the only reference is the NASA image archive. This structure is closer to the conventions of an artist statement than a research paper.

How the process is evidenced:
The process is supported almost entirely by two figures.

Fig. 1 presents a panoramic installation of the reconstructed moons, including the silhouette of a viewer, and establishes the work’s physical scale and aesthetic atmosphere.

Fig. 2 is a four-stage process diagram showing the original lunar image → segmented out-painting → recomposed lunar group → partially scaled mosaic. It carries almost the entire burden of methodological explanation.

The figures therefore perform nearly all of the paper’s evidentiary work. The text contains no quantitative metrics, system logs, or evaluation data.

Figures:
Two figures: one atmospheric image of the completed work and one four-stage process diagram.

Person and tense:
Usage is mixed. Descriptions of the artwork alternate between the past tense (“The artwork established…”) and the present tense (“The work explores…,” “The piece operates…”).

Technical descriptions generally use the present tense. First-person plural is not dominant, appearing only occasionally in phrases such as “We tested” and “we select.”

Limitations:
Entirely absent.
6 · Venue Signals

The acceptance of this work into the SIGGRAPH Art Gallery, as distinct from the Spatial Storytelling and CGIT Art Papers venues represented by the previous two papers, suggests that this track places particular value on a compelling conceptual translation + a visually strong finished artwork + presentation across multiple media.

Its expectations concerning length, evaluation, theoretical dialogue, and related work appear substantially lighter. In practice, the paper functions largely as a two-page artist statement accompanying an exhibited artwork.

Taken together, the three papers suggest a useful spectrum of writing expectations:

Art Gallery — concept + artwork statement
→ Spatial Storytelling — concept + artwork + technical pipeline
→ CGIT Art Papers — concept + system + related-work gap + theoretical framing

This comparison is particularly useful when deciding which track to submit to and how much scholarly argumentation the submission needs to carry.

7 · Take-Home Points

What I learned:
The paper demonstrates the strength of “reversing an existing imaging technique” as a conceptual engine: a creative proposition that can be communicated in a single sentence yet generate an entire artwork.

It also demonstrates how a universally recognizable object such as the Moon can make an abstract question—whether a consensual image can exist—immediately perceptible.

What was new to me:
The treatment of astronomical Lunar Mosaic as a technological-historical object that can be reversed provides a particularly clean example of a media-archaeological creative operation.

How it can inform my own research:
(a) The proposition that the unity of an image is produced through acts of stitching can contribute directly to my argument concerning shashin and machine vision.

(b) The work also reveals a methodological mismatch between a proposition located in the viewer and an implementation located in the image.

This is especially important for my work on memory sovereignty: if the research concerns differences in memory, interpretation, or agency, those differences should genuinely originate from participants or viewers, rather than being simulated through model randomness.

This can become a methodological principle in its own right.

Is its structure worth imitating?
As a template for an Art Gallery statement: yes. It demonstrates an extremely compact structure—Abstract → Introduction → Process → Significance—that can communicate a work effectively within approximately two pages.

As a model for JVC, October, or CGIT: no. It contains no evaluation, almost no theoretical dialogue, and virtually no bibliography.

Its primary value is therefore as a lower-bound example of how concise a practice-based artwork statement can be, rather than as a model for sustained academic argumentation.

8 · Quotable Passages (Verbatim, with Page/Section)
p. 1 (Abstract):
“Are We Gazing at the Same Moon? Do we observe reality within the same time and space?”
p. 1 (§1 Introduction):
“individual perception of it is mediated by personal memory, cultural context, and the conditions of observation.”
p. 2 (§2 Process and Technique):
“The recomposed scene reads as a mosaic of co-existing moons rather than one body sampled at different times.”
p. 2 (§3 Significance):
“Where Cubism composited incompatible viewpoints and panography composited multiple exposures, this project fragments its subject by generating it through independent AI sampling processes applied to a single source.”
p. 2 (§3 Significance):
“The dual movement of divergence and convergence models the condition of collective experience: shared in principle, irreconcilable in practice.”

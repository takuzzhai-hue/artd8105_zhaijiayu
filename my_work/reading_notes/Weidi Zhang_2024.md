# Reading Notes: ReCollection: Creating Synthetic Memories with AI in an Interactive Art Installation

Weidi Zhang (Arizona State University), Lijiaozi Cheng (University of Sheffield), and Jieliang Luo (Autodesk Research). Proceedings of the ACM on Computer Graphics and Interactive Techniques (PACM CGIT), 7(4), Article 51, August 2024. DOI: 10.1145/3664207

## Why · Why Read This Paper?

There are three main reasons.

First, the authors are the same research team behind A Walled City (Zhang, Cheng, and Luo), which you have already examined. ReCollection is an earlier and more personal project, originating from the experience of witnessing the deterioration of the author's grandmother's memory due to dementia. It uses generative AI to reweave memories that have been taken away by time and illness.

Reading these two projects together makes it possible to trace the evolution of the artists' methodology, from individual memories to collective digital monuments.

Second, the project directly addresses a central tension within your research on latent images, latency, and the historical transformation of structures of delay: the dissolution of the boundary between remembrance and imagination.

AI automatically completes fragmented linguistic memories into coherent narratives. This process can be understood as a generative movement from latency and fragmentation toward development and completion.

Third, the installation shares a remarkably similar physical configuration with your proposed installation for the 2027 Venice exhibition's Macao Pavilion:

LED displays + microphone pedestal + darkroom-like immersive environment + soundscapes created through granular synthesis of urban recordings.

It therefore offers an almost directly applicable exhibition reference.

Its citation network connects Rosi Braidotti's nomadic subjectivity, Seymour Chatman's narratology, critical dementia studies (particularly Jenkins's concept of the inter-embodied self as montage), George Legrady's Pockets Full of Memories, and John Twomey's Not Not.

## D · Description / Summary

### Origins and Design Questions

The project originated from the author's experience of watching her grandmother's cherished stories gradually dissolve into fragmented words as a result of dementia.

The emergence of text-to-image AI in 2022 offered a new perspective: using language to reimagine and reconstruct fragmented memories.

The authors formulate three central design questions:

1. As we coexist with machines, might we accumulate synthetic recollections through a collective, symbiotic imagination?
2. Can language reweave and synthesize visual memories?
3. How might collective memories inspire new visual forms and alternative narratives?

### The Artwork

ReCollection is an interactive AI art installation.

Participants whisper a sentence describing a personal memory into a microphone for approximately ten seconds.

The system transcribes their speech, automatically expands the fragment into a complete narrative, and generates continuously transforming synthetic memory imagery in real time.

Generation takes approximately twenty seconds.

During this interval, participants observe the visual memories contributed by previous visitors gradually fading and dissolving into their newly generated memories.

### Conceptual Framework: The Inter-Embodied Self as Montage

The project draws on a critical shift within critical dementia studies.

Rather than treating the restoration or recovery of a lost self as the primary goal, as may be associated with conventional person-centred reminiscence approaches, the authors engage with Nick Jenkins's concept of the inter-embodied self as montage.

From this perspective, the self does not require a unified and coherent narrative in order to flourish.

Instead, it can be understood as a polyphonic montage of voices and experiences that continually updates, transforms, and exists through relationships with others.

The authors also cite Anne Basting's argument that meaningful connection can emerge when expectations of remembering are replaced by freedom of imagination and shared expression.

Within this framework, AI is not positioned as a therapeutic instrument.

Rather, it becomes a non-human narrative agent participating in imaginative activity and collaborative worldmaking.

### Intelligent System (Figure 2)

The system consists of a three-component pipeline.

1\. Whisper — Speech-to-Text

Whisper converts participants' spoken memories into text and supports 98 languages.

2\. GPT-4 — Narrative Completion

GPT-4 expands the input into a coherent narrative.

The system uses a dual-agent structure:

- One agent controls narrative coherence and content.
- Another influences visual style, including cinematic composition, camera positioning, and viewing angles.

Together, they produce a written storyboard for subsequent image generation.

3\. Stable Diffusion — Text-to-Image Generation

Stable Diffusion translates the generated narrative into visual imagery.

The system also performs language-dependent cultural adaptation.

For example, Japanese input may produce Japanese faces and environments, while French input may generate cafés and croissants.

However, the authors acknowledge that such behavior can expose cultural biases embedded within large AI models.

For instance, domestic labor may be visually associated with women by default.

Rather than entirely suppressing these biases, the artists regard their visibility as material capable of stimulating public discussion.

### Artistic Decision: AI-Generated Outputs as Digital Ready-Mades

The artists deliberately avoid displaying raw AI-generated images directly.

Instead, they treat generated imagery as a form of digital ready-made, which is subsequently transformed through artistic processes.

Their visual approach draws inspiration from two historical techniques:

- Monotype printmaking, dating back to the 1640s.
- Slit-scan photography, which records sequential slices of a subject across time.

Using TouchDesigner, the team constructs a multilayered processing pipeline:

1. Convert the generated imagery into monochrome.
2. Apply Perlin noise to displace pixels along the X and Y axes.
3. Use a feedback system to track pixel displacement and introduce blurring.
4. Implement a GLSL-based particle system in which edge detection converts object boundaries into particles, while algorithms simulate turbulent motion.

Through these processes, machine-generated imagery is algorithmically dissolved, tilted, printed, and reprinted, producing continuously evolving real-time visuals.

The approach emphasizes the relationship between machinic vision and human perception.

### Interaction and Exhibition Design

The project was exhibited three times in 2023, including presentations at the SIGGRAPH Art Gallery, Signal, and the MIX Center.

The installation combines:

- A darkened exhibition environment.
- A projection surface or LED display.
- A pedestal positioned toward the projection, equipped with a microphone and USB button.
- Dim overhead spotlighting to establish an intimate atmosphere.
- A looping soundscape created by transforming urban field recordings through granular synthesis.

The work attracted more than 1,000 international visitors, who were encouraged to share memories in their native languages.

Some visitors reportedly became emotional upon encountering the generated visuals, with certain participants describing the imagery as vividly capturing details of their imagination.

The project underwent two major design iterations.

First version — SIGGRAPH

The original interface adopted a Polaroid or photo-album aesthetic, displaying framed imagery accompanied by descriptive text.

Visitors, however, sometimes perceived a disconnection between the textual descriptions and the generated images.

Second version — Signal

Inspired by the experience of gazing at one's reflection on a river surface and recognizing oneself through moving ripples, the artists redesigned the presentation.

The new interface used a circular composition and integrated text into the visual imagery.

This was intended to communicate a sense of memories being recreated, reflected, and reimagined.

### Conclusion and Future Directions

The authors argue that the intertwining of human and non-human narratives opens new possibilities for collective memory, imagination, and cultural reproduction.

Drawing on Chatman, they suggest that narrative agency should not be understood as exclusively human in an era shaped by mechanical and electronic reproduction.

The objective is not to restore fading memories but to encourage the collaborative imagination of collective memory.

Future directions include inviting people living with dementia to participate directly, since the installation has not yet been tested with this population, and extending the system into three-dimensional environments through speech-to-world generation and virtual reality.

## V · Critical Reflection

### 1. Dementia Provides the Conceptual Starting Point, Yet the Work Was Not Tested with People Living with Dementia

This is the paper's most significant tension.

Much of its theoretical foundation derives from critical dementia studies, particularly the argument that imagination should take precedence over attempts to restore or repair memory.

However, its participants were more than 1,000 general exhibition visitors, with no reported testing involving people living with dementia.

Only in the discussion of future directions do the authors acknowledge that the installation was not specifically designed for this population.

The project therefore risks drawing on the ethical and emotional weight of dementia to support a generative artwork intended primarily for general audiences.

This discrepancy deserves critical attention.

### 2. The Ethics of Synthetic Memory Remain Largely Unexamined

The system uses GPT-4 to automatically fill in missing details and complete fragmented narratives.

In other words, it applies AI-generated content to incomplete personal memories.

Within the context of dementia, this is an especially sensitive intervention.

Who has the authority to complete another person's memory? Whose memory is being produced through that completion?

This is precisely where your research could intervene.

The artwork enthusiastically embraces the movement from latency and incompleteness toward a fully developed image, yet largely avoids the question of power inherent in the act of completion.

To complete a memory is also potentially to rewrite it.

This recalls Cross's concern that materializing memory may deprive it of its movement and openness.

Here, AI-generated completion presents a comparable risk of fixing or rewriting memory through narrative closure.

### 3. Cultural Adaptation Is Both Superficial and Double-Edged

The system treats associations such as “Japanese language → Japanese faces” or “French language → cafés and croissants” as forms of cultural sensitivity.

However, these associations may simply reproduce cultural stereotypes.

Although the authors recognize the existence of algorithmic bias, they primarily aestheticize it as something capable of provoking discussion.

The system offers no clearly articulated mechanism for mitigating such biases.

Consequently, the critical response remains largely at the level of making bias visible rather than actively addressing its underlying mechanisms.

### 4. Weak Evaluation

The evaluation relies almost entirely on anecdotal evidence, such as visitors becoming emotional in response to the artwork.

The paper does not present:

- A systematic audience study.
- Coded interview data.
- A verifiable comparison between the two design iterations.

Although the reasons behind the second iteration are described concretely, their effects are not systematically evaluated.

This is a common limitation of papers that function partly as artist statements.

### 5. Detailed Technical Description but Relatively Thin Conceptual Argumentation

The TouchDesigner and GLSL processing pipeline is described in considerable detail.

However, the argumentative connection between the inter-embodied self as montage and the actual visual processing techniques remains relatively loose.

Why should Perlin-noise displacement and particle turbulence necessarily express a polyphonic, montage-like conception of the self?

The relationship appears to function more as a retrospective aesthetic justification than as a clearly demonstrated process of design derivation.

## R · Creative Reflection

### 1. A Direct Reference for Latent Images and Latency

The central operation of ReCollection can be summarized as follows:

Fragmented language

AI narrative completion

Development into moving imagery

Dissolution

Replacement by the next participant's memory

This constitutes a complete cycle of latency, development, and renewed disappearance.

It is almost a dynamic version of your concept of the latent image.

You could argue that ReCollection fills the interval of latency with generative completion: within approximately twenty seconds, AI is expected to produce a visually coherent image.

By contrast, the latent image in your research could preserve precisely what this system attempts to overcome:

A state of latency in which an image has not yet appeared and resists being brought to completion.

This creates a productive conceptual opposition:

AI-completed memory versus the latent image that endures delay and refuses completion.

### 2. Slit-Scan and Monotype as Historical Materials for a Genealogy of Delay

The authors have already brought together two historical techniques within digital generative practice:

Slit-scan photography, which translates temporal sequences into spatial arrangements, and monotype printmaking, which emphasizes the singularity and irreproducibility of an impression.

Both can be examined in relation to historical technologies of delayed or latent image formation.

Your chapter on the historical transformation of latency structures could develop a genealogy involving:

- Slit-scan photography — Delay as the spatialization of time.
- Monotype printmaking — The singular and potentially latent condition of an impression.
- Silver-halide photography — The chemically latent image awaiting development.
- Diffusion models — Image emergence through computational processes within latent space.

Together, these techniques could provide a historical framework for examining changing relationships between delay, inscription, image formation, and visibility.

### 3. Physical Correspondence with the 2027 Venice Installation

The installation's spatial and technical configuration offers a direct precedent for your proposed Venice project:

Darkroom-like space + LED display or projection + microphone pedestal + granular-synthesis urban soundscape + circular, reflection-inspired imagery.

It would be useful to treat ReCollection as a direct comparative case study when developing your installation's spatial organization, interaction structure, and audiovisual design.

### 4. Adapting the Digital Ready-Made Approach

The decision not to display raw AI output, but instead to treat it as a ready-made for further transformation, constitutes a strong artistic position.

It deliberately defamiliarizes and recontextualizes machinic vision, avoiding the simplistic approach of treating an AI-generated image as a finished artwork.

This method could inform your own AI-based imaging practice, but with an important reversal.

Rather than aesthetically dissolving the generated output, you could make the traces of latency and incompleteness visible.

Such traces might include:

- Noise
- Unfinished image structures
- Intermediate sampling stages
- Visible computational transitions

These elements could function as visual evidence of the processes through which images emerge from latent space.

### 5. A Different Method for Investigating the Same Problem

ReCollection approaches the imaginative reconstruction of memory through generative AI and critical dementia studies.

You could revisit a related problem through media archaeology and embodied phenomenology.

Rather than asking:

How can AI help us imagine memories?

You could ask:

How do different imaging technologies establish distinct structures of delay through which memory moves from latency into visibility?

Within this framework, ReCollection could be examined as a contemporary case in which AI compresses the interval between memory input and visual manifestation into approximately twenty seconds.

It would therefore become one point within a broader historical analysis of technological structures of latency.

### 6. Reading ReCollection Alongside A Walled City

These two projects were developed by the same research team.

They trace a movement from individual memories shaped by dementia (ReCollection) toward collective digital memorialization (A Walled City).

Their interaction structures also evolve:

- ReCollection: Whispered verbal memories.
- A Walled City: Uploaded photographs.

Yet both retain a common structure:

Participant input → AI transformation → Collective visibility

Both also leave relatively underexamined the question of participants' control over the ways AI transforms or rewrites their contributions.

This makes them a particularly valuable pair of case studies for a discussion of memory agency in generative AI art.

## Form · Reading the Paper as an Academic Genre

### Length and Organization

Excluding the references, the main text occupies approximately nine pages, pp. 51:1–51:9.

The references appear on p. 51:10.

It follows the standard format of a PACM CGIT journal paper, using a single-column layout and author–date citations.

### Approximate Proportions of Sections

| Section                                                         | Approximate proportion |
| --------------------------------------------------------------- | ---------------------- |
| Abstract + Introduction                                         | 12%                    |
| §2 Background: Memory, Imagination, and the Inter-Embodied Self | 18%                    |
| §3 Relevant Work                                                | 10%                    |
| §4 System, Visualization, and Exhibition Design                 | 40%                    |
| §5 Discussion                                                   | 12%                    |
| §6 Conclusion                                                   | 5%                     |
| Acknowledgments and References                                  | 3%                     |

Structural principle: Design methodology, technical implementation, and exhibition description occupy the largest proportion of the paper, while theoretical framing is concentrated in its opening sections.

### Where the Contribution Is First Introduced

The contribution is stated explicitly in the abstract, which describes the assembly of collective visual memories and the blurring of boundaries between remembrance and imagination.

The introduction concludes by formulating three central design questions.

### Key Contribution Statement

> “the artwork assembles collective visual memories based on participants' language input, blurring the boundaries between remembrance and imagination through intelligent system design and experimental visualization.” (Abstract)

### Description Versus Analysis

Descriptive content overwhelmingly dominates the paper.

The system architecture, technical pipeline, visual processing, and exhibition design receive the most extensive treatment.

Analytical discussion is concentrated in the theoretical framing of §2 and the relatively brief reflections in §5.

The paper follows a common structure for practice-oriented creative research:

Conceptual Background → System Design → Exhibition → Discussion

### How Related Work Is Used

The related-work section is short and primarily comparative.

The authors position the project in relation to two new media artworks:

- George Legrady's Pockets Full of Memories
- John Twomey's Not Not

These precedents help establish the project's position, while emphasizing that ReCollection differs through its focus on the intimacy and imaginative possibilities of synthetic memory.

The approach is one of constructing an artistic and intellectual lineage, rather than identifying and contesting a sharply defined research gap.

### How the Design Process Becomes Evidence

The paper documents its process through:

A system diagram (Figure 2), multiple exhibition photographs and visualization screenshots, technical pipeline details, and anecdotal audience responses.

It also provides concrete numerical anchors:

- 98 supported languages
- Approximately 10 seconds of recorded speech
- Approximately 20 seconds for generation
- More than 1,000 exhibition visitors
- Two major design iterations

However, there is no statistical analysis or systematic interview data.

### Figures

The paper includes seven figures, all primarily explanatory or documentary.

Figure 1: Overall exhibition view.

Figure 2: System flow diagram, serving as the primary explanation of the technical methodology.

Figure 3: Screenshots of the generated visualizations.

Figures 4–5: Documentation of the Signal exhibition, including the circular display, pedestal, and participating visitors.

Figures 6–7: Documentation and comparison of the original SIGGRAPH version, with its photo-album-like interface, and the subsequent redesigned version.

Together, the figures explain both how the system operates and how the installation appears and functions in an exhibition environment.

### Narrative Voice and Tense

The paper predominantly uses the first-person plural “we”, although the introduction begins with the more personal “I” in the account of the author's grandmother.

Past and present tenses are used in combination.

The system is generally described in the present tense, while completed exhibitions and design iterations are narrated in the past tense.

This combination of a personal “I” in the opening and a collective “we” throughout the main text is characteristic of creative research papers that integrate emotional motivation with collaborative technical methodology.

### Limitations

There is no independent limitations section.

Instead, limitations are incorporated into the discussion of future directions, including the acknowledgment that the project has not been tested with people living with dementia and the proposed expansion into 3D and VR.

The authors' explicit self-criticism is limited, leaving several conceptual and ethical questions for readers to identify.

## Venue · Publication Context and Expectations

The paper was published in PACM CGIT (Proceedings of the ACM on Computer Graphics and Interactive Techniques), a publication closely associated with the SIGGRAPH research and artistic ecosystem.

The artwork was also exhibited at the SIGGRAPH Art Gallery.

This publication context values the integration of:

Conceptual Background + Intelligent System Design + Experimental Visualization + Exhibition Strategy

It also places importance on sufficiently detailed descriptions of technical pipelines, enabling readers to understand and potentially reproduce the methods involved.

Another distinctive feature is the integration of humanities-oriented theoretical frameworks, such as dementia studies and narratology, with generative computational technologies.

As this paper illustrates, extensive empirical evaluation or direct confrontation with competing theoretical positions is not necessarily required for every contribution.

The principal expectation is a conceptually developed, technically realized, and exhibition-ready AI artwork accompanied by a coherent account of its design rationale.

This places ReCollection within the same general research and artistic ecosystem as A Walled City (published in the same journal) and Are We Gazing at the Same Moon? (SIGGRAPH Art Gallery).

In terms of research presentation, the paper demands more explicit technical and conceptual documentation than a purely exhibition-oriented artist statement, while placing less emphasis on sustained critical-theoretical argumentation than journals such as October or Screen.

This distinction is particularly useful when considering publication strategies for your own research.

If you intend to develop the Venice installation into a paper integrating technical implementation and conceptual argument, PACM CGIT could be a suitable venue.

If your primary contribution instead takes the form of critical theory, media archaeology, or phenomenological analysis, a humanities-oriented journal from your existing publication list may offer a better fit.

## Pa · Quotable Passages (With Page Numbers)

The following quoted passages are retained in English as provided in the original reading notes.

p. 51:1 — Abstract: Core Contribution

> “the artwork assembles collective visual memories based on participants' language input, blurring the boundaries between remembrance and imagination through intelligent system design and experimental visualization.”

p. 51:1 — Introduction: Origins and Central Questions

> “When we coexist with machines, will we accumulate synthetic recollections of collective symbiotic imagination? Is language capable of re-weaving and synthesizing visual memories?”

p. 51:3 — Jenkins (2014): The Inter-Embodied Self as Montage

> “our inter-embodied selves may be more fruitfully conceptualized as montages; polyphonic repertoires of voices and experiences that co-exist in dialogical relationship to one another; constantly updating, constantly changing.”

p. 51:3 — Basting: Imagination Before Memory

> “connection flourishes when we shift away from the expectation of memory and toward the freedom of imagination and shared expression.”

p. 51:5 — Digital Ready-Mades and Historical Imaging Techniques

Particularly relevant to your historical investigation of structures of delay:

> “we drew inspiration from fine-art practices such as the Monotype, a printmaking technique tracing its origins to the 1640s, and slit-scan photography, known for capturing sequential slices of a subject over time… exploring new aesthetics that explore the fleeting visual imagery, undergoing dissolution, tilting, printing, and reprinting over time.”

p. 51:6 — Core Interaction: The Dissolution of Previous Memories into Newly Generated Ones

> “participants observed the visual memories from previous user input fading and dissolving into new ones of their own.”

Translation note: The original structure, critical arguments, technical terminology, page references, and distinctions between the paper's claims and your own research interpretations have been preserved. The English quotations are reproduced from the notes supplied and have not been independently verified against the published paper.

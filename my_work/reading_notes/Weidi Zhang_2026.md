Reading Notes on A Walled City: An Interactive AI Artwork for Decentralized Urban Memories and Collective Presence

Weidi Zhang (Arizona State University), Lijiaozi Cheng (Sheffield), Yi Wang (Canva Research), Jieliang Luo (Minus AI). PACM CGIT 9(3), Article 39, July 2026. DOI: 10.1145/3816084

1 · Why I Read This Paper

This work belongs to a broader trajectory of immersive installations that transform personal images into navigable spatial environments, but it brings questions of memory sovereignty and participant agency into particularly close focus.

Participants upload private photographs, and a multi-agent AI system interprets, “re-aestheticizes,” and spatializes each image into an architectural memory chamber. These chambers accumulate into a decentralized virtual reconstruction inspired by Hong Kong’s Kowloon Walled City.

For my framework of the memory-sovereignty camera, particularly its ideas of dual-layer curation and refusable or vetoable AI-mediated memory, this work provides one of the most direct points of comparison. Of particular importance is its operational definition of the photograph: rather than treating photographs as direct access to subjective experience, the system treats them as cultural artifacts to be interpreted and rewritten.

The work therefore also provides a useful intersection between image phenomenology, media archaeology—with Kowloon Walled City functioning as a media-archaeological object—and machine interpretation.

2 · Summary

What the project is about:
A Walled City is a real-time interactive AI artwork based on the spatial logic, urban morphology, and visual aesthetics of the demolished Kowloon Walled City (KWC), the extraordinarily dense and self-organized urban enclave that existed in Hong Kong from the 1950s until 1993.

Participants scan a QR code and upload images associated with their personal visual memories. A customized multi-agent AI system then interprets, re-aestheticizes, and spatializes each image into a unique architectural chamber, which is continuously incorporated into an evolving urban network.

Main contributions:
(1) A multi-agent AI system that translates submitted images through semantic analysis → depth estimation → architectural reasoning → experimental visualization, producing a real-time generative “monument to memory, density, and collective digital presence”;
(2) an interactive process through which artistic decisions are encoded into the system and made visible in real time;
(3) the positioning of the artwork within a broader historical and philosophical discussion of decentralized urbanism and collective memory in AI-mediated cyberspace.

What problem does it address, and why does it matter?
Contemporary forms of virtual presence increasingly unfold within digital spaces that appear open but are, in practice, tightly controlled by platform protocols and centralized infrastructures—the so-called “walled garden.”

The project therefore asks whether AI systems can reinterpret historical forms of decentralized urbanism in order to construct memory-driven spatial systems for future forms of virtual cohabitation: systems in which memory becomes architecture, identity becomes spatialized, and communities emerge through rhizomatic networks.

Innovation and benefits:
The project operationalizes memory as image-based inference. A photograph is not treated as direct access to subjective experience, but as a culturally charged artifact that can be analyzed, re-aestheticized, and spatialized.

Its four-stage interaction—Load Scene → Visualize Network → Weave a Chamber → Locate in Network—allows fragments of personal memory to remain recognizable while simultaneously being rewritten, maintaining what the authors describe as a “tension between recognition and transformation.”

What does it advance?
Compared with works that visualize memory as images, such as George Legrady’s Pockets Full of Memories, or works that simulate forms of artificial life and behavior, A Walled City transforms individual memories irreversibly into inhabitable three-dimensional forms, anchoring them within the historical logic of a human settlement.

Each new contribution irreversibly alters and extends the living city, embedding individual memories within an ongoing system of co-creation among machine, participant, and artist.

Technically, the system combines LLaVA for semantic understanding, SDXL for style and texture generation, Depth Anything for depth estimation, and an LVM-based architectural reasoning agent. The latter operationalizes the informal settlement logic of Kowloon Walled City as a set of constrained growth rules and incorporates a self-review and revision mechanism to detect structural conflicts and maintain semantic consistency.

3 · Critical Reflections

The authors do not provide a separate limitations section. The only explicitly acknowledged limitations appear in the discussion of future work, particularly regarding navigation and the possibility of allowing users to explore neighborhoods more “organically.” Beyond these, I see several additional issues:

There is effectively no evaluation.
The authors claim that the system “maintains tension between recognition and transformation,” “makes artistic decisions visible,” and enables forms of emergent community. However, apart from two anecdotal audience responses—a Jeff Koons sculpture becoming a dog-like form, and a plate of food becoming a Walled City restaurant, with one participant describing the experience as seeing their memory “moved into another world”—there is no systematic audience study and no evaluation of generative quality or consistency.

Most of these claims therefore remain artist-authored statements of intention rather than empirically supported findings.

An unresolved conceptual tension:
On the one hand, the paper prominently draws on Deleuze and Guattari’s concept of the rhizome, Latour’s Actor-Network Theory (ANT), in which agency is distributed among human and nonhuman actors, and Tsing’s notion of “contingent proximities.” It claims that spatial organization is not imposed through a centralized, top-down structure.

On the other hand, the actual system contains an architectural reasoning agent and review mechanism that actively enforce KWC-derived constraints, eliminate conflicts, and repeatedly revise outputs until they satisfy those constraints. This is itself a relatively centralized and top-down mechanism of ordering.

There is therefore a noticeable discrepancy between the paper’s theoretical vocabulary of decentralization and the engineering reality of the system, but this contradiction is never directly addressed.

The gap in memory sovereignty and participant agency — the most important issue for my research:
Participants can upload their images, but they have no right to negotiate, reject, or veto how the AI rewrites those photographs, what kind of chamber is generated from them, or where that chamber is situated within the city.

Re-aestheticization is essentially one-directional. The paper frames this as a poetic “tension between recognition and transformation,” but from the perspective of memory ethics, the same process can be understood as a loss of participant control over the representation of their own memories.

This is precisely the layer missing from the work that my idea of refusable or vetoable AI-mediated memory attempts to introduce.

Historical appropriation:
The work transforms a real settlement associated with poverty, extralegal conditions, displacement, and demolition into an aesthetic language of cyberpunk density and a cinematic atmosphere of fragmented light.

This creates a risk of romanticizing or decontextualizing a historically difficult space. This problem is reinforced by the relatively limited historical scholarship cited in the paper: several sources on Kowloon Walled City come from popular media such as Fast Company, Bloomberg, and YouTube rather than more substantial historical research.

Scalability and sustainability:
The real-time multi-agent pipeline—LLaVA + SDXL + Depth Anything + LVM + review—runs across two high-performance workstations and a server-based pipeline. The paper does not explain how performance and navigational usability would be maintained as the city continues to grow indefinitely.

The authors themselves describe the system as “not fixed, scalable, or total.” This is conceptually productive as an aesthetic position, but it also implicitly acknowledges that the system is not engineered for scalability in a conventional technical sense.

4 · Creative Reflections

A new idea prompted by the paper:
The proposition that “a photograph is a culturally charged artifact to be interpreted and re-aestheticized, rather than a direct route to subjective experience” provides a particularly clear anti-photographic-transparency argument.

This could connect directly to my discussion of the ontology of shashin (写真) and the machine eye. What a machine “reads” from a photograph is not necessarily subjective experience or Barthes’s ça-a-été (“that-has-been”), but a layer of culturally legible signs and semantic patterns.

Methodological transfer:
The project’s translation pipeline—image → semantics → depth → architectural chamber → network—could be transferred to the spatialization of personal archives or family albums, without retaining the KWC theme.

It could also be adapted to my concept of the memory-sovereignty camera as a critical counter-model: instead of accepting one-directional AI transformation, the system could allow participants to negotiate or veto how their memories are spatialized. This would provide a clear point of differentiation from A Walled City.

A different approach to the same problem:
Their method can be summarized as one-directional AI re-aestheticization supported by the rhetoric of the rhizome.

An alternative would be to place the transformation process itself under participant control, allowing human–AI negotiation during the generation of each chamber. Participants might also be allowed to withdraw, erase, or gradually weather their chambers.

In this model, decentralization would operate not only at the level of visual form or network structure, but at the level of power and control. This would more fully realize the theoretical promises associated with Deleuze, Guattari, and Latour.

A direction worth developing:
Marcos Novak’s threefold conception of cyberspace—architecture as spatial condition, architecture as structural logic, and architecture as constructed form—functions as an important theoretical anchor in the paper and deserves further investigation.

It may provide a way to understand the architecturalization of memory as a form of spatial writing within media archaeology.

5 · Form: Reading the Paper as a Genre
Length of main text (excluding references):
Approximately 9.5 pages. The complete paper is around 11 pages, with roughly one page devoted to references.

Approximate distribution by section:
Introduction ~6% / §2 Conceptual Background (KWC history + “walled gardens”) ~14% / §3 Related Works ~8% / §4 Intelligent System + Visualization + Interaction Design (including §4.1 system, §4.2 four events, §4.3 exhibition setup) ~45% / §5 Architecture as Participatory Process (theory) ~14% / §6 Future Work and Conclusion ~7% / Acknowledgements + References ~6%.

System/interaction design and theoretical discussion function as two parallel centers of gravity, making this paper substantially “heavier” than Flashover.

Where the contribution claim first appears:
The research question is introduced in the second paragraph of the Introduction, followed by an explicit three-part contribution list at the end of §1, beginning with: “Our contributions of this art installation are as follows.” This appears on p. 2.
Contribution statement, verbatim:
“We develop a multi agent AI system that constructs a real time generative monument to memory, density, and collective digital presence by translating submitted images through semantic analysis, depth estimation, architectural reasoning, and experimental visualization.”

Description vs. analysis:
Descriptions of the artwork and system still occupy the majority of the paper. §4 alone takes up almost half of the text and explains the interaction events and individual AI agents in detail.

However, the paper contains substantially more analytical and theoretical material than Flashover. The discussion of “walled gardens” in §2 and the use of the rhizome, ANT, and Tsing in §5 create a combination of thick description + moderate theoretical framing.

Approach to related work:
Unlike Flashover, the paper explicitly constructs a gap.

§3 discusses works by Legrady, Akten, Crespo, and Ji & Wakefield before using the phrase “In contrast, A Walled City…” to distinguish the present project from previous approaches. The central distinction is that the work transforms memory into inhabitable three-dimensional form, rather than merely visualizing it as imagery or simulating behavioral processes.

This is one of the clearest ways in which the paper adopts a more conventional academic structure than Flashover.

How the process is evidenced:
Evidence is provided through ten installation/interface images + system diagrams (Fig. 3 system map and Fig. 4 four-event sequence) + two anecdotal audience quotations.

There are no system logs, quantitative metrics, or formal user-study data.

Figures:
The paper contains ten figures: one installation overview (Fig. 1), two process/sequence diagrams (Figs. 3 and 4), one historical image of KWC (Fig. 2), and a series of screenshots and documentation images corresponding to the four interaction events (Figs. 5–10).

The figures perform three functions simultaneously: establishing credibility, constructing aesthetic atmosphere, and explaining the method. Their evidentiary weight is therefore extremely high.

Person and tense:
The paper primarily uses the first-person plural and present tense (“We develop,” “We employ,” “We construct”) when discussing the system and its design intentions. Historical sections predominantly use the past tense.

Limitations:
Limitations are almost entirely absent. The only explicit acknowledgment appears in §6 in the form of future work concerning navigation.

The phrase “not fixed, scalable, or total” near the end of §5 effectively reframes a potential limitation as an aesthetic and conceptual position, rather than treating it as a technical weakness.

6 · Venue Signals

The publication of this paper in PACM CGIT, within the broader lineage of SIGGRAPH Art Papers, suggests that this venue values a three-part combination of real-time technical systems + explicit conceptual/theoretical framing + strong visual evidence.

Quantitative evaluation and formal user studies are not necessarily required, but the paper demonstrates that a credible related-work gap and a recognizable humanities-oriented theoretical framework—in this case the rhizome, ANT, Tsing, and Novak—carry considerable weight.

Compared with the SIGGRAPH Spatial Storytelling venue of Flashover, where related work and theory were almost absent, the CGIT Art tradition appears to demand a stronger degree of conceptual depth and academic positioning.

Its writing contract therefore seems to occupy an intermediate position between a pure demo paper and a theory-oriented journal such as October or JVC.

7 · Take-Home Points
What I learned:
The paper demonstrates how a humanities-oriented proposition—decentralized urbanism and collective memory—can be operationalized as a functioning multi-agent pipeline, while maintaining the proposition that memory is a culturally interpreted artifact as a conceptual axis connecting system design and theory.
What was new to me:
The use of Kowloon Walled City as a media-archaeological spatial metaphor for AI world-building, together with the concept of image-based inference as an operational definition that decisively rejects photographic transparency.

How it can inform my own research:
(a) The proposition that the photograph is a cultural artifact rather than direct access to subjective experience can directly inform my argument concerning shashin and the machine eye.
(b) The work’s agency gap—participants cannot veto or negotiate the AI’s transformation of their images—provides a particularly useful critical counterpoint to my framework of memory sovereignty and refusable AI-mediated memory.

This could potentially be articulated as a shift from A Walled City toward a negotiable memory apparatus, providing a clear point of differentiation for my own contribution.

Is its structure worth imitating?
Partially, yes. §3, which constructs a clear gap through related works, and §5, which returns to a coherent theoretical framework to interpret the artwork, are unusually well structured for a practice-based paper.

If I were writing for CGIT, DIS, or another art-and-technology research venue, the structure of these two sections would be particularly useful to emulate.

However, its lack of evaluation and its tendency to reframe limitations as aesthetic positions would not transfer well to a more theory- or evidence-oriented venue such as JVC or October.

Overall, it provides a stronger structural model than Flashover for understanding how a practice-based paper can embed theory into the articulation of an artwork.

8 · Quotable Passages (Verbatim, with Page/Section)
p. 2 (§1 & §2):
“the photograph is treated as a culturally charged artifact whose semantic content is analyzed, re-aestheticized, and spatialized, rather than as direct access to subjective experience.”
p. 2 (§2 Conceptual Background):
“Our contemporary virtual presence unfolds within a ‘walled garden’ that appears open and connected, yet is tightly enclosed by platform logics, proprietary protocols, and centralized control.”
p. 5 (§4.2):
“Its visual specificity allows the AI to spatialize memory while remaining recognizable, maintaining tension between recognition and transformation.”
p. 10 (§5):
“The artist-system designer does not centrally determine the spatial logic, but constructs a system in which historical urban knowledge, learned patterns, and participant inputs are brought into relation, through partial alignments and contingent proximities.”
p. 10 (§5):
“it offers a practice of decentralized world-building that is not fixed, scalable, or total, but composed through entanglement, one chamber at a time.”

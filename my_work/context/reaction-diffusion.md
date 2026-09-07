# Reaction--Diffusion Systems

## Deep Research Context Document for an Algorithm Explorer

**Intended use:** Technical and conceptual context for an AI coding
agent building an interactive web-based Algorithm Explorer for an art
and design student.\
**Primary model:** Gray--Scott reaction--diffusion\
**Document emphasis:** theory → computation → visual behavior →
interaction design → artistic experimentation

------------------------------------------------------------------------

## 0. Research Plan and Suitability Check

### Proposed research plan

The research is organized in six layers so that the final document can
function both as a learning resource and as implementation context for a
coding agent.

1.  **Scientific and historical foundation**
    -   Define reaction--diffusion systems.
    -   Trace the idea from mathematical models of diffusion and
        chemical kinetics to Alan Turing's 1952 theory of morphogenesis.
    -   Distinguish the general idea of reaction--diffusion from any one
        implementation.
2.  **Mathematical and computational mechanism**
    -   Explain concentration fields, reaction terms, diffusion, the
        Laplacian, time stepping, grids, initial conditions, and
        boundary conditions.
    -   Explain the Gray--Scott model in detail because it is especially
        useful for interactive visual exploration.
3.  **Parameter-to-visual-behavior mapping**
    -   Identify parameters that materially change the image.
    -   Explain not only what each parameter means mathematically, but
        what a student is likely to *see* when manipulating it.
4.  **Pattern space and implementation**
    -   Study spots, stripes, labyrinths, waves, splitting/mitosis-like
        forms, soliton-like structures, decay, and unstable regimes.
    -   Compare CPU, Canvas, p5.js, WebGL/WebGL2, and shader-based
        approaches.
    -   Translate the algorithm into an implementation pipeline suitable
        for a browser.
5.  **Creative-practice research**
    -   Examine reaction--diffusion as a generative-art technique and as
        a source of architectural/design morphology.
    -   Identify ways artists can deliberately depart from a
        scientifically "pure" simulation: image seeding, spatially
        varying parameters, feedback, masks, motion input, color
        mapping, hybrid systems, etc.
6.  **Algorithm Explorer specification**
    -   Convert the research into practical requirements for an
        interactive application.
    -   Propose controls, presets, visual explanations, parameter-space
        exploration, drawing tools, debugging/learning views, export
        features, and experiments.

### Suitability check

This plan is suitable for the project because the goal is **not merely
to explain reaction--diffusion**, but to make the algorithm *operable as
a visual material*. A purely mathematical report would leave a coding
agent without enough guidance about interface behavior, parameter
ranges, interaction, rendering, and experimentation. Conversely, a
purely creative-coding tutorial would hide the conceptual reason the
patterns emerge.

The six-layer structure therefore connects:

**theory → equations → numerical rules → visible behavior → artistic
manipulation → application design**

That chain is especially appropriate for an Algorithm Explorer because
the interface should help a student understand *causality*: "I changed
this variable; why did the image begin to split, shrink, connect,
oscillate, or disappear?"

------------------------------------------------------------------------

# 1. What Is Reaction--Diffusion?

A **reaction--diffusion system** describes substances, quantities, or
states that both:

1.  **react locally**, changing one another at a particular position;
    and
2.  **diffuse spatially**, spreading from regions of high concentration
    toward surrounding regions.

The important idea is that neither process alone necessarily produces
interesting structure.

Diffusion by itself usually smooths differences. If a drop of dye
spreads through water, concentration differences gradually disappear.

Reaction can create or remove substances locally, but without spatial
coupling it does not automatically create a large-scale image.

When **local nonlinear reactions** and **spatial diffusion** interact,
however, small differences can sometimes be amplified instead of erased.
A nearly uniform field can spontaneously organize into spots, stripes,
waves, branching structures, or labyrinths.

This is why reaction--diffusion is important for generative art: a
complex image does not have to be explicitly drawn. Instead, the artist
defines a system of relationships and lets the image **emerge through
iteration**.

A useful conceptual summary is:

> Reaction determines what happens *here*.\
> Diffusion connects what happens *here* to what happens *nearby*.\
> Iteration lets local differences become global form.

------------------------------------------------------------------------

# 2. Historical and Theoretical Background

## 2.1 Diffusion before Turing

Diffusion was mathematically formalized through equations describing how
concentrations spread in space. In its simplest form, diffusion tends to
flatten gradients: high concentrations spread toward low concentrations.

A basic diffusion equation is:

\[ `\frac{\partial u}{\partial t}`{=tex}=D`\nabla`{=tex}\^2u \]

where:

-   \(u\) is a concentration field;
-   \(D\) is the diffusion coefficient;
-   (`\nabla`{=tex}\^2) is the Laplacian, measuring how a point differs
    from its local neighborhood.

## 2.2 Alan Turing and morphogenesis

The major conceptual turning point was Alan Turing's 1952 paper **"The
Chemical Basis of Morphogenesis."**

Turing proposed that interacting chemical substances---he called them
**morphogens**---could react and diffuse through tissue. A system that
begins almost homogeneous could become unstable after a small
disturbance and develop spatial structure.

The radical insight is sometimes called **diffusion-driven instability**
or **Turing instability**:

> Diffusion, normally associated with smoothing, can under particular
> reaction conditions destabilize a uniform state and help create
> pattern.

Turing was interested in biological morphogenesis: how organized form
can arise during development. His paper considered how chemical dynamics
might contribute to phenomena such as periodic structures and
differentiation.

For art and design, the larger significance is profound: **form can be
produced by a process rather than specified by a blueprint**.

This makes reaction--diffusion historically connected to ideas now
common in computational design:

-   self-organization;
-   emergence;
-   decentralized form generation;
-   procedural morphology;
-   rule-based image production;
-   simulation as an image-making method.

## 2.3 From biological theory to computational image

Reaction--diffusion later became highly visible in computer graphics
because numerical simulation makes its evolving concentration fields
directly renderable.

John E. Pearson's 1993 paper **"Complex Patterns in a Simple System"**
demonstrated a surprisingly large variety of spatiotemporal patterns in
a simple reaction--diffusion model associated with the Gray--Scott
chemistry. The paper describes patterns including spots that grow and
divide.

The Gray--Scott system subsequently became especially popular in
creative coding because:

-   it uses only two concentration fields;
-   its equations are compact;
-   two parameters, commonly called **feed** and **kill**, produce
    dramatically different pattern regimes;
-   it is easy to discretize on a 2D pixel-like grid;
-   every cell can be updated in parallel, making it well suited to
    GPUs.

------------------------------------------------------------------------

# 3. Basic Mathematical and Computational Principles

## 3.1 A field rather than individual particles

Most creative-coding implementations do **not** simulate individual
molecules.

Instead, the canvas is represented as a grid. Each grid cell stores
concentrations of two virtual chemicals.

For Gray--Scott these are usually called:

-   **U** or **A**
-   **V** or **B**

For example, a cell might contain:

``` text
U = 0.82
V = 0.16
```

A 512 × 512 simulation therefore contains two 512 × 512 scalar fields.

The image is produced by mapping one or both fields to brightness or
color.

## 3.2 Diffusion

Diffusion asks:

> Is this cell's concentration higher or lower than the concentrations
> around it?

Computationally this is approximated with a **discrete Laplacian**.

A common 3 × 3 stencil used in creative-coding Gray--Scott
implementations is:

``` text
0.05   0.20   0.05
0.20  -1.00   0.20
0.05   0.20   0.05
```

For a concentration field (U), the weighted neighboring values are
summed to estimate (`\nabla`{=tex}\^2U).

This is essentially a convolution.

Important: this kernel is a numerical approximation and not the only
valid discretization.

## 3.3 Reaction

In Gray--Scott, one reaction is commonly represented conceptually as:

\[ U + 2V `\rightarrow `{=tex}3V \]

The nonlinear reaction term is:

\[ UV\^2 \]

This term consumes U and creates V.

The fact that V appears squared is important: the system is nonlinear.
Small concentration differences can therefore lead to disproportionately
different local behavior.

## 3.4 Feed and removal

The system is open rather than closed.

-   **Feed (F)** replenishes U.
-   **Kill (k)** removes V.
-   V is also affected by the feed term in the standard equations.

This continual input/removal keeps the system away from equilibrium and
allows sustained pattern formation.

------------------------------------------------------------------------

# 4. The Gray--Scott Model

A common dimensionless form is:

\[ `\frac{\partial U}{\partial t}`{=tex} = D_U`\nabla`{=tex}\^2U -
UV\^2 + F(1-U) \]

\[ `\frac{\partial V}{\partial t}`{=tex} = D_V`\nabla`{=tex}\^2V +
UV\^2 - (F+k)V \]

where:

  Symbol                Meaning
  --------------------- -------------------------------
  \(U\)                 concentration of chemical U/A
  \(V\)                 concentration of chemical V/B
  (D_U)                 diffusion rate of U
  (D_V)                 diffusion rate of V
  \(F\)                 feed rate
  \(k\)                 kill/removal rate
  (`\nabla`{=tex}\^2)   spatial Laplacian
  (UV\^2)               nonlinear reaction term

A widely used exploratory starting point, also shown in Karl Sims'
tutorial, is approximately:

``` text
DU = 1.0
DV = 0.5
F  = 0.055
k  = 0.062
dt = 1.0
```

These are not universal "correct values." They are a useful entry point
into one region of a much larger behavioral space.

------------------------------------------------------------------------

# 5. How the Algorithm Works Step by Step

## Step 1 --- Create the simulation grid

Choose a resolution such as:

``` text
256 × 256
512 × 512
1024 × 1024
```

Each cell stores U and V.

## Step 2 --- Initialize a mostly uniform state

A common initial state is:

``` text
U = 1
V = 0
```

across most of the grid.

## Step 3 --- Introduce a disturbance

Add V to one or more small areas.

Example:

``` text
center square:
U ≈ 0
V ≈ 1
```

Alternatively use:

-   random dots;
-   noise;
-   a brush stroke;
-   a photograph;
-   typography;
-   a silhouette;
-   camera input.

The seed is crucial because it defines where instability begins.

## Step 4 --- Calculate local diffusion

For each cell, calculate:

``` text
lapU = Laplacian(U)
lapV = Laplacian(V)
```

## Step 5 --- Calculate reaction

``` text
reaction = U * V * V
```

## Step 6 --- Calculate rates of change

``` text
dU = DU * lapU - reaction + F * (1 - U)
dV = DV * lapV + reaction - (F + k) * V
```

## Step 7 --- Integrate forward in time

With simple explicit Euler integration:

``` text
U_next = U + dU * dt
V_next = V + dV * dt
```

Often values are clamped or otherwise kept within a usable numerical
range.

## Step 8 --- Swap buffers

The new state becomes the old state for the next iteration.

Critically, all cells should conceptually update **simultaneously** from
the previous state. Do not update one cell and immediately let
neighboring cells read that partially updated result.

Use:

``` text
current buffer
next buffer
```

or GPU ping-pong textures/framebuffers.

## Step 9 --- Render

Map concentration to pixels.

Simplest:

``` text
brightness = V
```

More expressive mappings include:

``` text
U - V
abs(U - V)
smoothstep(...)
gradient lookup based on V
```

## Step 10 --- Repeat

Run several simulation iterations per displayed animation frame.

The visible image is therefore not a stored drawing. It is a **temporary
state of a continuously evolving dynamical system**.

------------------------------------------------------------------------

# 6. Parameters and Their Visual Effects

This section is particularly important for an interactive explorer.

## 6.1 Feed rate --- F

**Meaning:** how quickly U is replenished.

Conceptually, feed controls how much "resource" is supplied to the
reaction.

Visual effects depend strongly on the accompanying kill value, so F
should never be interpreted in isolation. Across useful regions,
changing F can alter:

-   feature density;
-   growth rate;
-   spot size;
-   splitting behavior;
-   transitions between isolated and connected forms;
-   whether patterns survive or collapse.

### Explorer design

Use:

-   a slider;
-   numeric input;
-   preferably a **2D F/k parameter map**.

A two-dimensional parameter-space selector is much more educational than
two unrelated sliders because the interesting behavior occurs in regions
of the **joint parameter space**.

------------------------------------------------------------------------

## 6.2 Kill rate --- k

**Meaning:** rate at which V is removed.

Increasing or decreasing k changes the survival conditions for V and can
move the system between:

-   expansion;
-   stable localized structures;
-   splitting;
-   waves;
-   sparse spots;
-   collapse to a uniform state.

Again, its effect is relational: a particular k may behave completely
differently at another F.

------------------------------------------------------------------------

## 6.3 Diffusion coefficients --- DU and DV

These control how quickly each field spreads.

A common setup has U diffuse faster than V.

Changing the ratio can affect:

-   characteristic feature width;
-   spacing;
-   smoothness;
-   stability;
-   scale of spots and stripes;
-   whether pattern formation occurs at all.

### Artistic extension

Allow users to break isotropy:

``` text
DU_x ≠ DU_y
DV_x ≠ DV_y
```

This can stretch circular patterns into directional structures.

------------------------------------------------------------------------

## 6.4 Time step --- dt

The time step determines how far the numerical simulation advances per
iteration.

Larger values:

-   evolve faster per update;
-   can become numerically unstable;
-   may produce explosive or broken patterns.

Smaller values:

-   evolve more smoothly;
-   require more iterations.

For an art tool, numerical instability can itself become an experimental
mode, but the interface should distinguish:

**physical/model behavior** from **numerical artifact**.

------------------------------------------------------------------------

## 6.5 Iterations per animation frame

This is not part of the mathematical model but is important for
perception.

Example:

``` text
1 iteration/frame   → slow, inspectable growth
8 iterations/frame  → active evolution
20+ iterations/frame → rapid morphogenesis
```

Expose it as **Simulation Speed** rather than only as a technical
number.

------------------------------------------------------------------------

## 6.6 Initial conditions / seed

Initial conditions can radically change the composition even when
parameters remain identical.

Useful seeds:

-   central square;
-   one dot;
-   random dots;
-   regular grid;
-   rings;
-   lines;
-   handwriting;
-   text;
-   imported image;
-   webcam silhouette;
-   previous simulation state.

This is one of the strongest artistic controls because it shifts the
system from "generating a texture" to "transforming an image."

------------------------------------------------------------------------

## 6.7 Boundary conditions

Common choices:

### Periodic / wrap

Left connects to right; top connects to bottom.

The simulation behaves like a torus.

Useful for seamless textures.

### Fixed boundary

Edge values remain fixed.

Can produce visible edge effects.

### Reflective / no-flux

Material does not pass through the boundary.

Useful when treating the simulation as a bounded "container."

### Masked / designed boundary

The artist defines where reaction or diffusion is allowed.

This opens direct connections to typography, architecture, image masks,
and spatial composition.

------------------------------------------------------------------------

## 6.8 Laplacian kernel / neighborhood

Changing the diffusion stencil changes spatial behavior.

Possible experiments:

-   standard isotropic 3 × 3;
-   cross-shaped neighborhood;
-   larger-radius kernels;
-   directional weights;
-   noisy weights;
-   spatially varying kernels.

This is a powerful way to expose the hidden assumption that "space"
itself has rules.

------------------------------------------------------------------------

# 7. Typical Visual Patterns

Reaction--diffusion should not be thought of as one "organic texture."
Different parameter regions produce qualitatively different dynamical
regimes.

Common visual families include:

## Spots

Isolated circular or blob-like regions.

Associations: - animal skin; - cells; - islands; - pores; - seeds.

## Stripes

Elongated connected structures.

Associations: - zebra-like markings; - fingerprints; - contour lines; -
vascular systems.

## Labyrinths

Dense interconnected paths with relatively consistent thickness.

Associations: - mazes; - coral; - microscopic tissue; - geological maps.

## Mitosis / splitting structures

Spots grow, elongate, and divide.

Pearson specifically described spots reaching a critical size and
splitting.

This pattern is especially valuable artistically because it appears
**life-like without explicitly simulating organisms**.

## Waves and fronts

Moving boundaries propagate across the field.

These emphasize time rather than static texture.

## Soliton-like/localized structures

Some regimes produce localized moving or interacting structures that
maintain recognizable organization for significant periods.

## Coral-like growth

Dense branching or clustered structures can resemble coral, lichen,
fungus, or mineral deposits.

## Collapse / extinction

Some parameter choices cause V to disappear and the field to return
toward uniformity.

This should **not** be hidden from the user. "Nothing happened" is part
of the phase space.

## Chaotic or unstable regimes

Some states flicker, oscillate, fragment, or continually reorganize.

For artists, instability may be more interesting than a perfectly stable
Turing-like pattern.

------------------------------------------------------------------------

# 8. Why Different Patterns Appear

The central mechanism is **competition across spatial scales**.

A local reaction can reinforce a concentration difference while
diffusion transports concentrations between neighboring areas.

A useful nontechnical mental model is:

``` text
local activation + broader inhibition
```

although not every reaction--diffusion system should be reduced
literally to that phrase.

Pattern scale emerges because some spatial wavelengths grow while others
are suppressed.

Therefore spots and stripes are not "templates" stored in the program.

The program contains:

-   equations;
-   parameters;
-   initial conditions;
-   spatial coupling.

The image is an outcome of those relationships.

This is a major conceptual distinction for an art student:

**Reaction--diffusion generates conditions for form rather than directly
specifying form.**

------------------------------------------------------------------------

# 9. Computational Implementation

## 9.1 CPU implementation

A beginner-friendly implementation can use:

-   JavaScript arrays / typed arrays;
-   HTML Canvas;
-   p5.js.

Pseudo-code:

``` text
initialize U and V arrays

loop:
    for every cell:
        lapU = computeLaplacian(U)
        lapV = computeLaplacian(V)

        reaction = U * V * V

        nextU =
            U + (
                DU * lapU
                - reaction
                + F * (1 - U)
            ) * dt

        nextV =
            V + (
                DV * lapV
                + reaction
                - (F + k) * V
            ) * dt

    swap current and next arrays
    render concentrations
```

### Advantages

-   easy to understand;
-   easy to debug;
-   ideal for educational code;
-   straightforward integration with p5.js.

### Disadvantages

-   higher resolutions become expensive;
-   multiple iterations per frame can reduce frame rate.

------------------------------------------------------------------------

# 10. GPU / WebGL Implementation

Reaction--diffusion is extremely well suited to GPU computation because
each grid cell performs nearly the same local calculation.

A high-performance browser implementation can use:

-   WebGL2;
-   GLSL fragment shaders;
-   floating-point textures;
-   two framebuffers/textures for ping-pong simulation.

Conceptual architecture:

``` text
Texture A
   ↓
Simulation Shader
   ↓
Texture B

Texture B
   ↓
Simulation Shader
   ↓
Texture A
```

Each shader pass:

1.  samples the current cell;
2.  samples neighboring texels;
3.  computes the Laplacian;
4.  applies Gray--Scott equations;
5.  writes the new U/V values.

A separate display shader converts the simulation texture to color.

### Why GPU is preferable for the final Explorer

A coding agent should strongly consider WebGL2 for the polished version
because the application should support:

-   real-time parameter changes;
-   brush interaction;
-   512² or higher grids;
-   several simulation steps per visual frame;
-   responsive animation;
-   richer color processing.

A React interface can manage UI state while WebGL/GLSL performs the
simulation.

------------------------------------------------------------------------

# 11. Recommended Architecture for the Algorithm Explorer

A robust educational web application could be structured as:

``` text
React / UI layer
│
├── parameter controls
├── presets
├── learning panels
├── experiment tools
├── timeline/history
└── export controls
        │
        ▼
Simulation controller
        │
        ▼
WebGL2 Gray–Scott engine
│
├── ping-pong float textures
├── simulation shader
└── display shader
        │
        ▼
Canvas
```

Alternative beginner version:

``` text
p5.js + typed arrays
```

The application can begin with CPU/p5.js for transparency, then migrate
to WebGL if performance becomes limiting.

------------------------------------------------------------------------

# 12. Recommended Interactive Controls

## Essential controls

### Simulation

-   Play / Pause
-   Reset
-   Single Step
-   Simulation Speed
-   Iterations per Frame

### Gray--Scott parameters

-   Feed F
-   Kill k
-   Diffusion U
-   Diffusion V
-   Time step

### Seeding

-   Add V brush
-   Remove V brush
-   Add U brush
-   brush radius
-   brush strength
-   random seed
-   clear field

### Display

-   U view
-   V view
-   U − V view
-   grayscale
-   gradient/color palette
-   invert
-   contrast
-   threshold

------------------------------------------------------------------------

# 13. The Most Useful Educational Feature: F/K Phase-Space Explorer

Instead of only displaying sliders, show a 2D map:

``` text
vertical axis   = F
horizontal axis = k
```

The user clicks or drags across this map and the simulation updates.

This directly teaches that pattern type is not caused by one parameter
independently, but by a **region in parameter space**.

Useful additions:

-   thumbnail previews;
-   named presets;
-   current coordinate marker;
-   trail showing explored values;
-   "random nearby" button;
-   bookmarks;
-   compare two points;
-   animate a path through parameter space.

This feature could become the conceptual center of the application.

------------------------------------------------------------------------

# 14. Presets

Presets should be presented as **entry points**, not as canonical
categories.

Possible labels:

-   Spots
-   Sparse Spots
-   Worms
-   Labyrinth
-   Coral
-   Mitosis
-   Waves
-   Solitons
-   Unstable
-   Decay

Each preset should display:

``` text
F
k
DU
DV
seed type
```

and ideally a short explanation of what the user should observe.

------------------------------------------------------------------------

# 15. Learning / Debug Views

To make the tool genuinely educational, allow the student to see the
invisible mechanics.

## Concentration inspector

Hover over a pixel:

``` text
x: 248
y: 173
U: 0.713
V: 0.281
```

## Neighborhood view

Show the 3 × 3 cells contributing to the Laplacian.

## Separate-field mode

Side by side:

``` text
U field | V field | final rendering
```

## Reaction vs diffusion visualization

Optionally visualize:

``` text
reaction contribution
diffusion contribution
feed contribution
kill contribution
```

This would make the equations visually intelligible.

## Equation panel

Display the equations with parameters highlighted.

When the user moves the F slider, highlight:

``` text
F(1-U)
(F+k)V
```

This links UI manipulation directly to mathematics.

------------------------------------------------------------------------

# 16. Creative Coding and Generative Art

Reaction--diffusion has become a familiar generative-art technique
because it naturally produces:

-   organic complexity;
-   repetition without exact repetition;
-   self-similarity across a field;
-   continuous transformation;
-   ambiguous biological associations;
-   richly textured surfaces.

Karl Sims' online tutorial and RD Tool demonstrate Gray--Scott
simulation as an interactive visual medium. MIT Media Lab
researcher/artist Char Stiles describes using reaction--diffusion in
interactive installations, mouse-driven WebGL work, and hybrid systems
combining reaction--diffusion with cyclic cellular automata.

The important artistic lesson is that the algorithm does not have to
remain scientifically isolated. It can function as a **visual behavior
module** inside a larger artwork.

------------------------------------------------------------------------

# 17. Examples in Art, Design, and Architecture

## 17.1 Char Stiles --- *On Reaction-Diffusion*

Stiles describes multiple creative uses of reaction--diffusion:

-   interactive "mirror"-like media work;
-   WebGL interaction controlled by the mouse;
-   combining reaction--diffusion with cyclic cellular automata;
-   offsetting the previous frame to make patterns drift upward;
-   intentionally exploring unstable systems.

This is a useful precedent because it treats reaction--diffusion as
something to **misuse productively**, not merely simulate accurately.

## 17.2 Kurt Kaminski --- *Cirrus*

*Cirrus* is a large real-time generative installation in Chicago.

The work couples:

-   a fluid simulation;
-   reaction--diffusion;
-   GLSL computation;
-   feedback between reaction and velocity.

The result behaves as an architectural-scale evolving tapestry.

This demonstrates an important creative strategy:

> Couple two dynamical systems so each becomes an input to the other.

## 17.3 Nicu P --- *Soliton* (2024)

This interactive installation maps visitor gesture and body movement
into reaction--diffusion behavior using pose estimation.

Reported mappings include:

-   gesture → pattern initiation;
-   movement speed → reaction rate;
-   body scale → diffusion spread;
-   orientation → boundary disruption.

This provides a strong model for embodied interaction.

## 17.4 Reaction Field --- Yong Ju Lee Architecture

The 2024 *Reaction Field* public installation in Seoul uses
reaction--diffusion-derived curvilinear pattern logic as a spatial
design principle.

The pattern becomes:

-   circulation;
-   furniture;
-   canopy relationship;
-   branching geometry;
-   spatial organization.

This demonstrates a shift from:

``` text
algorithm → image
```

to:

``` text
algorithm → geometry → physical space
```

## 17.5 Graphic and computational design

Reaction--diffusion has also appeared in generative graphic-design and
computational-design teaching contexts, including examples associated
with Karsten Schmidt/toxi and experimental typography/form generation.

For a design student, an especially productive question is therefore:

> What happens when a reaction--diffusion field is not the final image,
> but a control field for another design system?

------------------------------------------------------------------------

# 18. Artistic Modifications and Experiments

This is where an Algorithm Explorer can go beyond a standard scientific
simulator.

## 18.1 Paint the initial condition

Allow the user to draw V directly.

Experiments:

-   signatures;
-   handwriting;
-   faces;
-   symbols;
-   geometric grids;
-   gestural lines.

Observe whether the original image:

-   survives;
-   thickens;
-   dissolves;
-   reproduces;
-   fragments;
-   becomes texture.

Conceptually this turns reaction--diffusion into an **image
transformation process**.

------------------------------------------------------------------------

## 18.2 Import an image

Map image luminance to V:

``` text
dark pixels → high V
light pixels → low V
```

or vice versa.

Possible inputs:

-   photographs;
-   drawings;
-   typography;
-   scans;
-   historical ornaments.

The simulation can then be interpreted as a process of **algorithmic
erosion, growth, or metabolism**.

------------------------------------------------------------------------

## 18.3 Spatially varying parameters

Standard Gray--Scott uses constant F and k.

Instead:

``` text
F = function(x, y)
k = function(x, y)
```

Use:

-   Perlin/Simplex noise;
-   radial gradients;
-   image brightness;
-   distance from cursor;
-   sound amplitude;
-   camera data.

Now different parts of the image inhabit different reaction regimes
simultaneously.

This can create hybrid surfaces where one region forms spots while
another forms labyrinths.

------------------------------------------------------------------------

## 18.4 Parameter painting

Instead of painting chemical concentration, let the brush paint **F or
k**.

The user is no longer drawing the visible image directly. They are
drawing **the local rules that will later generate the image**.

This is an especially strong conceptual experiment for an art/design
project.

------------------------------------------------------------------------

## 18.5 Directional diffusion

Make diffusion anisotropic.

Example:

``` text
horizontal diffusion > vertical diffusion
```

Patterns become stretched and directional.

Allow a vector field to determine diffusion direction.

Possible source:

-   mouse gestures;
-   flow fields;
-   wind data;
-   optical flow;
-   hand-drawn vectors.

------------------------------------------------------------------------

## 18.6 Moving coordinate system

Following the kind of experiment described by Char Stiles, slightly
offset the sampled previous frame:

``` text
sample previous state at (x, y + offset)
```

The pattern appears to drift.

This effectively introduces advection-like behavior.

------------------------------------------------------------------------

## 18.7 Reaction--diffusion + fluid simulation

Use a fluid velocity field to transport U and V.

Then:

``` text
reaction
+
diffusion
+
advection
```

The patterns bend, swirl, and stretch.

This can create smoke-, ink-, cloud-, or tissue-like motion.

------------------------------------------------------------------------

## 18.8 Reaction--diffusion + cellular automata

Combine continuous concentration fields with discrete state rules.

Possibilities:

-   cellular automaton determines where reaction is allowed;
-   RD concentration changes CA state;
-   each system alternately updates the other.

This creates tension between:

``` text
continuous / discrete
organic / rule-based
field / cell
```

------------------------------------------------------------------------

## 18.9 Reaction--diffusion + sound

Map audio features to parameters:

``` text
volume → F
bass → k
treble → diffusion ratio
beat → seed injection
```

The system becomes audiovisual rather than simply animated.

------------------------------------------------------------------------

## 18.10 Camera / body interaction

Map:

-   silhouette → initial condition;
-   hand position → seed;
-   movement velocity → reaction speed;
-   body distance → diffusion;
-   pose → parameter preset.

This makes the participant temporarily part of the pattern-forming
system.

------------------------------------------------------------------------

## 18.11 Multiple species

Move beyond two chemicals.

Three or more interacting fields can produce much richer dynamics.

For an Explorer, this should be an **advanced experimental mode**,
because the two-species Gray--Scott model is easier to understand first.

------------------------------------------------------------------------

## 18.12 Nonuniform boundaries

Use masks shaped like:

-   letters;
-   architecture plans;
-   islands;
-   body silhouettes;
-   logos;
-   ornamental frames.

Reaction--diffusion then becomes a process happening *inside designed
space*.

------------------------------------------------------------------------

## 18.13 Parameter animation

Instead of fixed F and k:

``` text
F(t)
k(t)
```

The system moves through different behavioral regimes over time.

Interesting controls:

-   sine oscillation;
-   random walk;
-   keyframes;
-   Bézier path through F/k space;
-   MIDI controller.

The image becomes a record of changing rules.

------------------------------------------------------------------------

# 19. Artistic Concepts

## 19.1 Emergence

Reaction--diffusion is a direct demonstration of emergence.

No cell knows the final image.

Each location responds only to:

-   its own concentrations;
-   nearby concentrations;
-   shared equations.

Yet coherent large-scale form appears.

This challenges a traditional model of image-making in which the artist
determines every visible mark.

The artist instead designs **conditions for appearance**.

------------------------------------------------------------------------

## 19.2 Nature

Reaction--diffusion patterns often resemble:

-   animal markings;
-   coral;
-   cells;
-   lichen;
-   skin;
-   shells;
-   microbial colonies.

But artistic work should avoid simply saying:

> "The computer imitates nature."

A richer question is:

> Why can an abstract mathematical system appear natural to us?

The visual resemblance suggests that "naturalness" may be perceived
through processes such as:

-   repetition with variation;
-   local interaction;
-   bounded randomness;
-   multiscale organization;
-   growth over time.

------------------------------------------------------------------------

## 19.3 Growth

A reaction--diffusion image is not simply placed on a canvas.

It **develops**.

This introduces a temporal ontology:

``` text
image as object
        ↓
image as process
```

The final frame is only one moment in a longer evolution.

For an artist, this raises a question:

> Is the artwork the final pattern, the evolving animation, the rule
> system, or the act of interacting with it?

------------------------------------------------------------------------

## 19.4 Transformation

Reaction--diffusion can preserve traces of an input while continuously
reorganizing it.

When seeded from an image, the system sits between:

-   representation;
-   destruction;
-   growth;
-   abstraction.

A photograph can become biological texture without a conventional image
filter.

The image is not merely recolored; it is subjected to a new **behavioral
logic**.

------------------------------------------------------------------------

## 19.5 Repetition

Reaction--diffusion often produces repeated motifs, but they are rarely
exact copies.

This creates:

**repetition without duplication**

which is useful for thinking about:

-   ornament;
-   pattern design;
-   textile structures;
-   biological repetition;
-   seriality in art;
-   variation within systems.

------------------------------------------------------------------------

## 19.6 Image-making

Traditional digital image-making often treats the pixel as a value
selected by the artist or calculated from another image.

Reaction--diffusion treats each pixel more like a **state in an evolving
field**.

A pixel is meaningful not only because of its value but because of:

-   its neighborhood;
-   its history;
-   the local reaction;
-   the system's future evolution.

The image becomes relational.

------------------------------------------------------------------------

## 19.7 Control versus autonomy

Reaction--diffusion occupies an interesting position between authorship
and autonomy.

The artist controls:

-   equations;
-   parameters;
-   seeds;
-   boundaries;
-   rendering;
-   interaction.

But the artist does not manually determine every resulting form.

This produces a productive tension:

``` text
control ←────────────→ emergence
```

An Algorithm Explorer should make this tension experiential.

------------------------------------------------------------------------

# 20. Recommended Explorer Modes

Instead of one overloaded interface, the application could have several
modes.

## Mode 1 --- Learn

Minimal controls:

``` text
Play
Pause
Reset
F
k
```

Include short explanations.

Goal: understand the core mechanism.

## Mode 2 --- Explore

Add:

``` text
F/k phase map
presets
DU
DV
speed
seed tools
```

Goal: investigate behavioral space.

## Mode 3 --- Paint

Add:

``` text
chemical brush
eraser
image import
parameter painting
mask
```

Goal: treat the algorithm as an artistic medium.

## Mode 4 --- Analyze

Show:

``` text
U
V
Laplacian
reaction term
parameter values
neighborhood inspector
```

Goal: connect visual behavior to computation.

## Mode 5 --- Experiment

Add:

``` text
spatial parameter maps
anisotropic diffusion
frame offset/advection
audio input
camera input
parameter animation
hybrid systems
```

Goal: intentionally depart from the canonical model.

------------------------------------------------------------------------

# 21. Suggested User Interface

``` text
┌─────────────────────────────────────────────────────┐
│ Reaction–Diffusion Explorer                         │
├──────────────┬─────────────────────────┬────────────┤
│              │                         │            │
│ PARAMETERS   │                         │ LEARN      │
│              │                         │            │
│ Feed     F   │                         │ Equation   │
│ Kill     k   │      SIMULATION         │            │
│ Diff U       │        CANVAS           │ What is    │
│ Diff V       │                         │ happening? │
│ Speed        │                         │            │
│              │                         │ Inspector  │
│ PRESETS      │                         │            │
│              │                         │            │
├──────────────┴─────────────────────────┴────────────┤
│ F / K PARAMETER SPACE                              │
│                                                    │
│        [interactive phase map]                     │
│                                                    │
├─────────────────────────────────────────────────────┤
│ Paint | Seed | Import Image | Randomize | Export   │
└─────────────────────────────────────────────────────┘
```

The simulation should remain visually dominant. The interface should
feel like a **laboratory / instrument**, not a settings page.

------------------------------------------------------------------------

# 22. Features Especially Useful for an Art Student

## A/B comparison

Freeze one simulation and compare it against a modified parameter set.

``` text
LEFT:  F=.055 k=.062
RIGHT: F=.058 k=.062
```

This makes subtle parameter sensitivity visible.

## History

Store recent parameter states.

``` text
State 1
State 2
State 3
...
```

Allow the user to return to unexpected results.

## Random mutation

Button:

``` text
Mutate Parameters
```

Apply small random changes rather than fully random values.

This encourages evolutionary exploration.

## Bookmark pattern

Save:

-   parameters;
-   seed;
-   palette;
-   screenshot;
-   timestamp.

## Export

Useful outputs:

-   PNG;
-   short animation/GIF/WebM if feasible;
-   JSON parameter preset;
-   seed image;
-   high-resolution still.

The JSON export is especially useful because a visual result can be
reproduced.

------------------------------------------------------------------------

# 23. Recommended Technical Defaults

For a first polished implementation:

``` text
Model: Gray–Scott
Grid: 512 × 512
DU: 1.0
DV: 0.5
dt: ~1.0 initially
Rendering: WebGL2
State: floating-point textures
Update: ping-pong framebuffers
UI: React or lightweight vanilla UI
Simulation steps/frame: adjustable
Boundary: periodic by default
Seed: central square + brush
```

Start near:

``` text
F = 0.055
k = 0.062
```

but provide presets and parameter-space exploration rather than implying
this is a uniquely privileged setting.

------------------------------------------------------------------------

# 24. Implementation Warnings for the Coding Agent

## Do not update in-place

Reading and writing the same simulation state sequentially can introduce
directional artifacts.

Use double buffering.

## Handle boundaries explicitly

Do not let array indexing accidentally define boundary behavior.

## Separate simulation from rendering

Keep:

``` text
chemical state
```

independent from:

``` text
display color
```

This allows users to change palettes without altering the simulation.

## Avoid assuming every F/k combination produces a pattern

Uniform or decaying states are legitimate outcomes.

## Performance

If using CPU:

-   use typed arrays;
-   avoid allocating arrays every frame;
-   reduce grid resolution;
-   optionally perform multiple simulation steps before rendering.

If using GPU:

-   use floating-point texture/framebuffer support;
-   use ping-pong textures;
-   minimize unnecessary readback from GPU to CPU.

## Numerical stability

Expose adventurous values in an advanced mode, but keep beginner
defaults within stable ranges.

## Reproducibility

Random seeds should be optionally deterministic.

A saved experiment should ideally contain:

``` text
model
F
k
DU
DV
dt
boundary
initial seed
random seed
grid size
iterations
display mapping
palette
```

------------------------------------------------------------------------

# 25. Proposed Data Model for Saved Experiments

``` json
{
  "model": "gray-scott",
  "grid": {
    "width": 512,
    "height": 512,
    "boundary": "periodic"
  },
  "parameters": {
    "du": 1.0,
    "dv": 0.5,
    "feed": 0.055,
    "kill": 0.062,
    "dt": 1.0
  },
  "simulation": {
    "iterationsPerFrame": 8,
    "paused": false
  },
  "seed": {
    "type": "center-square",
    "randomSeed": 12345
  },
  "display": {
    "field": "v",
    "mapping": "gradient",
    "invert": false
  }
}
```

This makes the explorer useful not only as an interface but as a
repeatable experimental environment.

------------------------------------------------------------------------

# 26. Suggested Experiments for the Student

## Experiment 1 --- One parameter, many images

Keep everything fixed.

Change only F in very small increments.

Record how the morphology changes.

**Question:** At what point does a quantitative parameter change become
a qualitative visual change?

## Experiment 2 --- Same rules, different beginnings

Keep all parameters identical.

Use ten different seed images.

**Question:** How much authorship belongs to the initial condition?

## Experiment 3 --- Image metabolism

Import a photograph or drawing as V.

Let the simulation transform it.

**Question:** At what point does the source image stop being
recognizable?

## Experiment 4 --- Draw rules instead of images

Paint an F/k field.

Do not paint U or V directly.

**Question:** Can the artist compose an image indirectly by composing
its local laws?

## Experiment 5 --- Pattern as time

Save frames every N iterations.

Arrange them as a sequence.

**Question:** Is the "image" one frame, or is the image the history of
transformation?

## Experiment 6 --- Break isotropy

Introduce directional diffusion.

**Question:** How does changing the geometry of diffusion change the
visual idea of "natural growth"?

## Experiment 7 --- Human disturbance

Use mouse speed or body movement to inject V.

**Question:** Does interaction control the system, or merely disturb it?

------------------------------------------------------------------------

# 27. Broader Conceptual Interpretation

Reaction--diffusion is useful in art not simply because it creates
attractive organic patterns.

Its deeper value is that it provides a different model of image
production.

In conventional drawing:

``` text
intention → mark
```

In a reaction--diffusion system:

``` text
intention
   ↓
rules + parameters + initial conditions
   ↓
iterative local interactions
   ↓
emergent image
```

The artist's role shifts from directly determining appearance to
constructing a **space of possible appearances**.

This makes reaction--diffusion relevant to contemporary questions about:

-   procedural authorship;
-   computational agency;
-   simulation;
-   artificial life;
-   nonhuman image production;
-   generative systems;
-   emergence;
-   distributed causality;
-   process-based aesthetics.

The algorithm can therefore be understood not only as a technique for
producing patterns, but as a **model of how an image can come into
being**.

------------------------------------------------------------------------

# 28. Recommended Minimum Viable Product

The first version of the Algorithm Explorer should implement:

1.  Gray--Scott simulation.
2.  Real-time canvas.
3.  Play / Pause / Reset.
4.  F and k sliders.
5.  DU and DV controls.
6.  Speed control.
7.  At least 6 pattern presets.
8.  Mouse/touch chemical painting.
9.  Random seeding.
10. U / V / U−V display modes.
11. F/k 2D parameter selector.
12. Short contextual explanations.
13. PNG export.
14. JSON experiment export/import.
15. Responsive performance.

------------------------------------------------------------------------

# 29. Recommended Advanced Version

After the core version works:

1.  image upload as seed;
2.  parameter painting;
3.  masks;
4.  spatially varying F/k;
5.  anisotropic diffusion;
6.  A/B comparison;
7.  history/bookmarks;
8.  parameter animation;
9.  fluid/advection coupling;
10. camera/body interaction;
11. audio input;
12. high-resolution export;
13. timeline recording;
14. multiple model variants.

The project should prioritize **understanding through manipulation**
over feature quantity.

------------------------------------------------------------------------

# 30. Instructions for an AI Coding Agent

When this document is passed to Cursor or another coding agent, the
following brief can be used:

> Build an interactive web-based Reaction--Diffusion Explorer centered
> on the Gray--Scott model. The application is for an art and design
> student, so it must function simultaneously as a technically correct
> simulation, an educational visualization, and a creative instrument.
>
> Prioritize direct manipulation. Users should be able to change
> feed/kill parameters in real time, paint chemical concentrations into
> the field, switch between concentration views, select presets, reset
> the system, and explore F/k parameter space visually.
>
> Keep simulation state separate from display rendering. Prefer a WebGL2
> ping-pong texture implementation for real-time performance, while
> keeping the code architecture legible and well commented.
>
> Do not design the application as a generic dashboard. The simulation
> should be visually dominant and the interface should feel like an
> experimental laboratory or visual instrument.
>
> Build the basic Gray--Scott simulation first. Confirm numerical
> behavior and interaction before adding advanced creative features.
>
> After the core system is stable, prioritize image seeding, parameter
> painting, spatially varying parameters, A/B comparison, experiment
> history, and exportable presets.

------------------------------------------------------------------------

# 31. Key Takeaways

1.  Reaction--diffusion combines **local nonlinear reaction** with
    **spatial diffusion**.
2.  Turing's 1952 morphogenesis work showed how an initially
    near-uniform system could develop spatial structure through
    instability.
3.  Gray--Scott is particularly suitable for creative coding because a
    compact two-field model produces a broad range of patterns.
4.  Feed and kill parameters should be explored as a **2D behavioral
    space**, not merely as independent sliders.
5.  Initial conditions, diffusion ratios, boundaries, and numerical
    choices are also meaningful creative variables.
6.  The most interesting artistic use is not necessarily faithful
    scientific simulation; productive modifications include image
    seeding, parameter painting, spatial variation, feedback, motion,
    sound, and hybrid systems.
7.  Reaction--diffusion reframes image-making as **the design of
    conditions from which images emerge**.
8.  An effective Algorithm Explorer should make the connection between
    **equation, parameter, process, and visible form** directly
    manipulable.

------------------------------------------------------------------------

# 32. Selected Research Sources

### Foundational theory

**Alan M. Turing --- "The Chemical Basis of Morphogenesis" (1952).**\
Foundational proposal that interacting and diffusing morphogens can
generate spatial structure from an initially homogeneous or
near-homogeneous state.\
DOI: https://doi.org/10.1098/rstb.1952.0012\
Oxford reprint/overview:
https://doi.org/10.1093/oso/9780198250791.003.0022

**John E. Pearson --- "Complex Patterns in a Simple System," Science 261
(1993), 189--192.**\
Numerical investigation of the Gray--Scott system showing diverse
irregular spatiotemporal regimes, including dividing spots.\
DOI: https://doi.org/10.1126/science.261.5118.189

### Computational / educational references

**Karl Sims --- Reaction--Diffusion Tutorial.**\
Clear practical explanation of Gray--Scott, typical coefficients, grid
initialization, Laplacian approximation, and parameter-dependent pattern
formation.\
https://karlsims.com/rd.html

**Karl Sims --- Reaction--Diffusion Explorer Tool.**\
Interactive precedent for a browser-based Gray--Scott exploration
environment.\
https://karlsims.com/rdtool-help.html

**Gray--Scott implementation examples.**\
Reference repository showing governing equations and implementations in
multiple languages.\
https://github.com/wigging/gray-scott

### Creative practice

**MIT Media Lab --- Char Stiles, "On Reaction-Diffusion."**\
Documents reaction--diffusion in interactive media art, WebGL
experiments, mouse interaction, unstable systems, and hybridization with
cellular automata.\
https://www.media.mit.edu/projects/on-reaction-diffusion/overview/

**Kurt Kaminski --- Cirrus.**\
Architectural-scale generative installation coupling reaction--diffusion
with real-time fluid simulation using TouchDesigner and GLSL.\
https://www.kurtkaminski.com/cirrus

**Nicu P --- Soliton (2024).**\
Interactive installation using body/gesture input to seed and modulate
reaction--diffusion patterns.\
https://nicup.art/soliton/

**Yong Ju Lee Architecture --- Reaction Field (2024).**\
Example of translating reaction--diffusion-derived pattern logic into
public-space geometry and furniture.\
Project documentation summarized by Jidipi:
https://architectures.jidipi.com/j00109107/en/reaction-field

### Additional scientific context

**Testing Turing's theory of morphogenesis in chemical cells.**\
Experimental work demonstrating reaction--diffusion differentiation in
coupled chemical cells and testing structures related to Turing's
predictions.\
https://pmc.ncbi.nlm.nih.gov/articles/PMC3970514/

------------------------------------------------------------------------

# 33. Research Note

The term **"Turing pattern"** is sometimes used loosely in art and
design to describe any spot/stripe-like reaction--diffusion image. For
technical accuracy, the Explorer should distinguish:

-   **reaction--diffusion systems** as a broad mathematical class;
-   **Turing's diffusion-driven instability** as a specific theoretical
    mechanism;
-   **Gray--Scott** as one particular reaction--diffusion model
    frequently used in computational art.

That distinction will make the application both creatively flexible and
conceptually rigorous.

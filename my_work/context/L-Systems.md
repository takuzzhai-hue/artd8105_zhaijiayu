# L-Systems (Lindenmayer Systems)

## Deep Research Context Document for an Algorithm Explorer

**Intended use:** Technical and conceptual context for an AI coding
agent building an interactive web-based Algorithm Explorer for an art
and design student.\
**Primary focus:** deterministic and stochastic L-systems, branching
plant models, turtle interpretation\
**Related forms:** D0L systems, context-sensitive L-systems, parametric
L-systems, stochastic L-systems, 2D/3D turtle graphics\
**Document emphasis:** formal rules → rewriting → geometric
interpretation → developmental form → creative manipulation → interface
design

------------------------------------------------------------------------

# 0. Research Plan and Suitability Check

## Proposed research plan

This research is organized in six layers.

### Layer 1 --- Historical and conceptual foundation

-   Define L-systems and distinguish them from ordinary recursive
    drawing tricks.
-   Study Aristid Lindenmayer's 1968 work on formal models of biological
    development.
-   Trace the shift from cellular-development theory to formal-language
    research and later computer graphics and plant modeling.
-   Use *The Algorithmic Beauty of Plants* as a major reference for
    graphical and botanical interpretation.

### Layer 2 --- Formal/computational mechanism

-   Explain alphabet, axiom, production rules, parallel rewriting,
    generations, and interpretation.
-   Explain the critical distinction between generating a symbolic
    string and rendering that string geometrically.
-   Introduce turtle graphics and stack-based branching.

### Layer 3 --- Model families and parameters

-   Cover deterministic context-free L-systems (D0L), stochastic
    systems, context-sensitive systems, parametric systems, and 3D
    extensions.
-   Map iteration depth, turning angle, segment length, production
    rules, probabilities, branch scaling, thickness, tropism, and
    randomness to visible changes.

### Layer 4 --- Implementation

-   Translate the grammar into a browser implementation.
-   Discuss string growth, parsing, turtle state, stack operations,
    progressive rendering, performance, and safe iteration limits.
-   Recommend an architecture suitable for JavaScript / TypeScript,
    Canvas or SVG, and optional WebGL/Three.js for 3D.

### Layer 5 --- Art/design experimentation

-   Investigate L-systems as a generative image-making method rather
    than only a plant simulator.
-   Explore typography, ornament, architecture, animation, interaction,
    sound, image fields, stochastic mutation, rule interpolation, and
    hybrid algorithms.

### Layer 6 --- Algorithm Explorer specification

-   Design an interface that makes the causal chain visible: **grammar →
    generations → symbolic structure → turtle operations → geometry**
-   Propose controls, presets, side-by-side comparisons, generation
    timelines, rule editors, branch inspectors, animation, export, and
    creative modes.

## Suitability check

This plan is suitable because the central difficulty of learning
L-systems is that the visible plant or fractal is **not the algorithm
itself**. There are two linked systems:

1.  a symbolic developmental system that rewrites strings;
2.  a geometric interpreter that turns selected symbols into drawing
    actions.

A useful Algorithm Explorer must expose both.

A student should be able to see:

``` text
Axiom
  ↓
Generation 1
  ↓
Generation 2
  ↓
Generation 3
  ↓
Turtle interpretation
  ↓
Visible form
```

This structure also makes L-systems especially valuable for an
art/design project: the artist can manipulate not just geometry, but the
**grammar that produces geometry**.

------------------------------------------------------------------------

# 1. What Is an L-System?

An **L-system**, short for **Lindenmayer system**, is a formal rewriting
system introduced by biologist Aristid Lindenmayer.

At its simplest, it contains:

1.  an **alphabet** of symbols;
2.  an initial string called the **axiom**;
3.  a set of **production rules**;
4.  a procedure that repeatedly rewrites symbols;
5.  optionally, a geometric interpretation that turns the resulting
    string into an image.

Example:

``` text
Axiom:
F

Rule:
F → F+F−F
```

After one generation:

``` text
F+F−F
```

After another generation, every `F` is replaced simultaneously:

``` text
F+F−F + F+F−F − F+F−F
```

The resulting string can then be interpreted graphically.

For example:

``` text
F = move forward and draw
+ = rotate left
- = rotate right
```

A short symbolic rule can therefore generate increasingly complex
geometry.

The important conceptual point is:

> An L-system does not directly store a complex final shape. It stores a
> developmental rule for repeatedly transforming a structure.

------------------------------------------------------------------------

# 2. Historical and Theoretical Background

## 2.1 Aristid Lindenmayer

Aristid Lindenmayer was a theoretical biologist and botanist.

In 1968 he published two papers titled **"Mathematical Models for
Cellular Interactions in Development"** in the *Journal of Theoretical
Biology*.

The systems later named after him were created to formalize biological
development, particularly:

-   cellular growth;
-   division;
-   neighborhood relationships;
-   filamentous organisms;
-   branching developmental processes.

The original motivation was therefore **development**, not computer
graphics.

This matters conceptually.

An L-system is best understood as:

``` text
a model of how structure changes over generations
```

rather than simply:

``` text
a trick for drawing fractals
```

## 2.2 Parallel rewriting

A defining feature is **parallel rewriting**.

In many traditional formal grammars, one symbol or part of a string may
be rewritten at a time.

In an L-system, all applicable symbols are conceptually rewritten
simultaneously during a generation.

Example:

``` text
Axiom:
AB

Rules:
A → AB
B → A
```

Generation 0:

``` text
AB
```

Generation 1:

``` text
ABA
```

Generation 2:

``` text
ABAAB
```

Both symbols in a generation are evaluated from the same previous
generation.

This parallelism was appropriate for biological modeling because many
cells develop simultaneously.

## 2.3 From biology to formal-language theory

After Lindenmayer's work, computer scientists and mathematicians
developed extensive mathematical theories of L-systems.

The systems became important in:

-   formal language theory;
-   automata theory;
-   combinatorics on words;
-   developmental modeling.

A major theoretical distinction is that an L-system grammar can be
interpreted as a **description of a dynamic process**, rather than only
as a generator of a static language.

## 2.4 From strings to images

A later major development was the use of L-systems for computer
graphics.

Alvy Ray Smith and especially Przemysław Prusinkiewicz helped connect
L-systems with:

-   fractals;
-   turtle graphics;
-   realistic plant modeling;
-   computer animation of plant development.

Prusinkiewicz and Lindenmayer's 1990 book **The Algorithmic Beauty of
Plants** became a foundational reference.

Its major conceptual contribution for visual practice is the
relationship:

``` text
development
→
self-similarity
→
geometry
```

Plant-like visual complexity can emerge because later structures repeat
or transform developmental modules created earlier.

------------------------------------------------------------------------

# 3. Core Components

A basic L-system can be written as:

\[ G = (V, `\omega`{=tex}, P) \]

where:

-   \(V\) = alphabet;
-   (`\omega`{=tex}) = axiom;
-   \(P\) = production rules.

Some definitions include constants or additional components.

------------------------------------------------------------------------

# 4. Alphabet

The alphabet is the set of symbols the system can use.

Example:

``` text
V = {F, X, +, -, [, ]}
```

Not every symbol needs to mean the same kind of thing.

Some symbols may:

-   rewrite but not draw;
-   draw but remain unchanged;
-   rotate the turtle;
-   control branching.

For example:

``` text
X = structural/developmental symbol
F = draw forward
+ = turn
- = turn
[ = save turtle state
] = restore turtle state
```

This distinction is important for an Explorer.

The symbolic grammar and drawing commands should be visually
distinguished.

------------------------------------------------------------------------

# 5. Axiom

The **axiom** is the initial symbolic state.

Example:

``` text
X
```

It can be thought of as:

-   a seed;
-   embryo;
-   starting instruction;
-   initial developmental condition.

Everything that follows is generated from this starting state and the
production rules.

------------------------------------------------------------------------

# 6. Production Rules

A production rule defines how a symbol transforms.

Example:

``` text
X → F+[[X]-X]-F[-FX]+X
F → FF
```

During each generation, every matching symbol is replaced.

A symbol without a matching production rule is usually copied unchanged.

Production rules are where much of the creative power lies.

Changing a few characters can radically change the final morphology.

------------------------------------------------------------------------

# 7. Parallel Rewriting Step by Step

Suppose:

``` text
Axiom:
F

Rule:
F → F+F−F−F+F
```

Generation 0:

``` text
F
```

Generation 1:

``` text
F+F−F−F+F
```

Generation 2:

Each of the five `F` symbols is replaced with the complete rule.

The string becomes much longer.

The important implementation principle is:

``` text
oldString
   ↓
read every symbol
   ↓
append replacements to newString
   ↓
replace oldString with newString
```

Do not rewrite characters in-place while simultaneously reading the
modified result.

------------------------------------------------------------------------

# 8. From Symbols to Geometry: Turtle Graphics

The L-system itself produces strings.

A separate interpreter converts the string into geometry.

A common approach is **turtle graphics**.

Imagine a virtual turtle with:

``` text
position
heading
step length
drawing state
```

The turtle reads the generated string from left to right.

A common command vocabulary is:

``` text
F  move forward and draw
f  move forward without drawing
+  rotate by +angle
-  rotate by -angle
[  push current state
]  pop previous state
```

Additional commands may represent:

``` text
leaf
flower
branch thickness
color
roll
pitch
yaw
```

------------------------------------------------------------------------

# 9. Why a Stack Is Necessary for Branching

Consider:

``` text
F[+F]F[-F]F
```

When the turtle encounters:

``` text
[
```

it stores its current:

``` text
position
heading
possibly thickness/color/scale
```

onto a stack.

It then draws the branch.

When it reaches:

``` text
]
```

it restores the previous state.

Conceptually:

``` text
main stem
   |
   |---- branch
   |
   |---- branch
   |
```

Without the stack, the turtle would continue from the end of the first
branch instead of returning to the branching point.

This simple push/pop mechanism is fundamental to plant-like L-systems.

------------------------------------------------------------------------

# 10. Step-by-Step Algorithm

## Step 1 --- Define alphabet

Example:

``` text
F X + - [ ]
```

## Step 2 --- Define axiom

``` text
X
```

## Step 3 --- Define rules

Example:

``` text
X → F+[[X]-X]-F[-FX]+X
F → FF
```

## Step 4 --- Choose generation count

Example:

``` text
iterations = 5
```

## Step 5 --- Rewrite in parallel

Repeat:

``` text
next = ""

for symbol in current:
    if rule exists:
        next += replacement
    else:
        next += symbol

current = next
```

## Step 6 --- Initialize turtle

``` text
position = startingPoint
heading = -90°
length = segmentLength
stack = []
```

## Step 7 --- Interpret generated string

For each symbol:

``` text
F → draw forward
+ → turn
- → turn
[ → save state
] → restore state
```

## Step 8 --- Render

Draw lines, polygons, leaves, sprites, or meshes.

## Step 9 --- Experiment

Change:

``` text
axiom
rules
angle
iterations
length
randomness
scale
```

and regenerate.

------------------------------------------------------------------------

# 11. The Most Important Parameters

## 11.1 Iteration / generation depth

This determines how many rewriting generations occur.

Example:

``` text
0 → seed
1 → simple structure
2 → more branches
3 → increasingly complex
...
```

### Visual effect

Increasing iterations usually creates:

-   greater complexity;
-   more detail;
-   more repeated structure;
-   longer strings;
-   more branches;
-   smaller apparent features if the result is scaled to fit the canvas.

However, complexity often grows exponentially.

A one-step increase can produce a huge computational jump.

### Explorer requirement

Show:

``` text
Generation 0
Generation 1
Generation 2
...
```

as a timeline rather than only a slider.

------------------------------------------------------------------------

# 12. Turning Angle

The turtle turns by angle:

\[ `\theta`{=tex} \]

when encountering `+` or `-`.

### Small angle

Produces:

-   narrow branching;
-   vertical or directional growth;
-   delicate curvature-like structures.

### Large angle

Produces:

-   wide branching;
-   open structures;
-   star-like or radial forms;
-   stronger angularity.

Changing only the angle while preserving the grammar can transform the
entire visual character.

This makes angle one of the strongest real-time controls.

------------------------------------------------------------------------

# 13. Segment Length

`F` usually moves by a distance:

``` text
stepLength
```

Changing it scales the drawing.

But more interesting systems allow segment length to change by
generation or branch depth.

Example:

``` text
childLength =
parentLength * 0.72
```

This creates tapering developmental scale.

------------------------------------------------------------------------

# 14. Production Rules

Rules are the deepest structural parameter.

Changing:

``` text
F → FF
```

to:

``` text
F → F[+F]F[-F]F
```

does not merely adjust an existing image.

It changes the **developmental grammar**.

For an Explorer, rule editing should therefore be treated as a
first-class interaction, not buried in advanced settings.

------------------------------------------------------------------------

# 15. Axiom

Changing the starting seed can create dramatically different structures
even with identical rules.

This raises a useful artistic question:

> How much of the final image belongs to the rule, and how much belongs
> to the initial condition?

------------------------------------------------------------------------

# 16. Branch Angle Asymmetry

Instead of:

``` text
+ = +25°
- = -25°
```

allow:

``` text
leftAngle = 18°
rightAngle = 32°
```

This breaks bilateral symmetry.

The plant may appear:

-   windblown;
-   unbalanced;
-   directional;
-   more biologically irregular.

------------------------------------------------------------------------

# 17. Branch Length Scaling

Introduce:

``` text
lengthScale = 0.7
```

for nested branches.

Effects:

-   lower values → rapidly shrinking delicate branches;
-   higher values → long dense branches.

------------------------------------------------------------------------

# 18. Thickness and Taper

Track line width as part of turtle state.

Example:

``` text
trunk width = 8
child width = parent width × 0.7
```

This changes the result from a mathematical line diagram into a more
bodily or botanical structure.

------------------------------------------------------------------------

# 19. Randomness

Classic deterministic L-systems produce identical results every time.

Randomness can be introduced through:

-   stochastic rules;
-   random turning angles;
-   random segment lengths;
-   random branch deletion;
-   random color;
-   random thickness.

The system then shifts from:

``` text
exact repetition
```

toward:

``` text
family resemblance
```

------------------------------------------------------------------------

# 20. Common L-System Models

## 20.1 D0L Systems

A **deterministic context-free L-system** is one of the simplest forms.

Characteristics:

-   each symbol has one deterministic replacement;
-   replacement does not depend on neighbors;
-   all symbols rewrite in parallel.

Example:

``` text
Axiom:
F

Rule:
F → F+F−F−F+F
```

Excellent starting point for the Explorer.

------------------------------------------------------------------------

# 21. Stochastic L-Systems

A symbol can have multiple possible productions with probabilities.

Example:

``` text
F →
  0.5: F[+F]F
  0.3: F[-F]F
  0.2: FF
```

Every generation can therefore differ.

### Artistic importance

This produces a family of related structures rather than one fixed
fractal.

The artist designs a **distribution of possibilities**.

Useful controls:

``` text
Random Seed
Probability A
Probability B
Probability C
```

------------------------------------------------------------------------

# 22. Context-Sensitive L-Systems

The replacement of a symbol can depend on neighboring symbols.

Conceptually:

``` text
A < B > C → X
```

means:

``` text
replace B with X
when B has A on the left
and C on the right
```

This permits richer developmental relationships.

It is more biologically expressive because a module's development can
depend on its surroundings.

For the Explorer, context-sensitive rules should be an advanced mode.

------------------------------------------------------------------------

# 23. Parametric L-Systems

Symbols carry numeric parameters.

Example:

``` text
F(10)
```

might mean:

``` text
draw forward 10 units
```

A production could transform:

``` text
F(x) → F(x * 0.8)
```

This enables:

-   age;
-   branch length;
-   width;
-   energy;
-   growth rate;
-   developmental state;

to exist inside the grammar.

Parametric L-systems are extremely useful for advanced generative design
because they bridge symbolic rules and continuous geometry.

------------------------------------------------------------------------

# 24. 3D L-Systems

The turtle can exist in 3D.

Instead of only heading, it tracks orientation axes.

Commands may rotate around:

-   yaw;
-   pitch;
-   roll.

A 3D interpreter can produce:

-   trees;
-   roots;
-   coral-like structures;
-   spatial branching;
-   architectural frameworks.

Recommended technology:

``` text
Three.js
```

for an advanced web version.

------------------------------------------------------------------------

# 25. Typical Visual Patterns

L-systems can produce much more than plants.

Common families include:

## Fractal curves

-   Koch curve;
-   Koch snowflake;
-   Dragon curve;
-   Hilbert-like structures;
-   Sierpiński-like structures.

## Trees

-   binary branching;
-   asymmetric trees;
-   recursive branch systems.

## Ferns

Repeated branching modules can create fern-like silhouettes.

## Bushes

Dense stochastic branching creates shrub-like masses.

## Flowers

Rules can create stems, leaves, radial flower heads, and repeated
organs.

## Roots

Downward or gravity-influenced branching can produce root-like systems.

## Coral / vascular structures

Repeated branching can evoke:

-   blood vessels;
-   neurons;
-   lightning;
-   rivers;
-   coral.

## Ornament

Recursive symmetry can produce decorative borders and motifs.

## Networks

The turtle path can generate:

-   circulation systems;
-   street-like structures;
-   spatial diagrams.

------------------------------------------------------------------------

# 26. Why L-Systems Look Natural

The natural appearance is not simply caused by randomness.

A major reason is **developmental repetition**.

Plants often exhibit structures in which:

-   a branch resembles a smaller version of the whole;
-   modules repeat;
-   later growth develops from earlier growth;
-   local branching rules recur at multiple scales.

This produces **self-similarity**, but biological-looking systems are
often not perfectly self-similar.

They include:

-   scaling;
-   asymmetry;
-   environmental influence;
-   stochastic variation;
-   developmental constraints.

Therefore an advanced Explorer should allow users to move continuously
between:

``` text
perfect formal repetition
and
irregular developmental variation
```

------------------------------------------------------------------------

# 27. Computational Implementation

## 27.1 Basic browser implementation

Recommended first version:

``` text
TypeScript / JavaScript
+
HTML Canvas
```

or:

``` text
p5.js
```

The system has two major modules:

``` text
Grammar Engine
+
Turtle Renderer
```

Keep these separate.

------------------------------------------------------------------------

# 28. Grammar Engine Pseudocode

``` text
function expand(axiom, rules, iterations):

    current = axiom

    repeat iterations times:

        next = ""

        for symbol in current:

            if rules contains symbol:
                next += rules[symbol]
            else:
                next += symbol

        current = next

    return current
```

For stochastic systems:

``` text
rules[symbol]
```

returns a randomly selected production according to probability.

------------------------------------------------------------------------

# 29. Turtle Renderer Pseudocode

``` text
state:
    x
    y
    angle
    length
    thickness

stack = []

for symbol in generatedString:

    if symbol == "F":
        newX = x + cos(angle) * length
        newY = y + sin(angle) * length

        drawLine(x, y, newX, newY)

        x = newX
        y = newY

    if symbol == "+":
        angle += turnAngle

    if symbol == "-":
        angle -= turnAngle

    if symbol == "[":
        stack.push(copy(state))

    if symbol == "]":
        state = stack.pop()
```

------------------------------------------------------------------------

# 30. Performance

The major computational danger is **exponential string growth**.

Suppose one symbol becomes five copies each generation.

Then roughly:

``` text
1
5
25
125
625
3125
15625
...
```

The Explorer should therefore protect users from accidentally freezing
the browser.

Recommended:

``` text
MAX_SYMBOLS = configurable safety limit
```

Before expansion, estimate or monitor string size.

Display:

``` text
Generation: 7
Symbols: 184,392
Segments: 61,201
```

This itself is educational.

------------------------------------------------------------------------

# 31. Progressive Growth Rendering

Do not always render the final geometry instantly.

Allow:

``` text
Growth Animation
```

The turtle interprets only part of the string each frame.

Example:

``` text
100 commands/frame
```

This visually reconstructs development.

Possible modes:

### Draw order

Reveal geometry according to turtle traversal.

### Generation order

Animate:

``` text
generation 0 → 1 → 2 → 3
```

### Biological growth approximation

Animate branch extension and child emergence separately.

This is especially valuable because L-systems are fundamentally
developmental.

------------------------------------------------------------------------

# 32. Canvas vs SVG vs WebGL

## Canvas

Best general choice for:

-   many segments;
-   animation;
-   real-time experimentation;
-   trails.

## SVG

Useful for:

-   vector export;
-   inspectable geometry;
-   moderate segment counts;
-   graphic design workflows.

## WebGL / Three.js

Useful for:

-   very large systems;
-   3D L-systems;
-   spatial camera navigation;
-   volumetric branch structures.

Recommended:

``` text
Canvas first
SVG export
Three.js later
```

------------------------------------------------------------------------

# 33. Generative Art and Creative Coding

L-systems are especially important for generative art because they
separate:

``` text
rule
from
result
```

The artist can define a compact symbolic grammar and generate images too
complex to design element-by-element.

This changes authorship.

Instead of:

``` text
draw this branch here
```

the artist says:

``` text
whenever this developmental symbol appears,
replace it according to this relationship
```

The artwork becomes an exploration of **rule space**.

------------------------------------------------------------------------

# 34. The Algorithmic Beauty of Plants

Prusinkiewicz and Lindenmayer's *The Algorithmic Beauty of Plants* is
foundational for understanding L-systems visually.

It develops graphical modeling using L-systems and applies them to:

-   trees;
-   herbaceous plants;
-   phyllotaxis;
-   plant organs;
-   developmental animation;
-   cellular layers;
-   fractal properties of plants.

The book is particularly useful for an art/design context because it
treats plant form as the visible consequence of developmental procedures
rather than as static geometry.

------------------------------------------------------------------------

# 35. L-Systems in Creative Software

L-system concepts have appeared in procedural and 3D tools.

For example, Houdini includes an L-System node where generated strings
are interpreted through turtle-like commands to create geometry.

This shows how L-systems can move beyond educational fractal drawing and
become part of professional procedural modeling workflows.

------------------------------------------------------------------------

# 36. L-Systems in Architecture and Generative Design

L-systems have been studied as one of several generative techniques in
architectural design alongside:

-   cellular automata;
-   genetic algorithms;
-   shape grammars;
-   swarm intelligence.

Possible architectural uses include:

-   branching structural systems;
-   façade subdivision;
-   circulation;
-   spatial growth;
-   urban networks;
-   ornamental systems;
-   recursive modular assemblies.

A crucial design shift is:

``` text
L-system string
      ↓
turtle / geometric interpretation
      ↓
curves
      ↓
thickness / surfaces / volumes
      ↓
architectural geometry
```

The generated line does not have to be the final design.

It can become a **skeleton for another geometric process**.

------------------------------------------------------------------------

# 37. Artistic Experiment: Rewrite Typography

Treat letters or words as symbols in a grammar.

Example:

``` text
A → ART
R → RULE
T → TREE
```

The generated text can itself become visual material.

Alternatively, use linguistic symbols as structural modules.

This reveals that an L-system sits between:

``` text
language
and
image
```

------------------------------------------------------------------------

# 38. Artistic Experiment: Draw the Grammar

Instead of hiding the generated string, display it beside the image.

Highlight the symbol currently being interpreted.

Example:

``` text
F F [ + F X ] ...
        ↑
```

At the same moment, highlight the corresponding branch on the canvas.

This creates a direct visual bridge:

``` text
symbol ↔ gesture
```

This should be a major educational feature.

------------------------------------------------------------------------

# 39. Artistic Experiment: Rule Mutation

Create a button:

``` text
MUTATE RULE
```

Possible mutations:

-   insert symbol;
-   delete symbol;
-   swap `+` and `-`;
-   add branch brackets;
-   duplicate a module;
-   alter probability.

Small textual mutations can produce dramatic morphological changes.

This creates a powerful relationship between:

``` text
genotype-like rule
and
phenotype-like image
```

without claiming that an L-system is literally genetics.

------------------------------------------------------------------------

# 40. Artistic Experiment: Rule Breeding

Create two grammars:

``` text
Parent A
Parent B
```

Combine parts of their rules.

Generate offspring grammars.

This connects naturally to the later **Genetic Algorithm Explorer**.

Possible workflow:

``` text
grammar A
+
grammar B
↓
rule crossover
↓
new L-system
```

------------------------------------------------------------------------

# 41. Artistic Experiment: Stochastic Plants

Keep the same grammar but change the random seed.

Display a grid of 20 outputs.

The result becomes a study of:

``` text
identity
vs
variation
```

All images share a developmental grammar but differ in individual
realization.

------------------------------------------------------------------------

# 42. Artistic Experiment: Environmental Growth

Classic L-systems can be extended so growth responds to external
information.

Possible environmental fields:

-   light;
-   gravity;
-   cursor;
-   image brightness;
-   sound;
-   wind;
-   obstacle maps.

Example:

``` text
branches turn toward mouse position
```

or:

``` text
dark image regions inhibit growth
```

The grammar produces potential growth while the environment modifies
realization.

------------------------------------------------------------------------

# 43. Artistic Experiment: Tropism

Introduce a directional force such as gravity.

Branches gradually bend toward a vector.

Conceptually:

``` text
grammar determines branching
+
tropism modifies orientation
```

This breaks rigid fractal geometry and creates more organic forms.

Useful controls:

``` text
Tropism Direction
Tropism Strength
```

------------------------------------------------------------------------

# 44. Artistic Experiment: Image-Guided Growth

Import a photograph.

Use image values to affect:

-   branch probability;
-   turn angle;
-   segment length;
-   thickness;
-   color;
-   termination.

For example:

``` text
dark pixels → more branching
light pixels → less branching
```

The source image becomes an invisible developmental landscape.

------------------------------------------------------------------------

# 45. Artistic Experiment: Sound-Guided Grammar

Map audio to parameters.

Example:

``` text
bass → branch length
volume → angle
treble → stochasticity
beat → new generation
```

A plant or abstract structure can "grow" through sound.

------------------------------------------------------------------------

# 46. Artistic Experiment: Body Interaction

Use webcam or hand tracking.

Possible mappings:

``` text
hand height → growth generation
hand horizontal position → angle
pinch → bloom
body silhouette → obstacle
movement speed → wind/tropism
```

A recent browser-based creative coding example combines an L-system
flower structure with MediaPipe hand tracking so gesture influences sway
and blooming.

------------------------------------------------------------------------

# 47. Artistic Experiment: Time-Based Rule Change

Normally rules remain constant.

Instead:

``` text
Generation 0–2:
X → rule A

Generation 3–5:
X → rule B

Generation 6+:
X → rule C
```

The organism changes its developmental logic over time.

This creates:

``` text
growth
+
historical transformation
```

The final image contains traces of different rule regimes.

------------------------------------------------------------------------

# 48. Artistic Experiment: Local Grammar

Different branches can carry different states.

Using parametric or context-sensitive systems:

``` text
young branch
mature branch
damaged branch
flowering branch
```

may follow different productions.

The structure gains internal differentiation.

------------------------------------------------------------------------

# 49. Artistic Experiment: L-System + Reaction--Diffusion

Use an L-system to generate a branching skeleton.

Then seed Reaction--Diffusion along the branches.

Pipeline:

``` text
L-system
→
branch geometry
→
RD seed
→
organic surface
```

The L-system provides developmental topology.

Reaction--Diffusion provides local texture/morphogenesis.

This would make a strong cross-algorithm experiment in the larger
Algorithm Explorer.

------------------------------------------------------------------------

# 50. Artistic Experiment: L-System + Boids

Use branches as:

-   paths;
-   obstacles;
-   attraction lines;

for Boids.

Or let Boid trails become input for a branching grammar.

This connects:

``` text
developmental structure
with
collective movement
```

------------------------------------------------------------------------

# 51. Recommended Interactive Controls

## Grammar

-   Axiom text field
-   Production rule editor
-   Add Rule
-   Delete Rule
-   Validate Grammar
-   Reset Grammar

## Generation

-   Iteration slider
-   Previous Generation
-   Next Generation
-   Animate Generations
-   Show Symbol Count

## Turtle

-   Turn Angle
-   Segment Length
-   Starting Angle
-   Line Width
-   Length Scaling
-   Thickness Scaling

## Stochasticity

-   Random Seed
-   Rule Probabilities
-   Angle Jitter
-   Length Jitter
-   Branch Dropout

## Rendering

-   Fit to Canvas
-   Zoom
-   Pan
-   Line / Ribbon mode
-   Color by Branch Depth
-   Color by Symbol
-   Color by Generation
-   Show Leaves
-   Show Nodes

## Analysis

-   Show Generated String
-   Highlight Current Symbol
-   Show Turtle Position
-   Show Stack Depth
-   Show Bounding Box
-   Show Branch Depth

------------------------------------------------------------------------

# 52. Essential Feature: Generation Timeline

Display:

``` text
G0  G1  G2  G3  G4  G5
●───●───●───●───●───●
```

Selecting a generation shows:

-   generated string;
-   symbol count;
-   rendered geometry;
-   branch count;
-   bounding box.

This makes growth legible as a sequence.

------------------------------------------------------------------------

# 53. Essential Feature: Rule-to-Geometry Linking

Split the interface:

``` text
RULE / STRING
        |
        |
        v
GEOMETRY
```

When hovering over a substring, highlight the geometry generated by it
if mapping data is available.

When hovering over a branch, show which symbol occurrence produced it.

This transforms an abstract grammar into something spatially
understandable.

------------------------------------------------------------------------

# 54. Essential Feature: Stack Visualizer

For branching systems, show:

``` text
STACK
────────
state 3
state 2
state 1
```

When `[` is read:

``` text
PUSH
```

When `]` is read:

``` text
POP
```

This is especially useful for students who do not code.

It explains how branching can emerge from a linear string.

------------------------------------------------------------------------

# 55. Rule Presets

Include presets such as:

-   Koch Curve
-   Koch Snowflake
-   Sierpiński-like Curve
-   Dragon-style Curve
-   Binary Tree
-   Plant
-   Fern
-   Bush
-   Stochastic Tree
-   Asymmetric Plant

Each preset should expose:

``` text
axiom
rules
angle
iterations
```

Never hide the grammar behind a preset name.

The point is to learn from it.

------------------------------------------------------------------------

# 56. Suggested Explorer Modes

## Mode 1 --- Learn

Show:

``` text
axiom
one rule
generation timeline
simple turtle
```

Goal: understand rewriting.

## Mode 2 --- Build

Allow:

``` text
rule editing
angle
iterations
branching
```

Goal: construct grammars.

## Mode 3 --- Inspect

Show:

``` text
generated string
current symbol
turtle state
stack
branch depth
```

Goal: understand symbolic-to-spatial translation.

## Mode 4 --- Grow

Animate generations and progressive turtle drawing.

Goal: understand development and time.

## Mode 5 --- Design

Add:

``` text
color
thickness
leaves
ribbons
SVG export
```

Goal: use the system as a graphic tool.

## Mode 6 --- Experiment

Add:

``` text
stochastic rules
parametric rules
tropism
image fields
sound
camera
rule mutation
```

Goal: move beyond canonical L-systems.

------------------------------------------------------------------------

# 57. Suggested UI Layout

``` text
┌────────────────────────────────────────────────────────────┐
│ L-SYSTEM EXPLORER                                          │
├──────────────────┬─────────────────────────┬───────────────┤
│                  │                         │               │
│ GRAMMAR          │                         │ INSPECTOR     │
│                  │                         │               │
│ Axiom: X         │       GENERATED         │ Generation 4  │
│                  │        GEOMETRY         │ Symbols 8211  │
│ X → ...          │                         │ Stack depth   │
│ F → FF           │                         │ Branch depth  │
│                  │                         │               │
│ + Add Rule       │                         │               │
├──────────────────┴─────────────────────────┴───────────────┤
│ G0 ─ G1 ─ G2 ─ G3 ─ G4 ─ G5                              │
│                  GENERATION TIMELINE                       │
├────────────────────────────────────────────────────────────┤
│ Angle | Length | Iterations | Randomness | Grow | Export  │
└────────────────────────────────────────────────────────────┘
```

The interface should feel like a **grammar laboratory / growth
instrument**, not a settings dashboard.

------------------------------------------------------------------------

# 58. Artistic Concept: Emergence

L-systems demonstrate emergence differently from Boids or
Reaction--Diffusion.

In an L-system, complexity emerges from repeated symbolic substitution.

A tiny rule may produce an enormous structure.

Conceptually:

``` text
small description
        ↓
repetition
        ↓
large complexity
```

This raises questions about compression:

> How much visual complexity can be contained inside a very small rule?

------------------------------------------------------------------------

# 59. Artistic Concept: Nature

L-systems are strongly associated with plants.

But the important question is not:

``` text
Can a computer draw a tree?
```

A richer question is:

> Can the appearance of a tree be approached by describing a process of
> development rather than describing its final outline?

This moves representation from:

``` text
shape imitation
```

to:

``` text
process imitation
```

------------------------------------------------------------------------

# 60. Artistic Concept: Growth

Growth is perhaps the most central artistic concept for L-systems.

The final structure can be understood as accumulated developmental
history.

Generation 5 contains transformations derived from generations 0--4.

The image is therefore not simply a configuration.

It is a **record of repeated becoming**.

------------------------------------------------------------------------

# 61. Artistic Concept: Transformation

Each generation transforms symbolic material.

Example:

``` text
X
↓
F[+X]...
↓
FF[+F...]...
```

Identity is maintained through transformation.

This creates a useful tension:

``` text
continuity
vs
change
```

------------------------------------------------------------------------

# 62. Artistic Concept: Repetition

L-systems use literal repetition at the level of rules.

But repetition does not necessarily produce visual monotony.

Because repeated modules occur at:

-   different positions;
-   different orientations;
-   different depths;
-   different scales;

the same instruction becomes many different visual events.

Thus:

``` text
same rule
+
different context
=
visual variation
```

------------------------------------------------------------------------

# 63. Artistic Concept: Image-Making

Traditional image-making often begins with spatial decisions:

``` text
put line here
put shape there
```

L-systems begin with symbolic relationships:

``` text
replace this symbol
with this sequence
```

Only afterward does space appear.

The process becomes:

``` text
symbol
→
grammar
→
development
→
movement
→
image
```

This is a fundamentally different image-making ontology.

------------------------------------------------------------------------

# 64. Artistic Concept: Language and Image

L-systems occupy an unusual space between writing and drawing.

The same object can be viewed as:

``` text
a string of symbols
```

or:

``` text
a plant / fractal / ornament
```

The image has a textual substrate.

This makes L-systems especially interesting for:

-   typography;
-   concrete poetry;
-   computational writing;
-   notation;
-   code art;
-   generative graphic design.

------------------------------------------------------------------------

# 65. Artistic Concept: Rule and Freedom

A deterministic L-system is extremely rule-bound.

Yet it can produce forms that look organic.

A stochastic L-system introduces uncertainty while preserving grammar.

This creates a continuum:

``` text
determinism
←──────────────→
variation
```

The artist can decide how much freedom exists inside the rule.

------------------------------------------------------------------------

# 66. Artistic Concept: Scale and Self-Similarity

Many L-system structures repeat related forms across scales.

This creates connections to:

-   fractals;
-   recursive ornament;
-   branching;
-   nested organization.

However, the Explorer should avoid teaching:

``` text
L-system = fractal
```

Not every L-system produces a fractal, and L-systems are fundamentally a
rewriting formalism.

Fractal geometry is one important possible outcome.

------------------------------------------------------------------------

# 67. Artistic Concept: Authorship

The artist does not necessarily design every branch.

Instead, the artist designs:

-   alphabet;
-   axiom;
-   rules;
-   interpretation;
-   constraints;
-   variation.

Authorship shifts from:

``` text
making the object
```

toward:

``` text
making the system that makes the object
```

This is central to generative art.

------------------------------------------------------------------------

# 68. Recommended Technical Architecture

``` text
Application
│
├── Grammar Engine
│   ├── parser
│   ├── deterministic rewriter
│   ├── stochastic rewriter
│   ├── validation
│   └── generation cache
│
├── Turtle Interpreter
│   ├── state
│   ├── stack
│   ├── commands
│   └── geometry output
│
├── Renderer
│   ├── Canvas
│   ├── overlays
│   ├── animation
│   └── export
│
├── Experiment State
│   ├── grammar
│   ├── turtle settings
│   ├── random seed
│   └── rendering settings
│
└── UI
    ├── grammar editor
    ├── timeline
    ├── controls
    ├── inspector
    └── presets
```

Use TypeScript if possible so grammar/rule structures remain explicit.

------------------------------------------------------------------------

# 69. Suggested Data Model

``` json
{
  "model": "d0l",
  "axiom": "X",
  "rules": {
    "X": "F+[[X]-X]-F[-FX]+X",
    "F": "FF"
  },
  "iterations": 5,
  "turtle": {
    "angle": 25,
    "segmentLength": 4,
    "startAngle": -90,
    "lineWidth": 1.2,
    "lengthScale": 1.0,
    "widthScale": 0.8
  },
  "random": {
    "seed": 12345,
    "angleJitter": 0,
    "lengthJitter": 0
  },
  "render": {
    "colorMode": "branchDepth",
    "fitToCanvas": true,
    "showNodes": false
  }
}
```

------------------------------------------------------------------------

# 70. Stochastic Rule Data Model

Instead of:

``` json
"F": "FF"
```

use:

``` json
"F": [
  {
    "probability": 0.5,
    "replacement": "F[+F]F"
  },
  {
    "probability": 0.3,
    "replacement": "F[-F]F"
  },
  {
    "probability": 0.2,
    "replacement": "FF"
  }
]
```

Validate that probabilities sum appropriately.

------------------------------------------------------------------------

# 71. Export

Useful exports:

-   PNG
-   SVG
-   generated string as TXT
-   grammar as JSON
-   full experiment JSON
-   animated GIF/WebM if implemented
-   geometry as SVG paths
-   optional OBJ/GLTF for future 3D mode

For an art/design student, **SVG export is especially valuable** because
generated structures can continue into Illustrator or other vector
workflows.

------------------------------------------------------------------------

# 72. Implementation Warnings

## Exponential growth

Never allow unrestricted iteration.

Display warnings before generating extremely large strings.

## Bracket validation

Ensure:

``` text
[
]
```

are balanced.

Otherwise stack underflow can occur.

## Grammar validation

Detect:

-   invalid syntax;
-   missing symbols;
-   malformed stochastic probabilities.

## Deterministic random seeds

Stochastic experiments should be reproducible.

## Separate rewriting from rendering

Do not entangle grammar expansion with Canvas drawing.

The same grammar should be renderable through:

-   Canvas;
-   SVG;
-   3D;

without rewriting the grammar engine.

## Cache generations

If the user moves from generation 6 back to generation 5, do not
recompute everything unnecessarily.

Store generated generations.

## Fit geometry after interpretation

Compute or estimate bounding box and scale/translate to fit the
viewport.

## Avoid assuming `F` is the only drawable symbol

Make the command map configurable.

------------------------------------------------------------------------

# 73. Recommended Minimum Viable Product

The first version should include:

1.  deterministic context-free L-system engine;
2.  editable axiom;
3.  editable production rules;
4.  iteration control;
5.  2D turtle renderer;
6.  `F`, `f`, `+`, `-`, `[`, `]`;
7.  angle control;
8.  segment-length control;
9.  generation timeline;
10. generated-string viewer;
11. rule presets;
12. growth animation;
13. fit-to-canvas;
14. pan and zoom;
15. branch-depth coloring;
16. stack visualization;
17. grammar validation;
18. symbol-count warning;
19. PNG export;
20. SVG export;
21. JSON import/export.

------------------------------------------------------------------------

# 74. Recommended Advanced Version

After the core works:

1.  stochastic rules;
2.  deterministic random seed;
3.  angle/length jitter;
4.  parametric L-systems;
5.  context-sensitive rules;
6.  branch tapering;
7.  leaves/flowers;
8.  tropism;
9.  image-guided growth;
10. rule mutation;
11. rule breeding;
12. side-by-side grammar comparison;
13. sound interaction;
14. camera/hand interaction;
15. environmental obstacles;
16. 3D turtle mode;
17. Three.js rendering;
18. hybrid algorithm connections.

------------------------------------------------------------------------

# 75. Suggested Experiments for the Student

## Experiment 1 --- One grammar, many angles

Keep:

``` text
axiom
rules
iterations
```

fixed.

Change only angle.

**Question:** How can one symbolic structure contain many different
visual identities?

------------------------------------------------------------------------

## Experiment 2 --- One-character mutation

Change one symbol in a production.

Example:

``` text
+
```

to:

``` text
-
```

or insert:

``` text
[]
```

**Question:** How large can the morphological effect of a tiny textual
change become?

------------------------------------------------------------------------

## Experiment 3 --- Growth as animation

Show generations 0--7 sequentially.

**Question:** Does viewing development change how the final image is
understood?

------------------------------------------------------------------------

## Experiment 4 --- Determinism vs stochasticity

Generate:

``` text
20 deterministic outputs
```

then:

``` text
20 stochastic outputs
```

**Question:** When does repetition begin to feel natural rather than
mechanical?

------------------------------------------------------------------------

## Experiment 5 --- Grammar portrait

Import a portrait as an environmental field.

Allow branches to grow according to image brightness.

**Question:** Can an image be represented indirectly as constraints on
growth?

------------------------------------------------------------------------

## Experiment 6 --- Draw the same grammar differently

Render identical generated strings as:

-   lines;
-   circles;
-   ribbons;
-   typography;
-   particles.

**Question:** Where does the visual identity reside: in the grammar or
in its interpretation?

------------------------------------------------------------------------

## Experiment 7 --- Reverse nature

Create a plant grammar.

Then render it with:

-   neon lines;
-   geometric blocks;
-   metallic 3D tubes;
-   typographic symbols.

**Question:** Does a developmental logic remain "natural" when its
material appearance is artificial?

------------------------------------------------------------------------

## Experiment 8 --- Growth against gravity

Introduce tropism.

Animate its direction.

**Question:** How does an external field negotiate with internal
developmental rules?

------------------------------------------------------------------------

# 76. A Signature Feature: Grammar Microscope

Select one branch in the rendered structure.

Show:

``` text
Produced by:
Generation 4
Symbol occurrence #284
Parent symbol:
X at Generation 3
Production:
X → F[+X][-X]
```

Then trace backward:

``` text
branch
← symbol
← parent production
← earlier generation
← axiom
```

This would let the user investigate the **genealogy of form**.

It is an unusually strong fit for an educational L-System Explorer.

------------------------------------------------------------------------

# 77. A Signature Feature: Rule Comparison

Two synchronized canvases:

``` text
A                              B
X → F[+X][-X]                  X → F[++X][--X]
```

Highlight the changed characters.

Render both with identical:

-   angle;
-   iterations;
-   length;
-   seed.

This reveals morphological sensitivity.

------------------------------------------------------------------------

# 78. A Signature Feature: Rule Mutation Explorer

Provide:

``` text
Mutate Slightly
Mutate Moderately
Mutate Wildly
```

Generate a grid of variants.

For each variant show:

``` text
changed rule
preview
```

The user can save interesting descendants.

This transforms grammar writing into visual search.

------------------------------------------------------------------------

# 79. Comparison with Reaction--Diffusion and Boids

## Reaction--Diffusion

Basic unit:

``` text
continuous concentration field
```

Main mechanism:

``` text
reaction + diffusion
```

Image arises through:

``` text
local field dynamics
```

## Boids

Basic unit:

``` text
moving agent
```

Main mechanism:

``` text
local perception + steering
```

Image/motion arises through:

``` text
collective interaction
```

## L-System

Basic unit:

``` text
symbol / module
```

Main mechanism:

``` text
parallel rewriting + interpretation
```

Image arises through:

``` text
developmental grammar
```

All three demonstrate emergence, but through fundamentally different
computational ideas:

``` text
Reaction–Diffusion → fields
Boids              → agents
L-Systems          → symbols / grammar
```

This distinction should be visible across the larger Algorithm Explorer
project.

------------------------------------------------------------------------

# 80. Instructions for an AI Coding Agent

> Build an interactive browser-based L-System Explorer for an art and
> design student. The application must function simultaneously as a
> technically clear grammar simulator, an educational visualization, and
> a creative generative-design instrument.
>
> Architect the system as two independent layers: a grammar/rewrite
> engine and a turtle/geometric interpreter. Do not couple string
> expansion directly to Canvas rendering.
>
> Begin with deterministic context-free L-systems. Support editable
> axiom and production rules, parallel rewriting, generation history,
> and standard 2D turtle commands including forward drawing, rotation,
> and stack-based branching.
>
> Make the relationship between symbolic rules and visible geometry
> explicit. Users should be able to inspect generated strings, move
> between generations, watch the turtle interpret commands, and
> understand `[` / `]` through a visible stack.
>
> The simulation/generative canvas should remain visually dominant. The
> interface should feel like a grammar laboratory or growth instrument
> rather than a generic settings dashboard.
>
> Include real-time controls for iteration depth, turn angle, segment
> length, line width, and rendering. Include presets, but always expose
> their underlying axiom and rules.
>
> Protect the browser from exponential string growth by monitoring
> symbol count and imposing configurable safety limits.
>
> Cache generations. Validate brackets and grammar syntax. Keep random
> experiments reproducible through seeded randomness.
>
> Prioritize SVG and JSON export in addition to PNG because the user is
> an art/design student and may continue editing generated geometry in
> other design software.
>
> After the deterministic core is stable, add stochastic productions,
> branch scaling/tapering, tropism, rule mutation, rule comparison,
> image-guided growth, and optional 3D rendering.
>
> A high-value educational feature is a synchronized
> grammar/string/geometry view. A high-value advanced feature is a
> "grammar microscope" that lets a user select a branch and trace it
> back through its parent production to earlier generations.

------------------------------------------------------------------------

# 81. Key Takeaways

1.  L-systems were introduced by Aristid Lindenmayer in 1968 as formal
    models of biological development.
2.  Their core mechanism is **parallel symbolic rewriting**.
3.  A basic system contains an alphabet, axiom, and production rules.
4.  The generated string and its visible rendering are conceptually
    separate.
5.  Turtle graphics provide a common bridge from symbols to geometry.
6.  Stack operations `[` and `]` make branching possible.
7.  Iteration depth, angle, production rules, axiom, segment length,
    scaling, and stochasticity strongly affect visible form.
8.  L-systems include deterministic, stochastic, context-sensitive,
    parametric, and 3D variants.
9.  They can generate plants and fractals, but should not be reduced to
    "a plant/fractal algorithm."
10. Their deeper idea is **developmental description**: describe how
    form changes rather than only what the final form looks like.
11. For generative art, L-systems shift authorship from drawing objects
    to designing grammars.
12. An effective Explorer should expose the complete causal chain:
    **rule → rewriting → generation → turtle action → geometry**.
13. One of the strongest artistic possibilities is to manipulate the
    grammar itself as visual material.
14. One of the strongest conceptual themes is the relationship between
    **language and image**.
15. One of the strongest cross-algorithm opportunities is to use
    L-system geometry as input to Reaction--Diffusion, Boids, or later
    Genetic Algorithm experiments.

------------------------------------------------------------------------

# 82. Selected Research Sources

## Foundational history and theory

**Aristid Lindenmayer --- "Mathematical Models for Cellular Interactions
in Development" I & II (1968).**\
The foundational work from which L-systems emerged. Lindenmayer
developed the formalism in connection with biological development and
cellular interaction.

**Journal of Theoretical Biology --- "Pillars of theoretical biology:
'Mathematical models for cellular interaction in development, I and II'"
(2025).**\
A modern retrospective on Lindenmayer's two 1968 papers and the
subsequent impact of L-systems on developmental modeling and formal
systems.\
https://doi.org/10.1016/j.jtbi.2025.112142

## Major visual/computational reference

**Przemysław Prusinkiewicz & Aristid Lindenmayer --- *The Algorithmic
Beauty of Plants* (1990).**\
Foundational text on graphical modeling with L-systems, trees,
herbaceous plants, phyllotaxis, organs, developmental animation,
cellular layers, and fractal properties.\
Springer: https://link.springer.com/book/10.1007/978-1-4613-8476-2\
Algorithmic Botany electronic edition:
https://www.algorithmicbotany.org/papers/

**Przemysław Prusinkiewicz & James Hanan --- *Lindenmayer Systems,
Fractals, and Plants*.**\
Important reference connecting L-systems with plant geometry, computer
graphics, and fractal interpretation.\
https://link.springer.com/book/10.1007/978-1-4757-1428-9

## L-system theory

**Grzegorz Rozenberg & Arto Salomaa --- mathematical theory of
L-systems.**\
Major formal-language research on parallel rewriting and L-system
theory.

**Rozenberg & Salomaa (eds.) --- *Lindenmayer Systems: Impacts on
Theoretical Computer Science, Computer Graphics, and Developmental
Biology*.**\
Documents the interdisciplinary influence of L-systems.\
https://link.springer.com/book/10.1007/978-3-642-58117-5

## Practical graphical interpretation

**SideFX Houdini --- L-System documentation.**\
Professional procedural-modeling reference showing string rewriting and
turtle interpretation as geometry-generation tools.\
https://www.sidefx.com/docs/houdini/nodes/sop/lsystem.html

**Algorithmic Botany --- publications archive.**\
Research publications and downloadable material from the University of
Calgary's Algorithmic Botany group.\
https://www.algorithmicbotany.org/papers/

## Generative design / architecture

**Vishal Singh & Ning Gu --- "Towards an integrated generative design
framework" (Design Studies, 2012).**\
Reviews L-systems alongside cellular automata, genetic algorithms, shape
grammars, and swarm intelligence as generative design techniques.\
https://doi.org/10.1016/j.destud.2011.06.001

## Creative coding / contemporary interaction

**Interactive Flower Garden --- L-System & Computer Vision.**\
A contemporary browser example combining an L-system plant structure
with Canvas rendering and MediaPipe hand tracking for interactive sway
and blooming.\
https://github.com/aayansheraz/interactive-flowers/

------------------------------------------------------------------------

# 83. Research Note

The numbered list in the user's prompt still contains terminology
inherited from the earlier Reaction--Diffusion task, including
"Reaction-Diffusion" and the "Gray-Scott model."

Those terms do not belong to L-system theory.

For technical accuracy, this research interprets the intended questions
as:

``` text
1. What are L-systems?
2. What is their historical/theoretical background?
3. What are their formal/computational principles?
4. How does rewriting and turtle interpretation work?
5. Which parameters affect visible morphology?
6. What are the main L-system families?
7. What visual structures can they generate?
8. How can they be implemented computationally?
9. How are they used in art/design/architecture/creative coding?
10. How can artists modify them?
11. Which controls should an Algorithm Explorer expose?
12. How do L-systems connect to emergence, nature, growth,
    transformation, repetition, and image-making?
```

The Gray--Scott model remains part of the separate Reaction--Diffusion
context document.

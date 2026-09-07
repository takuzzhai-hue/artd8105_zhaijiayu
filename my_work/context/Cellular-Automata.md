# Cellular Automata

## Deep Research Context Document for an Algorithm Explorer

**Intended use:** Technical and conceptual context for an AI coding
agent building an interactive web-based Algorithm Explorer for an art
and design student.\
**Primary focus:** cells, states, neighborhoods, synchronous update
rules, emergence, Conway's Game of Life, elementary cellular automata,
Life-like rules, totalistic/non-totalistic systems, probabilistic and
multi-state variants\
**Document emphasis:** local rule → repeated updates → spatial/temporal
pattern → emergent behavior → creative manipulation

------------------------------------------------------------------------

# 0. Research Plan and Suitability Check

## Proposed research plan

This research is organized in six layers.

### Layer 1 --- Historical and conceptual foundation

-   Define cellular automata (CA) as discrete dynamical systems.
-   Trace their roots through Stanislaw Ulam and John von Neumann's
    mid-20th-century work on self-reproduction and computation.
-   Examine John Conway's Game of Life (1970) as the most influential
    public example.
-   Examine Stephen Wolfram's systematic study of one-dimensional
    elementary cellular automata and his four behavioral classes.

### Layer 2 --- Formal/computational mechanism

-   Explain cells, grids/lattices, finite states, neighborhoods, local
    transition rules, discrete time, and synchronous updates.
-   Make the distinction between a local rule and global emergent
    behavior explicit.
-   Explain boundary conditions and why they affect visible outcomes.

### Layer 3 --- Major CA families

-   One-dimensional elementary cellular automata.
-   Conway's Game of Life and Life-like cellular automata.
-   Totalistic and outer-totalistic rules.
-   Non-totalistic rules.
-   Multi-state / generations cellular automata.
-   Probabilistic cellular automata.
-   Reversible and asynchronous variants.
-   Continuous-valued and related CA-like systems as advanced
    extensions.

### Layer 4 --- Parameters and implementation

-   Map rule choice, initial condition, density, neighborhood, state
    count, update scheme, boundary mode, randomness, grid size, and
    simulation speed to visible behavior.
-   Translate the model into browser-friendly data structures and update
    loops.
-   Discuss double buffering, typed arrays, Canvas/WebGL, performance,
    sparse grids, history, and reproducibility.

### Layer 5 --- Art/design experimentation

-   Treat the CA as an image-making system, not only a mathematical
    simulation.
-   Explore pixel aesthetics, textiles, tiling, typography, image
    seeding, sound, interaction, architecture, urbanism, erosion/growth,
    drawing tools, and hybrid systems.
-   Examine how artists can design rules, initial conditions,
    environments, and mappings rather than individual pixels.

### Layer 6 --- Algorithm Explorer specification

-   Make the causal chain visible: **cell + state + neighborhood + local
    rule + time → global pattern**
-   Provide an interactive rule editor, neighborhood editor, seed
    painter, timeline, cell inspector, pattern library, rule-space
    explorer, comparison view, statistics, and export.
-   Give special attention to Game of Life objects such as still lifes,
    oscillators, spaceships, guns, and methuselah-like long transients.

## Suitability check

This plan is highly suitable for the project because cellular automata
are among the clearest demonstrations of **emergence from local rules**.

The main learning goal should not be memorizing Conway's four rules. It
should be understanding that every cell only has access to a small local
neighborhood, yet repeated simultaneous updates can produce:

-   stability;
-   periodicity;
-   propagation;
-   apparent randomness;
-   long-lived structures;
-   self-organization;
-   computation.

For an art/design student, the Explorer should make it possible to move
continuously between:

``` text
drawing an initial image
        ↓
defining local relations
        ↓
letting the system transform the image
        ↓
observing emergent visual behavior
```

This makes CA both a technical model and an unusually direct
image-making instrument.

------------------------------------------------------------------------

# 1. What Is a Cellular Automaton?

A **cellular automaton** is a discrete computational system made from a
regular collection of cells.

Each cell:

1.  occupies a location in a grid or lattice;
2.  has one state chosen from a finite set;
3.  observes a defined local neighborhood;
4.  updates according to the same local rule;
5.  changes at discrete time steps.

A minimal conceptual model is:

``` text
GRID
+
CELL STATES
+
NEIGHBORHOOD
+
UPDATE RULE
+
TIME
=
CELLULAR AUTOMATON
```

For example, a cell may have only two states:

``` text
0 = off
1 = on
```

At each tick, its next state is determined from its current state and
nearby cells.

The surprising part is that extremely simple local rules can create
complex global structures.

------------------------------------------------------------------------

# 2. Cellular Automata Are Not Reaction--Diffusion

The original prompt contains terminology inherited from the
Reaction--Diffusion research.

Cellular automata and Reaction--Diffusion can both produce emergent
patterns, but their computational logic is different.

## Reaction--Diffusion

Usually works with:

``` text
continuous concentration fields
+
differential equations
+
reaction and diffusion
```

## Cellular Automata

Usually works with:

``` text
discrete cells
+
discrete states
+
local transition rules
+
discrete time
```

The Gray--Scott model therefore belongs to the Reaction--Diffusion
document, not this one.

------------------------------------------------------------------------

# 3. Historical Background

## 3.1 Stanislaw Ulam

In the 1940s and 1950s, mathematician Stanislaw Ulam investigated
systems in which simple local interactions on grids could generate
complex patterns.

His interest in discrete spatial systems helped form the intellectual
environment from which cellular automata emerged.

## 3.2 John von Neumann

John von Neumann was interested in a profound question:

> Can a machine reproduce itself?

He developed a theoretical self-reproducing automaton on a cellular
grid.

His construction was far more complicated than Conway's later Game of
Life, but it established a foundational connection among:

-   local computation;
-   self-reproduction;
-   artificial life;
-   universal computation.

The history of Conway's Life is directly connected to von Neumann's
self-reproducing-machine problem.

## 3.3 John Conway and the Game of Life

British mathematician John Horton Conway devised the **Game of Life** in
1970.

It became widely known after Martin Gardner introduced it in the October
1970 issue of *Scientific American*.

Life is a **zero-player game**:

``` text
choose an initial configuration
↓
start the simulation
↓
the rules determine everything afterward
```

Its popularity helped establish cellular automata as an accessible way
to explore:

-   emergence;
-   complexity;
-   artificial life;
-   computation.

## 3.4 Stephen Wolfram

Beginning in the early 1980s, Stephen Wolfram systematically studied
very simple one-dimensional cellular automata.

He showed that extremely small rule tables can produce behavior ranging
from uniformity to apparent chaos and complex localized structures.

His 1984 paper **"Universality and Complexity in Cellular Automata"**
proposed four broad behavioral classes.

This work made **rule space** itself an object of investigation.

------------------------------------------------------------------------

# 4. The Five Core Components

A cellular automaton can be understood through five questions.

## 4.1 Where are the cells?

Examples:

``` text
1D line
2D square grid
hexagonal grid
triangular grid
3D lattice
graph/network
```

## 4.2 What states can a cell have?

Binary:

``` text
0 / 1
dead / alive
black / white
```

Multi-state:

``` text
0, 1, 2, 3, ...
```

States can represent:

-   age;
-   species;
-   material;
-   energy;
-   color;
-   occupancy;
-   phase.

## 4.3 Which cells count as neighbors?

The **neighborhood** defines local perception.

## 4.4 What is the update rule?

The rule maps:

``` text
current local configuration
→
next cell state
```

## 4.5 How does time advance?

Most classic CAs use synchronous discrete generations:

``` text
t
↓
calculate every next state
↓
replace entire grid
↓
t + 1
```

------------------------------------------------------------------------

# 5. Formal Model

A CA can be represented abstractly by:

\[ s_i(t+1)=F(N_i(t)) \]

where:

-   (s_i(t+1)) is the next state of cell (i);
-   (N_i(t)) is the neighborhood configuration around cell (i) at time
    (t);
-   \(F\) is the local transition rule.

The key point is that:

``` text
the same F
```

is generally applied everywhere.

Complexity therefore does not require each location to have a
complicated unique instruction.

------------------------------------------------------------------------

# 6. Cells

A **cell** is the smallest spatial unit of the automaton.

In a browser implementation, a 2D binary grid might conceptually be:

``` text
0 0 0 1 0
0 1 1 0 0
0 1 0 0 1
0 0 0 0 0
```

Each value is a cell state.

For visualization:

``` text
0 → empty / white
1 → filled / black
```

But the state does not have to correspond directly to a color.

The renderer can map state to:

-   color;
-   shape;
-   texture;
-   glyph;
-   sound;
-   geometry.

This separation is important for creative use.

------------------------------------------------------------------------

# 7. States

## Binary states

The simplest form:

``` text
S = {0,1}
```

Examples:

-   dead/alive;
-   empty/occupied;
-   white/black.

## Multiple states

Example:

``` text
S = {0,1,2,3,4}
```

These can represent:

``` text
dead
newborn
young
mature
decaying
```

A multi-state CA can therefore encode temporal traces inside each cell.

This is extremely useful for visual art.

------------------------------------------------------------------------

# 8. Neighborhoods

The neighborhood defines which nearby cells influence a cell's next
state.

This is one of the most important parameters.

------------------------------------------------------------------------

# 9. Moore Neighborhood

For a square grid, the Moore neighborhood includes the eight surrounding
cells:

``` text
x x x
x C x
x x x
```

`C` is the center cell.

This is used by Conway's Game of Life.

Radius 1:

``` text
8 neighbors
```

Larger radii are possible.

------------------------------------------------------------------------

# 10. von Neumann Neighborhood

The von Neumann neighborhood uses the four orthogonally adjacent cells:

``` text
  x
x C x
  x
```

This often creates more axis-aligned or diamond-like propagation.

Comparing Moore and von Neumann neighborhoods with the same conceptual
rule can produce dramatically different visual structures.

------------------------------------------------------------------------

# 11. Extended Neighborhoods

Artists can define unusual neighborhoods:

``` text
x . . . x
. x . x .
. . C . .
. x . x .
x . . . x
```

or directional neighborhoods:

``` text
x x x
. C .
. . .
```

or arbitrary masks.

The neighborhood itself can become a drawing tool.

A strong Explorer should therefore include a **Neighborhood Editor**
rather than only a dropdown.

------------------------------------------------------------------------

# 12. Synchronous Updating

Classic CAs usually update simultaneously.

Suppose:

``` text
OLD GRID
```

is read to calculate every cell.

All results go into:

``` text
NEW GRID
```

Only after every next state is calculated do we swap them.

Correct implementation:

``` text
currentGrid
    ↓
calculate
    ↓
nextGrid
    ↓
swap
```

Do not update the current grid in place, because later cells would then
see partially updated neighbors.

This is called **double buffering**.

------------------------------------------------------------------------

# 13. Boundary Conditions

Finite computer screens require a decision about edges.

## Fixed / dead boundary

Cells outside the grid are always state 0.

Visual effect:

-   patterns may disappear at edges.

## Wrap / toroidal boundary

Left connects to right.

Top connects to bottom.

Conceptually:

``` text
screen = surface of a torus
```

Visual effect:

-   spaceships re-enter from the opposite side;
-   no hard boundary.

## Reflective boundary

Edges mirror values.

## Infinite / sparse grid

Store only active cells.

Useful for large Life patterns.

Boundary conditions are not merely technical---they change the world the
automaton inhabits.

------------------------------------------------------------------------

# 14. Conway's Game of Life

The Game of Life uses:

``` text
2D square grid
binary states
Moore neighborhood
synchronous updates
```

Each cell has eight neighbors.

The rule is commonly written:

``` text
B3/S23
```

Meaning:

``` text
Birth:
a dead cell becomes alive with exactly 3 live neighbors

Survival:
a live cell survives with 2 or 3 live neighbors
```

Everything else becomes or remains dead.

------------------------------------------------------------------------

# 15. Game of Life Rules Step by Step

For every cell:

## Rule 1 --- Underpopulation

If alive and fewer than 2 neighbors are alive:

``` text
dies
```

## Rule 2 --- Survival

If alive and 2 or 3 neighbors are alive:

``` text
survives
```

## Rule 3 --- Overpopulation

If alive and more than 3 neighbors are alive:

``` text
dies
```

## Rule 4 --- Birth

If dead and exactly 3 neighbors are alive:

``` text
becomes alive
```

Then all calculated changes are applied simultaneously.

------------------------------------------------------------------------

# 16. Game of Life Pseudocode

``` text
for y in grid:
    for x in grid:

        neighbors = countLiveNeighbors(x, y)

        if current[x,y] == ALIVE:

            if neighbors == 2 or neighbors == 3:
                next[x,y] = ALIVE
            else:
                next[x,y] = DEAD

        else:

            if neighbors == 3:
                next[x,y] = ALIVE
            else:
                next[x,y] = DEAD

swap(current, next)
```

------------------------------------------------------------------------

# 17. Life-like Rule Notation

Life-like cellular automata often use:

``` text
B.../S...
```

where:

-   `B` = birth neighbor counts;
-   `S` = survival neighbor counts.

Conway Life:

``` text
B3/S23
```

HighLife:

``` text
B36/S23
```

This small rule change allows very different behavior, including famous
replicator structures in HighLife.

An Explorer should make B/S rule editing extremely easy.

------------------------------------------------------------------------

# 18. Why Game of Life Is Important

Life is important not because its four verbal rules are complicated.

It is important because those rules can produce:

-   still lifes;
-   oscillators;
-   spaceships;
-   guns;
-   puffers;
-   long-lived transients;
-   logic structures;
-   universal computation.

The system demonstrates the central CA principle:

> Global organization does not need to be explicitly written into the
> local rule.

------------------------------------------------------------------------

# 19. Still Lifes

A still life does not change from one generation to the next.

Example:

``` text
Block

■■
■■
```

It is a stable local configuration.

Conceptually:

``` text
dynamic system
→
stable image
```

------------------------------------------------------------------------

# 20. Oscillators

An oscillator cycles through a repeating sequence.

Example:

``` text
Blinker

Generation A:
■■■

Generation B:
 ■
 ■
 ■
```

Then back again.

The image becomes temporal.

A CA image may therefore be understood as a **loop**, not a static
composition.

------------------------------------------------------------------------

# 21. Spaceships

A spaceship repeats its shape while translating across the grid.

The most famous example is the **glider**.

Conceptually:

``` text
pattern
+
periodic transformation
=
movement
```

No cell itself travels across the entire screen.

Instead, cells turn on and off in a coordinated way that creates the
appearance of a moving object.

This is a profound example of emergent identity.

------------------------------------------------------------------------

# 22. Guns

A gun is a stationary or periodic structure that repeatedly emits
spaceships.

The **Gosper glider gun** is one of the most famous Life patterns.

It demonstrates:

``` text
local rule
→
stable mechanism
→
repeated production of moving structures
```

This makes Life feel less like a pixel effect and more like a mechanical
ecology.

------------------------------------------------------------------------

# 23. Methuselahs and Long Transients

Some tiny initial configurations evolve for a surprisingly long time
before stabilizing.

These are often called **methuselahs** in the Life community.

They are artistically interesting because:

``` text
small seed
→
long unpredictable history
→
large spatial transformation
```

An Explorer should include several long-transient presets.

------------------------------------------------------------------------

# 24. Elementary Cellular Automata

An **Elementary Cellular Automaton (ECA)** is one of the simplest CA
families.

It has:

``` text
1 dimension
2 states
radius-1 neighborhood
```

Each cell observes:

``` text
left
center
right
```

There are:

\[ 2\^3 = 8 \]

possible neighborhood configurations.

Each configuration can map to either 0 or 1.

Therefore there are:

\[ 2\^8 = 256 \]

possible rules.

These are numbered:

``` text
Rule 0
...
Rule 255
```

------------------------------------------------------------------------

# 25. How a 1D CA Becomes a 2D Image

The automaton itself is one-dimensional.

Example generation:

``` text
000010000
```

The next generation is another row.

To visualize history, stack generations vertically:

``` text
time
↓

    ■
   ■■■
  ■■  ■
 ■■■■■■■
...
```

Therefore the image's vertical axis is **time**.

This is conceptually important:

> A 2D ECA image is often a visualization of the history of a 1D world.

------------------------------------------------------------------------

# 26. Rule Number Encoding

For an ECA, list neighborhoods:

``` text
111
110
101
100
011
010
001
000
```

Suppose outputs are:

``` text
0 0 0 1 1 1 1 0
```

Binary:

``` text
00011110
```

Decimal:

``` text
30
```

Therefore this is:

``` text
Rule 30
```

A rule-number explorer should show the binary rule table, not just the
number.

------------------------------------------------------------------------

# 27. Rule 30

Rule 30 is famous for producing complex, apparently irregular patterns
from extremely simple initial conditions.

It is commonly associated with Wolfram's Class 3 behavior.

From a single active cell, it produces a triangular history with a
mixture of:

-   recognizable local structures;
-   asymmetry;
-   apparent randomness.

For artists, it demonstrates:

``` text
deterministic rule
≠
visually predictable result
```

------------------------------------------------------------------------

# 28. Rule 90

Rule 90 produces a highly regular fractal structure closely related to
the Sierpiński triangle.

This makes it a useful comparison against Rule 30.

Same basic CA framework:

``` text
binary
1D
nearest neighbors
```

but a different rule produces radically different image logic.

------------------------------------------------------------------------

# 29. Rule 110

Rule 110 produces a mixture of repetitive backgrounds and interacting
localized structures.

It is a classic example associated with Wolfram's Class 4 behavior and
is capable of universal computation.

For an Explorer, Rule 110 is valuable because it sits visually between:

``` text
order
and
chaos
```

------------------------------------------------------------------------

# 30. Wolfram's Four Behavioral Classes

Stephen Wolfram proposed four broad classes for CA behavior.

These are qualitative categories, not perfectly sharp universal laws.

## Class 1 --- Uniform

Evolution approaches a homogeneous state.

Visual feeling:

``` text
extinction
silence
blankness
```

## Class 2 --- Stable / periodic

Evolution produces stable or repeating structures.

Visual feeling:

``` text
order
texture
rhythm
```

## Class 3 --- Chaotic

Evolution remains irregular or pseudo-random.

Visual feeling:

``` text
noise
turbulence
unpredictability
```

## Class 4 --- Complex localized structures

Stable/periodic regions coexist with moving or interacting structures.

Visual feeling:

``` text
organized complexity
```

This classification is an excellent educational lens for the Explorer.

------------------------------------------------------------------------

# 31. Totalistic Cellular Automata

A **totalistic** rule depends on the total sum of states in the
neighborhood.

It does not care where those states occur.

Example:

``` text
if neighbor sum = 3:
    turn on
```

This compresses many local configurations into one count.

------------------------------------------------------------------------

# 32. Outer-Totalistic Cellular Automata

Conway's Life is commonly described as **outer-totalistic**.

The rule considers:

1.  the center cell's current state;
2.  the total number of active surrounding neighbors.

It does not distinguish spatial arrangements with the same neighbor
count.

Thus these two neighborhoods may be equivalent to the rule:

``` text
■ ■ .
. C .
. ■ .

and

■ . ■
. C .
. ■ .
```

if both contain three active neighbors.

------------------------------------------------------------------------

# 33. Non-Totalistic Cellular Automata

A non-totalistic rule can distinguish **where** neighbors are located.

Example:

``` text
north + east neighbors
```

may behave differently from:

``` text
south + west neighbors
```

even if both have two live neighbors.

This dramatically expands rule space.

Artistically, it allows:

-   directionality;
-   chirality;
-   anisotropy;
-   wind-like effects;
-   directional growth.

------------------------------------------------------------------------

# 34. Multi-State Cellular Automata

Instead of:

``` text
dead / alive
```

use:

``` text
0 dead
1 newborn
2 active
3 fading
4 refractory
```

This creates visible trails and life cycles.

A common creative pattern is:

``` text
active
→
decay 1
→
decay 2
→
dead
```

The state history becomes visible as color.

------------------------------------------------------------------------

# 35. Generations-Type Rules

A useful multi-state family extends Life-like birth/survival rules with
decaying states.

Conceptually:

``` text
dead
↓ birth
alive
↓ death
decay 1
↓
decay 2
↓
...
↓
dead
```

This can produce:

-   waves;
-   glowing trails;
-   cyclic textures;
-   organic propagation.

Very useful for an art-oriented Explorer.

------------------------------------------------------------------------

# 36. Probabilistic Cellular Automata

Rules do not always need deterministic outputs.

Example:

``` text
if 3 neighbors:
    become alive with probability 0.8
```

Now identical initial states can produce different futures.

This introduces:

``` text
chance
inside
local law
```

Controls:

-   probability;
-   noise;
-   random seed.

------------------------------------------------------------------------

# 37. Asynchronous Cellular Automata

Classic CA updates all cells synchronously.

An asynchronous variant may update:

-   one cell at a time;
-   random subsets;
-   cells in random order.

This changes the dynamics.

It can produce less rigid temporal structures.

Artistically:

``` text
shared clock
vs
individual timing
```

becomes an experimental variable.

------------------------------------------------------------------------

# 38. Reversible Cellular Automata

Some CA rules are designed so that previous states can be reconstructed
from later states.

This introduces questions about:

-   reversibility;
-   memory;
-   entropy;
-   time direction.

A reversible mode could be an advanced Explorer feature.

------------------------------------------------------------------------

# 39. Grid Geometry

The lattice need not be square.

Possible geometries:

## Square

Most familiar.

## Hexagonal

Each cell naturally has six adjacent neighbors.

Can create more isotropic growth.

## Triangular

Different directional relationships.

## 3D cubic lattice

Produces volumetric cellular structures.

## Graph-based

Cells exist on arbitrary networks.

This moves beyond traditional visual CA but preserves local-rule logic.

------------------------------------------------------------------------

# 40. Most Important Parameters

Unlike algorithms with a few numeric parameters, CA behavior is strongly
controlled by **structural parameters**.

The most important are:

1.  update rule;
2.  initial condition;
3.  neighborhood;
4.  number of states;
5.  grid geometry;
6.  boundary condition;
7.  update timing;
8.  randomness;
9.  grid resolution;
10. simulation speed.

------------------------------------------------------------------------

# 41. Rule Choice

This is the deepest parameter.

Changing:

``` text
B3/S23
```

to:

``` text
B36/S23
```

changes only one birth condition.

Yet the system's possible structures change.

Similarly:

``` text
Rule 30
Rule 90
Rule 110
```

use the same basic ECA architecture but produce radically different
histories.

The rule should therefore be treated as editable creative material.

------------------------------------------------------------------------

# 42. Initial Condition

The same rule can behave very differently from different starting
states.

Possible seeds:

``` text
single cell
random noise
hand drawing
text
photograph
preset pattern
symmetrical seed
imported bitmap
```

This creates an important artistic relationship:

``` text
rule
vs
initial image
```

Which one determines the result more strongly?

------------------------------------------------------------------------

# 43. Initial Density

For random initialization:

``` text
density = probability a cell starts alive
```

Low density:

-   isolated structures;
-   empty space;
-   sparse interactions.

High density:

-   overcrowding;
-   rapid collisions;
-   dense texture.

A density slider is essential.

------------------------------------------------------------------------

# 44. Neighborhood Radius

Increasing neighborhood radius gives each cell access to more
surrounding information.

Effects may include:

-   larger-scale structures;
-   smoother or more global behavior;
-   new symmetries;
-   different propagation speeds.

But the exact visual effect depends on the rule.

------------------------------------------------------------------------

# 45. State Count

More states allow cells to carry more history.

Binary:

``` text
on/off
```

Multi-state:

``` text
birth/growth/decay/refractory
```

Visually this enables:

-   trails;
-   gradients;
-   age maps;
-   material transformations.

------------------------------------------------------------------------

# 46. Update Speed

Simulation speed does not change the mathematical sequence in
synchronous deterministic CA, but it changes human perception.

Slow:

``` text
cell-by-cell causality becomes legible
```

Fast:

``` text
the system becomes texture / motion
```

The Explorer should support both.

------------------------------------------------------------------------

# 47. Grid Resolution

Large cells:

-   easy to inspect;
-   emphasizes pixel/grid structure.

Tiny cells:

-   reveals macro-patterns;
-   makes the CA resemble a continuous field.

This creates a useful perceptual transition:

``` text
cellular
←────────→
field-like
```

------------------------------------------------------------------------

# 48. Boundary Mode

A glider reaching a fixed edge disappears.

On a torus, it returns from the opposite side.

Therefore the boundary defines the topology of the simulated world.

The Explorer should make boundary mode visible and understandable.

------------------------------------------------------------------------

# 49. Randomness

Randomness can enter through:

-   initial state;
-   probabilistic rules;
-   asynchronous timing;
-   mutation of rules.

These should be separate controls.

A deterministic rule with random initial conditions is conceptually
different from a probabilistic rule.

------------------------------------------------------------------------

# 50. Typical Visual Pattern Families

Cellular automata can generate:

-   uniform fields;
-   stripes;
-   checker-like textures;
-   fractals;
-   branching structures;
-   waves;
-   domains;
-   oscillators;
-   moving particles;
-   gliders;
-   fronts;
-   spirals;
-   pseudo-random noise;
-   crystalline structures;
-   labyrinths;
-   long transient explosions;
-   repeating motifs;
-   self-reproducing structures;
-   computational patterns.

There is no single "CA aesthetic."

The aesthetic arises from the relationship among:

``` text
rule
+
seed
+
neighborhood
+
visual mapping
```

------------------------------------------------------------------------

# 51. Computational Implementation

Recommended first implementation:

``` text
TypeScript / JavaScript
+
HTML Canvas
```

For large grids:

``` text
TypedArray
+
Canvas ImageData
```

or later:

``` text
WebGL / GPU
```

The architecture should separate:

``` text
CA Engine
from
Renderer
```

------------------------------------------------------------------------

# 52. Recommended Data Representation

For binary CA:

``` text
Uint8Array(width * height)
```

Index:

``` text
index = y * width + x
```

This is generally faster and simpler than nested JavaScript arrays.

Maintain:

``` text
current
next
```

buffers.

------------------------------------------------------------------------

# 53. Double-Buffer Update

``` text
function step():

    for each cell:
        neighborhood = read(current)
        next[cell] = rule(current[cell], neighborhood)

    swap(current, next)
```

Never read from `next` while calculating the same generation.

------------------------------------------------------------------------

# 54. Game of Life Implementation

``` text
function nextLifeState(currentState, liveNeighbors):

    if currentState == 1:
        return (
            liveNeighbors == 2 ||
            liveNeighbors == 3
        ) ? 1 : 0

    return liveNeighbors == 3 ? 1 : 0
```

Represent birth and survival sets:

``` text
birth = {3}
survival = {2,3}
```

This makes arbitrary Life-like rules easy.

------------------------------------------------------------------------

# 55. Generic Life-Like Implementation

``` text
function nextState(alive, neighbors, birthSet, survivalSet):

    if alive:
        return survivalSet.has(neighbors) ? 1 : 0
    else:
        return birthSet.has(neighbors) ? 1 : 0
```

The UI can directly manipulate `birthSet` and `survivalSet`.

------------------------------------------------------------------------

# 56. ECA Implementation

For each cell:

``` text
left
center
right
```

convert neighborhood to binary index:

``` text
111 → 7
110 → 6
...
000 → 0
```

Then read the corresponding bit from the rule number.

Conceptually:

``` text
output = (ruleNumber >> neighborhoodIndex) & 1
```

This allows all 256 elementary rules with one integer.

------------------------------------------------------------------------

# 57. Performance

A 1000 × 1000 grid contains:

``` text
1,000,000 cells
```

At 60 steps per second:

``` text
60 million cell updates / second
```

plus neighborhood reads and rendering.

Optimization strategies:

-   typed arrays;
-   avoid object allocation per cell;
-   precompute neighbor indices when useful;
-   update only when needed;
-   separate simulation rate from render rate;
-   use ImageData for pixel rendering;
-   use Web Workers;
-   use WebGL/GPU for advanced versions;
-   use sparse sets for sparse infinite Life worlds.

------------------------------------------------------------------------

# 58. Sparse Representation

Game of Life often contains huge empty regions.

Instead of storing every cell, store only live cells:

``` text
Set<coordinate>
```

To calculate next generation:

1.  visit live cells;
2.  count their neighboring candidate cells;
3.  evaluate only potentially active positions.

This is useful for:

-   large spaces;
-   glider guns;
-   infinite-grid exploration.

For a beginner Explorer, dense arrays are simpler.

Sparse mode can be advanced.

------------------------------------------------------------------------

# 59. Rendering

## Pixel mode

One cell = one square.

Best for teaching.

## Smooth mode

Interpolate or blur cells.

Makes patterns feel field-like.

## Glyph mode

Map states to:

``` text
letters
symbols
icons
```

## Shape mode

Cells become:

``` text
circles
triangles
lines
```

## Height mode

State becomes 3D height.

## Trail mode

Color cells by age or last activation time.

The renderer should be swappable without changing the CA engine.

------------------------------------------------------------------------

# 60. Generative Art

Cellular automata are natural generative-art systems because the artist
defines local relationships and then allows the image to develop
autonomously.

The artist can control:

``` text
rules
initial conditions
states
neighborhood
mapping
intervention
```

rather than manually drawing the final pattern.

The work can exist as:

-   final frame;
-   animation;
-   print;
-   interactive installation;
-   continuously evolving screen;
-   data source for another medium.

------------------------------------------------------------------------

# 61. Pixel Aesthetics

Because CA are explicitly cellular, they connect naturally to:

-   pixel art;
-   digital grids;
-   mosaics;
-   weaving;
-   cross-stitch;
-   LED matrices;
-   tile systems.

The grid does not need to be hidden.

It can become the visual language.

------------------------------------------------------------------------

# 62. Textile and Pattern Design

CA histories can be translated into repeating surfaces.

For example:

``` text
1D CA history
→
2D textile pattern
```

Rule 90 can create fractal triangular motifs.

Rule 30 can create asymmetric irregular texture.

Life-like systems can generate evolving motifs sampled at selected
times.

Possible outputs:

-   fabric;
-   wallpaper;
-   ceramic tile;
-   knitting patterns;
-   jacquard-like grids.

------------------------------------------------------------------------

# 63. Architecture and Urbanism

Cellular automata have been investigated as generative systems in
architecture and urban design.

Researchers have adapted CA to:

-   spatial allocation;
-   building growth;
-   urban expansion;
-   façade systems;
-   modular aggregation;
-   design-space exploration.

A key issue in architectural CA research is **control**.

Purely generic CA behavior is often insufficient for specific design
tasks.

Architectural applications typically introduce:

-   constraints;
-   goals;
-   designer intervention;
-   environmental feedback;
-   modified neighborhoods;
-   heterogeneous rules.

Recent research emphasizes interactive feedback and control strategies
rather than treating CA as an autonomous form generator.

------------------------------------------------------------------------

# 64. Artistic Experiment: Paint the Seed

Let the user paint live cells directly.

Tools:

``` text
brush
eraser
line
rectangle
spray
symmetry
text stamp
```

Then press:

``` text
RUN
```

The drawing becomes an initial condition rather than a final image.

This is probably the most intuitive creative entry point.

------------------------------------------------------------------------

# 65. Artistic Experiment: Image as Initial Condition

Import a photograph.

Convert brightness to cell states:

``` text
dark → alive
light → dead
```

or use threshold controls.

Then evolve.

The photograph is no longer preserved as a representation.

It becomes **material for a rule-driven transformation**.

------------------------------------------------------------------------

# 66. Artistic Experiment: Typography

Render text into the grid.

Example:

``` text
"ALIVE"
```

Then apply Life or another rule.

The word may:

-   dissolve;
-   stabilize;
-   fragment;
-   emit moving structures.

This creates a relationship between semantic language and cellular
transformation.

------------------------------------------------------------------------

# 67. Artistic Experiment: Rule Morphing

Interpolate or switch between rules over time.

For Life-like rules:

``` text
B3/S23
↓
B36/S23
↓
another rule
```

The world changes its physical laws while it is running.

Conceptual question:

> What happens to an organism when the rules of its world change?

------------------------------------------------------------------------

# 68. Artistic Experiment: Neighborhood Drawing

Allow the artist to draw the neighborhood mask.

Example:

``` text
■ . ■
. C .
■ . ■
```

Then create a rule based on neighbor count or pattern.

The artist is literally designing what a cell is capable of perceiving.

This is conceptually powerful.

------------------------------------------------------------------------

# 69. Artistic Experiment: Directional World

Use an asymmetric neighborhood:

``` text
x x x
. C .
. . .
```

Cells only respond to information "above."

This can produce directional flow.

It creates a world with a built-in orientation.

------------------------------------------------------------------------

# 70. Artistic Experiment: Aging Cells

Use states:

``` text
0 = dead
1 = newborn
2 = young
3 = mature
4 = fading
```

Color each age differently.

The grid becomes a temporal painting.

Every cell contains a small history.

------------------------------------------------------------------------

# 71. Artistic Experiment: Memory

Give cells memory of previous states.

Example:

``` text
next state depends on:
current neighbors
+
cell state 2 frames ago
```

This breaks the simplest Markov-like CA assumption and creates richer
temporal behavior.

Concept:

``` text
local memory
→
global history
```

------------------------------------------------------------------------

# 72. Artistic Experiment: Probabilistic Life

Start from Life:

``` text
B3/S23
```

but make birth probability:

``` text
80%
```

or survival imperfect.

Now the familiar Life world becomes unstable.

The difference between:

``` text
law
and
chance
```

becomes visible.

------------------------------------------------------------------------

# 73. Artistic Experiment: Human Intervention

Allow drawing while the simulation runs.

The user can:

-   add cells;
-   erase cells;
-   inject gliders;
-   change rules;
-   paint obstacles.

The artwork becomes a negotiation:

``` text
human gesture
vs
autonomous system
```

------------------------------------------------------------------------

# 74. Artistic Experiment: Sound

Map CA activity to sound.

Possible mappings:

``` text
live cell count → volume
birth rate → percussion
x position → pitch
state → instrument
pattern collision → trigger
```

Or reverse it:

``` text
audio amplitude
→
birth probability
```

The CA becomes audiovisual.

------------------------------------------------------------------------

# 75. Artistic Experiment: Camera / Body Input

Use webcam data as the initial grid or continuous intervention field.

Examples:

``` text
silhouette → live cells
motion → births
hand position → neighborhood center
face → seed
```

The participant becomes part of the automaton's environment.

------------------------------------------------------------------------

# 76. Artistic Experiment: CA as Drawing Machine

Do not display cells directly.

Instead:

``` text
birth → draw line
death → erase
oscillation → stamp circle
glider → move brush
```

The CA becomes a hidden process controlling another image.

This separates:

``` text
simulation
from
visual output
```

------------------------------------------------------------------------

# 77. Artistic Experiment: Rule Mutation

Take a CA rule and randomly alter one output.

For an ECA:

``` text
Rule 30
```

flip one bit in its 8-bit rule table.

Compare the new pattern.

For Life-like systems:

``` text
add/remove one B or S count
```

This reveals the sensitivity of global behavior to tiny local-rule
changes.

------------------------------------------------------------------------

# 78. Artistic Experiment: Rule Space Atlas

Generate thumbnails for:

``` text
Rule 0–255
```

using the same initial condition.

Arrange them as a grid.

Users can visually browse the entire elementary rule space.

Sort by:

-   rule number;
-   estimated entropy;
-   symmetry;
-   density;
-   Wolfram class;
-   visual similarity.

This would be a signature feature.

------------------------------------------------------------------------

# 79. Artistic Experiment: Seed Atlas

Keep one rule fixed.

Generate hundreds of different seeds.

Compare their outcomes.

This reverses the Rule Atlas:

``` text
same law
different beginnings
```

Question:

> Is complexity in the rule or in the initial condition?

------------------------------------------------------------------------

# 80. Artistic Experiment: Boundary Worlds

Run identical seeds simultaneously with:

``` text
fixed
wrap
reflective
```

boundaries.

The results gradually diverge.

The edge becomes part of the artwork's ontology.

------------------------------------------------------------------------

# 81. Artistic Experiment: Different Lattices

Run conceptually similar rules on:

``` text
square
hexagonal
triangular
```

grids.

Question:

> How much does geometry determine behavior before any "artistic"
> decision is made?

------------------------------------------------------------------------

# 82. Artistic Experiment: Cellular Material

Map states to material categories:

``` text
empty
wood
glass
metal
vegetation
```

Rules control transformation between materials.

This can become:

-   façade studies;
-   voxel sculptures;
-   speculative architecture;
-   material ecologies.

------------------------------------------------------------------------

# 83. Artistic Experiment: CA + Reaction--Diffusion

Use CA cells as seeds for Reaction--Diffusion.

Pipeline:

``` text
CA
→
discrete structure
→
RD
→
continuous organic texture
```

Or threshold an RD field into CA states.

This creates a dialogue between:

``` text
discrete
and
continuous
```

------------------------------------------------------------------------

# 84. Artistic Experiment: CA + Boids

Use live cells as:

-   obstacles;
-   food;
-   attractors.

Boids can modify the grid as they move.

Example:

``` text
boid passes cell
→
cell becomes alive
```

Then CA evolution transforms the trail.

------------------------------------------------------------------------

# 85. Artistic Experiment: CA + L-System

Use L-system geometry to initialize the CA grid.

``` text
branch drawing
→
rasterized cells
→
cellular evolution
```

The developmental skeleton can:

-   dissolve;
-   propagate;
-   stabilize;
-   mutate.

------------------------------------------------------------------------

# 86. Artistic Experiment: CA + Genetic Algorithm

Use a Genetic Algorithm to evolve:

``` text
CA rule
initial seed
neighborhood
```

Fitness can be:

``` text
user aesthetic preference
```

The GA searches cellular rule space.

This is one of the strongest cross-algorithm possibilities for the
complete Algorithm Explorer.

------------------------------------------------------------------------

# 87. Recommended Interactive Controls

## World

-   Grid Width
-   Grid Height
-   Cell Size
-   Grid Geometry
-   Boundary Mode
-   Background

## State

-   Number of States
-   State Colors
-   State Meaning
-   Decay Steps

## Neighborhood

-   Moore
-   von Neumann
-   Radius
-   Custom Neighborhood Editor
-   Include/Exclude Center

## Rule

-   Game of Life preset
-   B/S Rule Editor
-   ECA Rule Number 0--255
-   Binary Rule Table
-   Custom Transition Table
-   Probabilistic Rule Values

## Initial Condition

-   Clear
-   Randomize
-   Density
-   Single Cell
-   Pattern Presets
-   Draw
-   Upload Image
-   Text Seed
-   Random Seed

## Time

-   Step
-   Play
-   Pause
-   Speed
-   Rewind
-   Generation
-   Record History

## Visualization

-   Cell Color
-   Color by Age
-   Color by State
-   Trails
-   Grid Lines
-   Smooth Mode
-   Heatmap
-   Activity Overlay

------------------------------------------------------------------------

# 88. Essential Feature: Cell Inspector

Hover or click a cell.

Show:

``` text
Position:
(42, 18)

Current State:
1

Neighbors:
3

Neighborhood:
0 1 0
1 1 0
0 1 0

Rule Result:
1 → 1

Reason:
Survival with 3 neighbors
```

Then step one generation.

This makes local causality visible.

------------------------------------------------------------------------

# 89. Essential Feature: Neighborhood Inspector

Highlight the selected cell and its neighbors directly on the grid.

Example:

``` text
dim all cells
highlight center
highlight neighborhood
```

If the neighborhood is custom, show its mask.

This should be one of the first teaching interactions.

------------------------------------------------------------------------

# 90. Essential Feature: Rule Editor

For Life-like CA:

``` text
BIRTH
0 1 2 [3] 4 5 6 7 8

SURVIVE
0 1 [2] [3] 4 5 6 7 8
```

Click numbers on/off.

The notation updates:

``` text
B3/S23
```

in real time.

The simulation immediately shows the consequences.

------------------------------------------------------------------------

# 91. Essential Feature: ECA Rule Table

Display:

``` text
111 → 0
110 → 0
101 → 0
100 → 1
011 → 1
010 → 1
001 → 1
000 → 0
```

and:

``` text
Binary: 00011110
Rule: 30
```

Click any output bit to change the rule.

The rule number updates automatically.

This makes Rule 30 understandable rather than magical.

------------------------------------------------------------------------

# 92. Essential Feature: Time Scrubber

Store recent generations.

Allow:

``` text
← G120 ───────── G186 →
```

Users can move backward and forward.

This changes the CA from a transient simulation into an inspectable
temporal object.

------------------------------------------------------------------------

# 93. Essential Feature: Activity Statistics

Display:

``` text
Generation
Live Cells
Births
Deaths
Density
Changed Cells
Entropy estimate
```

Charts can reveal transitions not obvious from one frame.

But the canvas should remain dominant.

------------------------------------------------------------------------

# 94. Signature Feature: Rule Space Atlas

For ECA, show all 256 rules as thumbnails.

Hover:

``` text
Rule 90
```

Click:

``` text
open in Explorer
```

Allow visual sorting.

This is especially powerful because the entire elementary rule space is
small enough to browse.

------------------------------------------------------------------------

# 95. Signature Feature: Local → Global Lens

Select one cell.

Show its local neighborhood and rule evaluation on the left.

Show the entire emergent world on the right.

``` text
LOCAL                           GLOBAL

x x x                           [full grid]
x C x
x x x

neighbors = 3
C: dead → alive
```

This directly teaches the central idea of cellular automata.

------------------------------------------------------------------------

# 96. Signature Feature: Pattern Library

For Game of Life include:

-   Block
-   Beehive
-   Loaf
-   Boat
-   Blinker
-   Toad
-   Beacon
-   Pulsar
-   Glider
-   Lightweight spaceship
-   Gosper glider gun
-   R-pentomino
-   Acorn
-   Diehard

Group them by behavior:

``` text
Still Life
Oscillator
Spaceship
Gun
Long Transient
```

Users should be able to stamp them into the world.

------------------------------------------------------------------------

# 97. Suggested Explorer Modes

## Mode 1 --- Learn

Start with:

``` text
small grid
Game of Life
single selected cell
```

Explain neighborhood and update.

## Mode 2 --- Life Lab

Focus on:

-   B/S rules;
-   pattern library;
-   gliders;
-   oscillators;
-   guns.

## Mode 3 --- Elementary

Focus on:

``` text
Rule 0–255
```

and time-history images.

## Mode 4 --- Rule Lab

Edit local rules and neighborhoods.

## Mode 5 --- Paint

Use seed drawing and image import.

## Mode 6 --- Transform

Use multi-state, decay, stochastic rules, and alternative rendering.

## Mode 7 --- Compare

Run two rules or seeds side by side.

## Mode 8 --- Cross-Algorithm

Connect CA to:

-   Reaction--Diffusion;
-   Boids;
-   L-systems;
-   Genetic Algorithms.

------------------------------------------------------------------------

# 98. Suggested UI Layout

``` text
┌──────────────────────────────────────────────────────────────┐
│ CELLULAR AUTOMATA EXPLORER                                   │
├──────────────────┬──────────────────────────────┬────────────┤
│                  │                              │            │
│ RULE / WORLD     │                              │ INSPECTOR  │
│                  │         CA CANVAS            │            │
│ B3 / S23         │                              │ Cell 42,18 │
│ Moore r=1        │                              │ State 1    │
│ States: 2        │                              │ Neigh: 3   │
│ Boundary: Wrap   │                              │ → survives │
│                  │                              │            │
├──────────────────┴──────────────────────────────┴────────────┤
│ ← G120 ───────────────────────────────────────────── G186 → │
│                         TIME                                 │
├──────────────────────────────────────────────────────────────┤
│ Step | Play | Speed | Draw | Randomize | Presets | Export   │
└──────────────────────────────────────────────────────────────┘
```

The interface should feel like a **microscope for artificial worlds**,
not a generic settings dashboard.

------------------------------------------------------------------------

# 99. Artistic Concept: Emergence

Cellular automata are perhaps the clearest algorithm in this project for
discussing emergence.

A Game of Life cell does not know:

``` text
glider
oscillator
gun
```

It only knows:

``` text
my state
+
my neighbors
```

Yet recognizable structures appear.

Therefore:

``` text
global identity
can emerge
without global instruction
```

------------------------------------------------------------------------

# 100. Artistic Concept: Nature

CA are often used to think about natural systems because many natural
phenomena involve local interactions.

But a CA is not automatically a realistic model of nature.

For art, the more useful idea is:

> What kinds of "nature" appear when a world is constructed from
> discrete local rules?

The result may resemble:

-   organisms;
-   crystals;
-   erosion;
-   colonies;
-   ecosystems;
-   waves.

But these resemblances emerge from abstraction.

------------------------------------------------------------------------

# 101. Artistic Concept: Growth

Growth in CA occurs through local state transitions.

There is no central growth plan.

A pattern can expand because edge cells repeatedly create new active
cells.

This is:

``` text
distributed growth
```

rather than top-down construction.

------------------------------------------------------------------------

# 102. Artistic Concept: Transformation

Every generation replaces the current image with a new image.

Therefore CA can be understood as a repeated image transformation
operator:

``` text
Image(t)
    ↓ local rule
Image(t+1)
    ↓
Image(t+2)
```

The artwork is not only the image.

It is the **rule of transformation between images**.

------------------------------------------------------------------------

# 103. Artistic Concept: Repetition

The same rule is applied:

``` text
to every cell
at every generation
```

Yet repetition creates difference because local contexts differ.

This is one of the strongest conceptual properties of CA:

``` text
same instruction
+
different neighborhood
=
different outcome
```

------------------------------------------------------------------------

# 104. Artistic Concept: Image-Making

Traditional drawing:

``` text
artist decides pixel/mark
```

Cellular image-making:

``` text
artist defines local relation
↓
system decides future pixels
```

The artist creates conditions for an image to happen.

This shifts image-making from:

``` text
composition
```

toward:

``` text
rule-based transformation
```

------------------------------------------------------------------------

# 105. Artistic Concept: Locality

Each cell normally sees only nearby cells.

It has no global map.

This creates a conceptual question:

> How can coherent form arise when no part of the system understands the
> whole?

This connects CA to:

-   collective behavior;
-   decentralized systems;
-   urban growth;
-   social systems;
-   biological development.

------------------------------------------------------------------------

# 106. Artistic Concept: Time

A CA frame is incomplete without its history.

A still Life image can hide whether a pattern:

-   just appeared;
-   has existed for thousands of generations;
-   is about to collapse.

Therefore the true medium is:

``` text
space × time
```

The Explorer should emphasize trajectories and histories.

------------------------------------------------------------------------

# 107. Artistic Concept: Death and Birth

Game of Life explicitly uses biological language:

``` text
birth
survival
death
```

But these are state transitions, not literal organisms.

Artists can exploit this metaphor while also questioning it.

What does it mean to call a pixel "alive"?

------------------------------------------------------------------------

# 108. Artistic Concept: Identity

A glider seems like an object moving through space.

But its individual cells constantly change.

So where is the glider's identity?

Not in any single cell.

Its identity exists in:

``` text
a repeating relational pattern
```

This is a rich artistic and philosophical idea.

------------------------------------------------------------------------

# 109. Artistic Concept: Law

A CA world has explicit laws.

Every event follows the local rule.

Artists can therefore create speculative worlds by designing alternate
laws.

Changing one bit in a rule table can create another universe.

The artwork can be:

``` text
not an object
but a law
```

------------------------------------------------------------------------

# 110. Artistic Concept: Determinism and Unpredictability

A deterministic CA has no randomness after initialization.

Yet systems such as Rule 30 can appear unpredictable.

This creates an important distinction:

``` text
deterministic
≠
visually simple
≠
easily predictable
```

The Explorer can make this tension experiential.

------------------------------------------------------------------------

# 111. Recommended Technical Architecture

``` text
Application
│
├── CA Engine
│   ├── grid
│   ├── states
│   ├── neighborhood
│   ├── boundary
│   ├── update scheduler
│   └── random seed
│
├── Rule System
│   ├── Life-like B/S
│   ├── ECA rule
│   ├── transition table
│   ├── probabilistic rule
│   └── custom rule
│
├── Initial Conditions
│   ├── random
│   ├── drawing
│   ├── presets
│   ├── image import
│   └── text rasterization
│
├── Renderer
│   ├── Canvas
│   ├── pixel mode
│   ├── age/state color
│   ├── overlays
│   └── export
│
├── History
│   ├── generation buffers
│   ├── statistics
│   └── snapshots
│
└── UI
    ├── rule editor
    ├── neighborhood editor
    ├── seed tools
    ├── cell inspector
    ├── timeline
    ├── pattern library
    └── rule atlas
```

------------------------------------------------------------------------

# 112. Suggested Experiment Data Model

``` json
{
  "model": "life-like",
  "grid": {
    "width": 200,
    "height": 140,
    "geometry": "square",
    "boundary": "wrap"
  },
  "states": {
    "count": 2
  },
  "neighborhood": {
    "type": "moore",
    "radius": 1
  },
  "rule": {
    "birth": [3],
    "survival": [2, 3]
  },
  "initialCondition": {
    "type": "random",
    "density": 0.25,
    "seed": 18273
  },
  "simulation": {
    "generation": 0,
    "stepsPerSecond": 12
  },
  "render": {
    "mode": "cells",
    "showGrid": false,
    "colorMode": "state"
  }
}
```

------------------------------------------------------------------------

# 113. ECA Data Model

``` json
{
  "model": "elementary",
  "ruleNumber": 30,
  "width": 601,
  "generations": 400,
  "boundary": "fixed",
  "initialCondition": {
    "type": "single-center"
  }
}
```

------------------------------------------------------------------------

# 114. Multi-State Data Model

``` json
{
  "model": "generations",
  "states": 8,
  "birth": [3],
  "survival": [2, 3],
  "decay": true
}
```

The exact semantics should be documented in the implementation because
multi-state conventions vary.

------------------------------------------------------------------------

# 115. Implementation Warnings

## Do not update in place

Use current and next buffers for synchronous CA.

## Make boundary behavior explicit

Many apparent "bugs" are actually boundary choices.

## Separate state from color

Do not hard-code:

``` text
state 1 = black
```

into the engine.

## Do not equate CA with Game of Life

Life is one famous CA, not the entire field.

## Do not equate CA with fractals

Some CA produce fractal patterns, many do not.

## Keep rule representations inspectable

Users should be able to understand what the rule means.

## Seed randomness

Random initial conditions should be reproducible.

## Protect performance

Large grids × high simulation speeds can become expensive.

## Preserve history selectively

Storing every full grid indefinitely can consume large memory.

Use:

-   limited ring buffers;
-   snapshots;
-   compressed history;
-   recomputation from seed when feasible.

## Validate custom neighborhoods

Avoid empty or malformed masks unless deliberately allowed.

------------------------------------------------------------------------

# 116. Recommended Minimum Viable Product

The first complete version should include:

1.  2D square binary grid;
2.  Game of Life B3/S23;
3.  editable Life-like B/S rules;
4.  Moore and von Neumann neighborhoods;
5.  fixed and wrap boundaries;
6.  random initialization;
7.  density control;
8.  seed painting;
9.  pattern presets;
10. step/play/pause;
11. speed control;
12. generation counter;
13. cell inspector;
14. neighborhood highlighting;
15. time-history buffer;
16. state/live-cell statistics;
17. ECA mode;
18. Rule 0--255 editor;
19. Rule 30/90/110 presets;
20. PNG export;
21. JSON import/export.

------------------------------------------------------------------------

# 117. Recommended Advanced Version

After the core works:

1.  custom neighborhood editor;
2.  multi-state CA;
3.  Generations-type decay rules;
4.  probabilistic CA;
5.  asynchronous updates;
6.  hexagonal grid;
7.  image import;
8.  typography seed;
9.  rule mutation;
10. ECA rule-space atlas;
11. seed atlas;
12. age/trail rendering;
13. sparse infinite Life mode;
14. sound mapping;
15. webcam/body input;
16. 3D CA;
17. GPU acceleration;
18. reversible CA experiments;
19. Genetic Algorithm rule evolution;
20. cross-algorithm input/output.

------------------------------------------------------------------------

# 118. Suggested Experiments for the Student

## Experiment 1 --- One rule, many seeds

Use:

``` text
B3/S23
```

with:

-   one cell;
-   random 10%;
-   random 50%;
-   text;
-   hand drawing.

**Question:** How much of the result belongs to the law, and how much
belongs to the beginning?

------------------------------------------------------------------------

## Experiment 2 --- One-bit rule mutation

Compare:

``` text
Rule 30
```

with nearby rules produced by flipping one rule-table bit.

**Question:** How much global difference can one local decision create?

------------------------------------------------------------------------

## Experiment 3 --- Moore vs von Neumann

Keep everything else as similar as possible.

Change neighborhood.

**Question:** Is perception itself part of the world's morphology?

------------------------------------------------------------------------

## Experiment 4 --- Cell scale

Render identical simulation at:

``` text
20 px/cell
5 px/cell
1 px/cell
```

**Question:** At what point does a cellular world begin to look
continuous?

------------------------------------------------------------------------

## Experiment 5 --- Glider identity

Track one glider.

Color each physical cell by how long it remains alive.

**Question:** If the cells change but the glider persists, what
constitutes the object?

------------------------------------------------------------------------

## Experiment 6 --- Rule classes

Compare:

``` text
Class 1
Class 2
Class 3
Class 4
```

ECA examples.

**Question:** How does visual complexity relate to rule complexity?

------------------------------------------------------------------------

## Experiment 7 --- Image erosion

Import a photograph.

Use it as the initial state.

Run different Life-like rules.

**Question:** When does an image stop being a representation and become
a process?

------------------------------------------------------------------------

## Experiment 8 --- Change the laws mid-run

Run Life for 100 generations.

Then switch rule.

**Question:** Can a visual system contain a historical rupture?

------------------------------------------------------------------------

# 119. Comparison with the Other Algorithm Explorer Systems

## Reaction--Diffusion

Basic unit:

``` text
continuous field values
```

Interaction:

``` text
reaction + diffusion
```

## Boids

Basic unit:

``` text
moving agents
```

Interaction:

``` text
local steering
```

## L-Systems

Basic unit:

``` text
symbols / modules
```

Interaction:

``` text
parallel rewriting
```

## Genetic Algorithms

Basic unit:

``` text
population of candidates
```

Interaction:

``` text
selection + inheritance + variation
```

## Cellular Automata

Basic unit:

``` text
cell
```

Interaction:

``` text
local neighborhood update
```

Together:

``` text
Reaction–Diffusion → fields
Boids              → agents
L-Systems          → grammars
Genetic Algorithms → populations/search
Cellular Automata  → cells/local laws
```

This gives the overall Algorithm Explorer a strong conceptual structure.

------------------------------------------------------------------------

# 120. Instructions for an AI Coding Agent

> Build an interactive browser-based Cellular Automata Explorer for an
> art and design student. The application must function simultaneously
> as a technically clear cellular-automata simulator, an educational
> visualization of local-to-global emergence, and a creative
> image-making instrument.
>
> Architect the simulation engine independently from rendering. The core
> engine should explicitly model grid/lattice, cell state, neighborhood,
> local transition rule, boundary condition, update schedule, and
> generation.
>
> Begin with a 2D binary square-grid engine and Conway's Game of Life.
> Use synchronous double-buffered updates. Support B/S notation,
> starting with B3/S23, and allow users to edit birth and survival
> counts interactively.
>
> Make local causality visible. When a user selects a cell, highlight
> its neighborhood and show its current state, neighbor
> count/configuration, the applicable rule, and its calculated next
> state.
>
> Add a 1D Elementary Cellular Automata mode supporting all 256 rules.
> Display the eight neighborhood patterns, their output bits, binary
> rule representation, and decimal rule number. Include Rule 30, Rule
> 90, and Rule 110 presets.
>
> The main canvas should remain dominant. Include drawing tools so users
> can paint initial conditions and then transform those drawings through
> the automaton.
>
> Include fixed and toroidal boundaries, Moore and von Neumann
> neighborhoods, random initialization with density and deterministic
> seed, play/pause/step controls, simulation speed, generation history,
> and pattern presets.
>
> Add a Game of Life pattern library organized by still lifes,
> oscillators, spaceships, guns, and long transients. Allow patterns to
> be stamped into the grid.
>
> Store enough recent history for a timeline scrubber without allowing
> unbounded memory growth.
>
> Keep state semantics independent from rendering. Support cell/state
> color mappings and later add age trails, multi-state systems,
> stochastic rules, custom neighborhoods, image import, and alternative
> lattices.
>
> A high-value educational feature is a **Local → Global Lens** showing
> one cell's local rule evaluation beside the full emergent pattern.
>
> A high-value exploratory feature is a **Rule Space Atlas** showing
> thumbnails of all 256 elementary CA rules under a consistent seed.
>
> After the core is stable, add multi-state/Generations rules,
> probabilistic and asynchronous variants, rule mutation, custom
> neighborhood drawing, sound/camera interaction, and adapters
> connecting the CA to Reaction--Diffusion, Boids, L-systems, and
> Genetic Algorithms.

------------------------------------------------------------------------

# 121. Key Takeaways

1.  A cellular automaton is built from **cells, states, neighborhoods,
    local update rules, and discrete time**.
2.  Its defining conceptual power is that simple local interactions can
    generate complex global behavior.
3.  Cellular automata grew from mid-20th-century work associated
    especially with Ulam and von Neumann.
4.  Conway's Game of Life, devised in 1970, is the most famous example.
5.  Life uses a binary square grid, Moore neighborhood, synchronous
    updates, and rule B3/S23.
6.  Life can produce still lifes, oscillators, spaceships, guns, and
    long-lived transient structures.
7.  Elementary cellular automata are 1D binary radius-1 systems with
    exactly 256 possible rules.
8.  Rule 30 demonstrates apparent irregularity; Rule 90 produces regular
    fractal structure; Rule 110 supports complex localized behavior and
    universal computation.
9.  Wolfram's four classes provide a useful qualitative vocabulary:
    uniform, periodic/stable, chaotic, and complex localized behavior.
10. Neighborhood design is fundamental because it defines what each cell
    is capable of perceiving.
11. Synchronous CA require double buffering so every next state is
    calculated from the same previous generation.
12. Boundary conditions define the topology of the artificial world.
13. Multi-state, probabilistic, asynchronous, non-totalistic, and
    alternative-lattice systems greatly expand the artistic space.
14. For art, the initial condition can be treated as an image that is
    subsequently transformed by local law.
15. The artist can design not only the image but the **law under which
    images change**.
16. CA create strong conceptual connections to emergence, distributed
    growth, repetition, time, artificial life, identity, locality,
    determinism, and rule-based image-making.
17. The Explorer should expose the full causal chain: **cell →
    neighborhood → rule → next state → generation → emergent pattern**.
18. Across the full Algorithm Explorer, Cellular Automata provide the
    clearest example of **cells/local laws**, complementing fields,
    agents, grammars, and evolutionary populations.

------------------------------------------------------------------------

# 122. Selected Research Sources

## Cellular automata theory and taxonomy

**Stephen Wolfram --- "Universality and Complexity in Cellular
Automata," *Physica D* 10 (1984), 1--35.**\
Foundational systematic analysis of cellular automata and the four broad
behavioral classes. The paper describes CA as discrete dynamical systems
capable of complex self-organizing behavior.\
https://doi.org/10.1016/0167-2789(84)90245-8

**Wolfram MathWorld --- Cellular Automaton.**\
Useful technical overview of CA definitions, Moore and von Neumann
neighborhoods, elementary cellular automata, and the 256 elementary
rules.\
https://mathworld.wolfram.com/CellularAutomaton.html

**Adamatzky et al. / contemporary taxonomy research --- "A comprehensive
taxonomy of cellular automata" (2024/2025 publication context).**\
A modern formal taxonomy covering elementary and broader CA
formulations; useful for precise definitions of lattice, state,
neighborhood, and transition functions.\
https://doi.org/10.1016/j.cnsns.2024.108362

## Conway's Game of Life

**LifeWiki --- Conway's Game of Life.**\
Community technical reference for Conway's Life, B3/S23 rules, history,
patterns, and terminology.\
https://conwaylife.com/wiki/Conway%27s_Game_of_Life

**LifeWiki --- Main pattern/reference archive.**\
Extensive documentation of still lifes, oscillators, spaceships, guns,
puffers, methuselahs, and other Life structures.\
https://conwaylife.com/wiki/Main_Page

## Wolfram classes and elementary cellular automata

**Stephen Wolfram --- Four Classes of Behavior, *A New Kind of Science*
online.**\
Primary exposition of the four-class qualitative scheme for cellular
automaton behavior.\
https://www.wolframscience.com/nks/p231--four-classes-of-behavior/

**David Eppstein --- Wolfram's Classification of Cellular Automata.**\
Concise academic explanation of Classes 1--4 and their relationship to
stable, periodic, chaotic, and complex localized behavior.\
https://ics.uci.edu/\~eppstein/ca/wolfram.html

## Architecture and generative design

**Christiane M. Herr & Ryan C. Ford --- "Cellular automata in
architectural design: From generic systems to specific design tools,"
*Automation in Construction* 72 (2016), 39--45.**\
Examines how generic CA systems must be adapted when they become
specific architectural design tools.\
https://doi.org/10.1016/j.autcon.2016.07.005

**Yiming Liu & Christiane M. Herr --- "Control strategies for Cellular
Automata-based generative design in architecture and urbanism,"
*Automation in Construction* 183 (2026), 106754.**\
Recent review emphasizing controllability, designer intervention,
interactive feedback loops, and integration with AI in CA-based
architectural and urban generative design.\
https://doi.org/10.1016/j.autcon.2025.106754

------------------------------------------------------------------------

# 123. Research Note

The numbered list in the user's template contains terminology inherited
from the earlier Reaction--Diffusion task, including
"Reaction-Diffusion" and the "Gray-Scott model."

For technical accuracy, this document interprets the intended research
questions as:

``` text
1. What are Cellular Automata?
2. What is their historical and theoretical background?
3. What are their mathematical/computational principles?
4. How do cells update step by step?
5. Which parameters and structural choices affect visible behavior?
6. What are the major CA families and models, especially Conway's Game of Life?
7. What visual and temporal patterns can they generate?
8. How can CA be implemented computationally?
9. How are CA used in art, design, architecture, and creative coding?
10. How can artists modify and experiment with them?
11. Which controls should an Algorithm Explorer expose?
12. How do CA connect to emergence, nature, growth,
    transformation, repetition, image-making, locality,
    time, identity, and artificial life?
```

Special emphasis has been placed on:

``` text
cells
states
neighborhoods
update rules
emergence
Conway's Game of Life
different types of cellular automata
```

as requested.

# Flocking / Boids Systems

## Deep Research Context Document for an Algorithm Explorer

**Intended use:** Technical and conceptual context for an AI coding
agent building an interactive web-based Algorithm Explorer for an art
and design student.\
**Primary model:** Craig Reynolds' Boids flocking model\
**Related models:** Vicsek model, zone-based collective-motion models,
steering behaviors, swarm/agent systems\
**Document emphasis:** theory → local rules → computation → collective
behavior → visual experimentation → interaction design

------------------------------------------------------------------------

# 0. Research Plan and Suitability Check

## Proposed research plan

The research is organized in six connected layers.

### Layer 1 --- Historical and conceptual foundation

-   Establish what flocking and Boids are.
-   Study Craig Reynolds' 1986/1987 Boids work and its place in
    behavioral animation and artificial life.
-   Explain why decentralized local rules were important compared with
    scripting every individual trajectory.
-   Situate Boids alongside later collective-motion models such as
    Vicsek and biologically inspired zone models.

### Layer 2 --- Computational mechanics

-   Represent each boid as an autonomous moving agent.
-   Explain position, velocity, acceleration, perception, steering, and
    neighborhood search.
-   Derive the three canonical behaviors: separation, alignment,
    cohesion.
-   Explain steering-force combination and motion integration.

### Layer 3 --- Parameter-to-behavior mapping

-   Identify the parameters that most strongly affect visible collective
    behavior.
-   Explain how changing rule weights, perception radius, speed,
    steering force, density, field of view, noise, and boundary
    conditions changes the flock visually.

### Layer 4 --- Implementation and performance

-   Translate the algorithm into browser-friendly pseudocode.
-   Compare simple O(N²) neighbor checking with spatial partitioning.
-   Recommend implementation approaches for p5.js / Canvas and
    high-performance WebGL or optimized JavaScript.
-   Separate simulation logic from rendering.

### Layer 5 --- Creative-practice research

-   Examine Boids as a generative-art and interactive-media technique.
-   Study uses in animation, installations, architectural/generative
    design, creative coding, and swarm-based image making.
-   Explore deliberate modifications such as trails, predators,
    attractors, obstacles, heterogeneous agents, sound, camera input,
    image fields, and hybrid algorithms.

### Layer 6 --- Algorithm Explorer specification

-   Convert research into a practical application concept.
-   Design controls that reveal causal relationships between individual
    rules and collective behavior.
-   Add educational overlays, rule isolation, parameter-space
    experiments, trails, data views, presets, export, and artistic
    modes.

## Suitability check

This plan is well suited to the project because a Boids explorer should
not merely reproduce a flock of triangles.

The central learning problem is:

> How can many autonomous agents, each following only local rules,
> create coordinated global motion without a leader?

Therefore the application must expose the relationship:

**individual perception → local steering decision → repeated interaction
→ collective form**

For an art/design student, it should also make the system usable as a
**dynamic visual material**. The research therefore needs both
scientific/computational rigor and room for intentional misuse,
modification, and image-making.

------------------------------------------------------------------------

# 1. What Is Flocking / Boids?

**Flocking** describes coordinated collective movement such as:

-   bird flocks;
-   fish schools;
-   animal herds;
-   insect swarms;
-   crowds or artificial agents moving together.

In computer graphics, **Boids** is Craig Reynolds' influential model for
generating flock-like motion using autonomous agents.

The name "boid" is derived from "bird-oid object": an abstract bird-like
agent rather than a biologically complete bird.

Instead of scripting the trajectory of every bird, Reynolds' model gives
each simulated agent a small set of local steering rules.

The classic rules are:

1.  **Separation** --- avoid crowding nearby flockmates.
2.  **Alignment** --- steer toward the average heading of nearby
    flockmates.
3.  **Cohesion** --- steer toward the average position of nearby
    flockmates.

No boid needs a map of the final flock shape.

No central controller tells the group:

``` text
form a cloud
turn left
split into two groups
recombine
```

Instead, the collective motion emerges from repeated local interactions.

This is the key idea:

> The flock is not explicitly designed as a global object. It is
> continuously produced by the relationships among individuals.

------------------------------------------------------------------------

# 2. Historical and Theoretical Background

## 2.1 Craig Reynolds and behavioral animation

Craig Reynolds developed the Boids model in 1986 and published the
landmark paper:

**"Flocks, Herds, and Schools: A Distributed Behavioral Model"**\
SIGGRAPH 1987.

Reynolds proposed simulation as an alternative to manually scripting the
motion of every individual in a flock.

The simulated flock was treated as an elaboration of a particle system,
but with an important difference:

> each particle became an independent actor with perception and
> behavior.

This helped establish an influential approach known as **behavioral
animation**.

Traditional animation might define:

``` text
agent A follows path A
agent B follows path B
agent C follows path C
```

Boids instead defines:

``` text
each agent observes nearby agents
each agent computes steering
the group trajectory emerges
```

The model therefore moves authorship from the **trajectory** to the
**behavioral rules**.

## 2.2 Artificial life and emergence

Boids became a canonical example of **artificial life** and **emergent
behavior**.

Emergence describes situations where:

-   individual components follow relatively simple rules;
-   interactions are local;
-   no component represents the complete global pattern;
-   coherent large-scale organization nevertheless appears.

A flock can:

-   maintain group coherence;
-   change direction;
-   stretch;
-   compress;
-   split;
-   merge;
-   flow around obstacles;

without an explicit global flock controller.

## 2.3 Later collective-motion models

Boids is not the only model of flocking.

### Vicsek model

The Vicsek model, introduced in 1995, strips collective motion down
further.

Particles:

-   move at approximately constant speed;
-   align their heading with neighbors;
-   receive random angular noise.

Despite this simplicity, the model can exhibit a transition between
disordered motion and globally ordered collective motion.

This makes it important for statistical physics and active-matter
research.

### Zone-based biological models

Other models distinguish spatial interaction zones.

A well-known structure uses:

-   **zone of repulsion**;
-   **zone of orientation**;
-   **zone of attraction**.

Very close neighbors trigger avoidance. Intermediate neighbors influence
orientation. More distant visible neighbors attract.

Such models are useful if the Explorer later adds a more biologically
suggestive mode.

### Reynolds' later steering behaviors

Reynolds later generalized autonomous motion into a larger vocabulary of
steering behaviors, including:

-   seek;
-   flee;
-   pursuit;
-   evasion;
-   arrival;
-   wander;
-   obstacle avoidance;
-   path following;
-   containment;
-   leader following;
-   flocking.

This is important artistically because Boids can be treated as a
**behavior-composition framework**, not just one fixed algorithm.

------------------------------------------------------------------------

# 3. Basic Mathematical / Computational Principles

A boid is usually represented by a small state vector.

For boid (i):

\[ `\mathbf{x}`{=tex}\_i = `\text{position}`{=tex} \]

\[ `\mathbf{v}`{=tex}\_i = `\text{velocity}`{=tex} \]

\[ `\mathbf{a}`{=tex}\_i =
`\text{acceleration / accumulated steering}`{=tex} \]

At each simulation step:

1.  identify relevant neighbors;
2.  calculate steering behaviors;
3.  combine them;
4.  update velocity;
5.  update position;
6.  enforce boundaries;
7.  render the agent.

A common motion update is:

\[ `\mathbf{v}`{=tex}\_i(t+`\Delta `{=tex}t) =
`\mathbf{v}`{=tex}\_i(t)+`\mathbf{a}`{=tex}\_i(t)`\Delta `{=tex}t \]

\[ `\mathbf{x}`{=tex}\_i(t+`\Delta `{=tex}t) =
`\mathbf{x}`{=tex}\_i(t)+`\mathbf{v}`{=tex}\_i(t+`\Delta `{=tex}t)`\Delta `{=tex}t
\]

Velocity is usually limited by a maximum speed.

Steering acceleration is often limited by a maximum steering force.

------------------------------------------------------------------------

# 4. Neighborhood and Local Perception

The defining feature of Boids is **locality**.

A boid does not need to respond equally to every other boid.

Define a perception radius:

\[ R \]

Boid (j) is a neighbor of boid (i) when:

\[ \|\|`\mathbf{x}`{=tex}\_j-`\mathbf{x}`{=tex}\_i\|\| \< R \]

possibly combined with a field-of-view test.

The neighborhood determines what information an agent can use.

This makes perception itself an artistic parameter.

A small perception radius produces highly local behavior.

A large radius creates more globally coordinated motion.

------------------------------------------------------------------------

# 5. The Three Canonical Rules

# 5.1 Separation

**Goal:** avoid overcrowding and collisions.

For every neighbor that is too close, construct a vector pointing away
from that neighbor.

A simple conceptual form is:

\[ `\mathbf{s}`{=tex}*i = `\sum`{=tex}*{j`\in `{=tex}N_i}
`\frac{\mathbf{x}_i-\mathbf{x}_j}`{=tex}
{\|\|`\mathbf{x}`{=tex}\_i-`\mathbf{x}`{=tex}\_j\|\|\^2} \]

The inverse-distance weighting means closer agents repel more strongly.

Then convert this desired direction into a steering force.

### Visual effect

Low separation:

-   dense clusters;
-   overlapping agents;
-   compact masses.

High separation:

-   more personal space;
-   expanded flock;
-   dispersed or granular movement;
-   excessive values may prevent stable flock formation.

------------------------------------------------------------------------

# 5.2 Alignment

**Goal:** match the direction of nearby agents.

Compute the average velocity:

\[ `\mathbf{v}`{=tex}*{avg} = `\frac{1}{|N_i|}`{=tex}
`\sum`{=tex}*{j`\in `{=tex}N_i}`\mathbf{v}`{=tex}\_j \]

Then steer toward that velocity.

Conceptually:

``` text
desired velocity = average neighbor velocity
steering = desired velocity - current velocity
```

### Visual effect

Low alignment:

-   individuals move in conflicting directions;
-   flock looks noisy or turbulent;
-   coherent travel is difficult.

High alignment:

-   agents quickly share a common direction;
-   smooth streams form;
-   motion becomes strongly coordinated;
-   excessive alignment can make the flock rigid or mechanically
    synchronized.

------------------------------------------------------------------------

# 5.3 Cohesion

**Goal:** remain near the group.

Calculate the average neighbor position:

\[ `\mathbf{c}`{=tex}*i = `\frac{1}{|N_i|}`{=tex}
`\sum`{=tex}*{j`\in `{=tex}N_i}`\mathbf{x}`{=tex}\_j \]

Then steer toward this local center.

### Visual effect

Low cohesion:

-   flock fragments;
-   agents drift apart;
-   several small groups may form.

High cohesion:

-   tight clustering;
-   agents rapidly pull toward local centers;
-   if separation is weak, agents can collapse into dense knots.

------------------------------------------------------------------------

# 6. Steering: Desired Velocity Minus Current Velocity

A very useful implementation idea is Reynolds' steering formulation.

If an agent wants velocity:

\[ `\mathbf{v}`{=tex}\_{desired} \]

but currently has:

\[ `\mathbf{v}`{=tex} \]

then:

\[ `\mathbf{steering}`{=tex} = `\mathbf{v}`{=tex}\_{desired} -
`\mathbf{v}`{=tex} \]

The steering vector is then limited by:

``` text
maxForce
```

This creates gradual turning rather than instantaneous direction
changes.

This distinction is visually important.

Without steering limits, agents can snap abruptly.

With limited steering, movement acquires inertia and appears more
animal-like.

------------------------------------------------------------------------

# 7. Combining Behaviors

A common implementation calculates three steering vectors:

``` text
sep = separation()
ali = alignment()
coh = cohesion()
```

and weights them:

``` text
force =
    sep * separationWeight
  + ali * alignmentWeight
  + coh * cohesionWeight
```

Daniel Shiffman's widely used Processing example uses a stronger
separation weighting than alignment/cohesion in its default setup.

The exact weights are not universal.

This is precisely why they are excellent interactive controls.

The three weights define a **behavioral composition space**.

------------------------------------------------------------------------

# 8. How the Algorithm Works Step by Step

## Step 1 --- Create agents

Each boid receives:

``` text
position
velocity
acceleration
maxSpeed
maxForce
```

Optionally:

``` text
size
color
species
energy
fieldOfView
personal parameters
```

## Step 2 --- Find neighbors

For each boid:

``` text
neighbors = agents within perceptionRadius
```

Optionally filter by field of view.

## Step 3 --- Calculate separation

Find nearby agents that violate personal space.

Compute an avoidance steering vector.

## Step 4 --- Calculate alignment

Average neighbor velocities.

Steer toward that shared direction.

## Step 5 --- Calculate cohesion

Average neighbor positions.

Steer toward the local center.

## Step 6 --- Weight behaviors

``` text
steering =
  separation * Ws
  + alignment * Wa
  + cohesion * Wc
```

## Step 7 --- Add other forces

Optional:

``` text
+ cursor attraction
+ predator avoidance
+ obstacle avoidance
+ flow field
+ wind
+ noise
+ target seeking
```

## Step 8 --- Limit acceleration / steering

``` text
steering.limit(maxForce)
```

## Step 9 --- Update velocity

``` text
velocity += acceleration
velocity.limit(maxSpeed)
```

## Step 10 --- Update position

``` text
position += velocity
```

## Step 11 --- Resolve boundaries

Choose:

``` text
wrap
bounce
contain
steer away
open boundary
```

## Step 12 --- Reset acceleration

``` text
acceleration = 0
```

## Step 13 --- Render

Represent boids as:

-   triangles;
-   points;
-   lines;
-   sprites;
-   brush marks;
-   particles;
-   abstract glyphs.

Repeat every frame.

------------------------------------------------------------------------

# 9. Most Important Parameters and Visual Effects

## 9.1 Separation weight

Controls the strength of local repulsion.

### Increase

The flock becomes:

-   more spacious;
-   granular;
-   collision-averse;
-   fragmented at extreme values.

### Decrease

The flock becomes:

-   denser;
-   more compressed;
-   more likely to overlap.

------------------------------------------------------------------------

# 9.2 Alignment weight

Controls how strongly agents copy nearby movement direction.

### Increase

Produces:

-   coordinated directional flow;
-   smooth collective turns;
-   long moving bands;
-   high polarization.

### Decrease

Produces:

-   noisy local motion;
-   weak collective direction;
-   swirling or scattered behavior.

------------------------------------------------------------------------

# 9.3 Cohesion weight

Controls attraction toward local group centers.

### Increase

Produces:

-   compact groups;
-   frequent merging;
-   dense moving clusters.

### Decrease

Produces:

-   drifting individuals;
-   multiple sub-flocks;
-   eventual dispersal.

------------------------------------------------------------------------

# 9.4 Perception radius

Defines how far each agent can sense.

### Small radius

-   highly local coordination;
-   fragmented micro-flocks;
-   noisy changes;
-   short-range structure.

### Large radius

-   more global coordination;
-   large coherent flock;
-   synchronized turning;
-   potentially less visually complex local behavior.

------------------------------------------------------------------------

# 9.5 Separation radius

It is often useful to separate:

``` text
general neighbor radius
personal-space radius
```

A larger separation radius increases spacing.

This can transform a dense flock into an evenly distributed moving
constellation.

------------------------------------------------------------------------

# 9.6 Maximum speed

Controls how quickly boids travel.

Higher speed:

-   energetic;
-   sharp spatial transitions;
-   harder for steering to maintain stable groups unless force also
    increases.

Lower speed:

-   meditative;
-   slow morphogenesis;
-   easier to inspect local interaction.

------------------------------------------------------------------------

# 9.7 Maximum steering force

Controls turning responsiveness.

Low force:

-   wide arcs;
-   inertia;
-   smooth movement;
-   agents may fail to avoid obstacles quickly.

High force:

-   rapid turns;
-   twitchy behavior;
-   tighter formations;
-   less sense of momentum.

The relationship:

``` text
maxForce / maxSpeed
```

is often more visually meaningful than either parameter alone.

------------------------------------------------------------------------

# 9.8 Number of agents / density

Low population:

-   individual behavior is legible;
-   sparse structures;
-   flock may fail to remain connected.

High population:

-   cloud-like mass;
-   stronger collective visual field;
-   more complex local interactions;
-   greater computational cost.

Density can produce qualitative transitions in collective organization.

------------------------------------------------------------------------

# 9.9 Field of view

Classic simplified examples often give agents 360° perception.

More animal-like versions can restrict vision.

Example:

``` text
270°
180°
120°
```

A blind zone behind an agent can produce:

-   less perfect coordination;
-   directional asymmetry;
-   delayed response;
-   more natural-looking group dynamics.

------------------------------------------------------------------------

# 9.10 Noise

Add random variation to steering or heading.

Low noise:

-   orderly flock.

Medium noise:

-   organic instability;
-   shifting local structure.

High noise:

-   collective order breaks down.

This creates a useful conceptual axis:

``` text
order ←────────────→ disorder
```

The Vicsek model makes this relationship especially explicit.

------------------------------------------------------------------------

# 9.11 Boundary behavior

### Wrap / toroidal

Agents exiting one side re-enter from the opposite side.

Useful for continuous fields.

### Bounce

Velocity reflects at the edge.

Can create edge congestion.

### Soft containment

Agents steer away before reaching boundaries.

Feels more spatially natural.

### Open

Agents can leave permanently.

Useful for migration or birth/death systems.

------------------------------------------------------------------------

# 10. Typical Collective Patterns

Unlike reaction--diffusion, Boids does not primarily create static
texture families. Its patterns are **spatiotemporal organizations of
moving agents**.

Common forms include:

## Coherent flock

Most agents share a direction and remain grouped.

## Fragmented flock

Several independent groups form.

## Milling / vortex

Agents circulate around a center.

This can emerge through modified attraction/orientation rules or
external fields.

## Stream

Agents form elongated directional flows.

## Swarm cloud

Direction is less coherent but spatial cohesion remains.

## Explosion / dispersal

Strong separation or weak cohesion causes rapid spreading.

## Collapse

Excessive cohesion with insufficient separation forms a dense knot.

## Chasing chains

Seek/pursuit behaviors produce chain-like motion.

## Predator splitting

A predator or repulsive cursor divides the flock into streams that later
merge.

## Obstacle flow

The flock bends around barriers and reconstructs itself afterward.

These patterns should be understood dynamically:

> The form of a flock is a temporary configuration produced by ongoing
> negotiation among moving agents.

------------------------------------------------------------------------

# 11. Common and Related Models

## 11.1 Reynolds Boids

Best model for the main Explorer.

Core:

``` text
separation
alignment
cohesion
```

Strengths:

-   intuitive;
-   visual;
-   easy to modify;
-   excellent for interaction;
-   historically important in computer graphics.

------------------------------------------------------------------------

## 11.2 Vicsek model

Simpler collective-motion model.

Conceptually:

``` text
new heading =
average local heading
+ noise
```

with approximately constant speed.

Excellent for exploring:

-   phase transitions;
-   order/disorder;
-   effect of noise;
-   collective alignment.

A future Explorer could offer:

``` text
Model:
[Boids] [Vicsek]
```

to compare behavioral-animation and statistical-physics approaches.

------------------------------------------------------------------------

## 11.3 Zone model

Use different radii:

``` text
repulsion zone
orientation zone
attraction zone
```

This makes perception spatially structured.

It is particularly useful for a visual educational overlay because
concentric behavioral zones can be drawn around a selected agent.

------------------------------------------------------------------------

## 11.4 Steering-behavior systems

Extend Boids with:

``` text
seek
flee
wander
pursuit
evasion
arrival
obstacle avoidance
path following
flow-field following
leader following
```

This turns the Explorer into a broader **agent behavior laboratory**.

------------------------------------------------------------------------

# 12. Computational Implementation

## 12.1 Beginner implementation: JavaScript + p5.js

p5.js is excellent for the first implementation because:

-   vectors are easy to manipulate;
-   drawing agents is straightforward;
-   mouse interaction is simple;
-   code remains readable;
-   Processing/p5.js already has canonical flocking examples.

Suggested structure:

``` text
Boid
 ├ position
 ├ velocity
 ├ acceleration
 ├ flock()
 ├ separate()
 ├ align()
 ├ cohesion()
 ├ seek()
 ├ update()
 ├ edges()
 └ render()

Flock
 ├ boids[]
 ├ addBoid()
 └ update()
```

------------------------------------------------------------------------

# 13. Basic Pseudocode

``` text
initialize boids

animation loop:

    for each boid:
        neighbors = findNeighbors(boid)

        sep = separation(boid, neighbors)
        ali = alignment(boid, neighbors)
        coh = cohesion(boid, neighbors)

        force =
            sep * separationWeight
          + ali * alignmentWeight
          + coh * cohesionWeight

        boid.acceleration += force

    for each boid:
        boid.velocity += boid.acceleration
        limit(boid.velocity, maxSpeed)

        boid.position += boid.velocity

        handleBoundary(boid)

        boid.acceleration = 0

    render boids
```

For conceptual clarity, compute steering from the same frame state
before updating positions, especially when developing advanced
deterministic comparisons.

------------------------------------------------------------------------

# 14. Performance and Neighbor Search

A naive implementation checks every boid against every other boid.

For (N) agents:

\[ O(N\^2) \]

For:

``` text
100 boids
```

this is usually manageable.

For:

``` text
5,000 boids
```

it becomes expensive.

## Spatial grid

Divide the canvas into cells.

Each boid only checks:

-   its own cell;
-   nearby cells.

This can dramatically reduce neighbor-search cost.

## Quadtree

A quadtree recursively partitions 2D space.

Useful for:

-   variable-density simulations;
-   neighbor queries;
-   educational visualization of spatial indexing.

## k-d tree

Another spatial partitioning method used in some Boids implementations.

## Recommendation

For the first Explorer:

``` text
simple O(N²)
```

is acceptable if the population is modest.

For the polished version:

``` text
uniform spatial grid
```

is probably the best balance of performance and implementation
simplicity.

------------------------------------------------------------------------

# 15. Rendering Strategies

The simulation does not have to look like birds.

This is crucial for an art/design application.

## Points

Minimal visualization.

Reveals collective geometry.

## Oriented triangles

Classic Boids representation.

Heading directly shows velocity direction.

## Lines

Draw velocity vectors.

Useful for analysis.

## Trails

Do not fully clear the previous frame.

Agents become drawing instruments.

## Ribbons

Store recent positions and connect them.

Collective movement becomes flowing calligraphy.

## Brush particles

Each boid paints texture into a persistent canvas.

## Connections

Draw lines between neighbors.

This reveals the invisible social network.

## Density field

Accumulate boid positions into a field and blur it.

The discrete swarm becomes a continuous image.

## Voronoi

Generate a Voronoi diagram from boid positions.

Movement continuously remakes spatial territories.

------------------------------------------------------------------------

# 16. Boids in Generative Art and Creative Coding

Boids is especially important in generative practice because it produces
images through **behavior rather than direct geometry**.

A conventional generative drawing may define:

``` text
draw 100 circles according to formula X
```

Boids instead defines:

``` text
create 100 agents
give them relationships
allow drawing to emerge from their movement
```

This introduces:

-   agency;
-   temporality;
-   interaction;
-   collective behavior;
-   unpredictability;
-   local decision-making.

Daniel Shiffman's *The Nature of Code* and Processing examples have made
Boids a foundational creative-coding exercise.

The p5.js ecosystem also uses interactive versions where users add boids
and manipulate flocking parameters.

------------------------------------------------------------------------

# 17. Creative / Artistic Precedents

## 17.1 Craig Reynolds --- Boids

The original model is itself an important computer-graphics precedent.

Its significance lies less in a single final image than in the
transition:

``` text
scripted animation
        ↓
behavioral animation
```

The animator specifies behavioral tendencies rather than every
trajectory.

------------------------------------------------------------------------

## 17.2 Daniel Shiffman / Processing / The Nature of Code

Shiffman's implementations have become a major educational bridge
between Boids research and creative coding.

They expose:

-   vectors;
-   steering;
-   rule weighting;
-   mouse interaction;
-   emergent movement.

This is directly relevant to an Algorithm Explorer.

------------------------------------------------------------------------

## 17.3 Hack the Flock

**Hack the Flock**, a permanent interactive installation at TELUS Spark
in Calgary, explicitly lets visitors alter flocking code and parameters.

Visitors can modify:

-   alignment;
-   cohesion;
-   separation;
-   shape;
-   color;
-   speed;
-   turning behavior;
-   even agent imagery.

An especially useful lesson is that "mistakes" in code can generate
unexpected aesthetic behavior.

This is an excellent precedent for the Explorer's philosophy:

> experimentation should include breaking the expected rules.

------------------------------------------------------------------------

## 17.4 Swarm-based generative installations

Contemporary generative works frequently extend Boids with:

-   predators;
-   environmental forces;
-   evolutionary parameters;
-   interactive input;
-   projection;
-   long-duration autonomous behavior.

A recent example, *Selection Pressure* (2026), combines Boids-like
flocking with black-hole-like predators and evolutionary selection in a
real-time installation.

The important design lesson is the hybrid structure:

``` text
flocking
+
environmental threat
+
evolution
+
long-duration behavior
```

------------------------------------------------------------------------

# 18. Architecture and Generative Design

Swarm intelligence has been investigated as a generative-design strategy
in architecture.

Instead of interpreting boids literally as birds, designers can
interpret agents as:

-   spatial samples;
-   path generators;
-   structural particles;
-   circulation agents;
-   façade components;
-   construction agents.

The trajectory of many agents can generate:

-   curves;
-   networks;
-   circulation systems;
-   spatial density maps;
-   surfaces;
-   branching structures.

This suggests an important transformation:

``` text
boid movement
      ↓
trajectory data
      ↓
geometry
      ↓
design
```

For an art/design student, the final output therefore does not need to
be an animation of a flock.

The flock can be a **generator of geometry**.

------------------------------------------------------------------------

# 19. Interesting Artistic Modifications

# 19.1 Trails as drawing

Instead of clearing every frame:

``` text
background with alpha
```

or retain all previous positions.

The boids become moving pens.

Possible results:

-   calligraphic lines;
-   tangled hair-like structures;
-   migration maps;
-   flow drawings;
-   layered temporal images.

Conceptually:

> the image becomes a memory of movement.

------------------------------------------------------------------------

# 19.2 Different rule weights for every agent

Classic implementations give all agents the same parameters.

Instead:

``` text
boid A:
alignment = 1.2

boid B:
alignment = 0.3

boid C:
alignment = 2.0
```

Now the flock contains personalities.

Possible interpretation:

-   conformity;
-   individuality;
-   social pressure;
-   resistance.

------------------------------------------------------------------------

# 19.3 Multiple species

Create:

``` text
Species A
Species B
Species C
```

Each species has different:

-   speed;
-   color;
-   perception;
-   rule weights.

Define cross-species relationships:

``` text
A attracts B
B avoids C
C follows A
```

Complex ecological structures can emerge.

------------------------------------------------------------------------

# 19.4 Predator / prey

Add predator agents.

Normal boids:

``` text
flee(predator)
```

Predator:

``` text
pursue(flock)
```

The flock can:

-   compress;
-   split;
-   scatter;
-   reform.

This produces highly dramatic interactive motion.

------------------------------------------------------------------------

# 19.5 Cursor as force

Mouse modes:

``` text
Attract
Repel
Disturb
Feed
Predator
Vortex
```

The participant does not directly move boids.

Instead, the participant changes the **force field** influencing them.

------------------------------------------------------------------------

# 19.6 Obstacles

Add:

-   circles;
-   walls;
-   text;
-   image masks;
-   architecture plans.

Boids navigate around them.

The negative space becomes part of the composition.

------------------------------------------------------------------------

# 19.7 Image-based force field

Load an image.

Use pixel values to affect motion.

Example:

``` text
brightness → attraction
edge → avoidance
color → species preference
```

A photograph becomes an invisible behavioral landscape.

------------------------------------------------------------------------

# 19.8 Flow fields

Combine Boids with a vector field.

Each boid receives:

``` text
flocking force
+
flow field force
```

The tension between local social behavior and environmental flow can
create rich motion.

------------------------------------------------------------------------

# 19.9 Noise

Use Perlin/Simplex noise to add directional drift.

``` text
social rules
+
environmental turbulence
```

This can produce wind-like or underwater motion.

------------------------------------------------------------------------

# 19.10 Sound interaction

Map audio:

``` text
volume → separation
bass → cohesion
treble → speed
beat → predator pulse
```

The flock becomes an audiovisual instrument.

------------------------------------------------------------------------

# 19.11 Camera / body interaction

Use webcam or pose tracking.

Examples:

``` text
body silhouette = obstacle
hands = attractors
movement speed = flock speed
body center = predator
```

The user becomes an environmental condition rather than a direct
controller.

------------------------------------------------------------------------

# 19.12 Typography

Use letters as:

-   obstacles;
-   attraction fields;
-   paths;
-   spawn regions.

Boids can gradually trace or erode typographic forms.

------------------------------------------------------------------------

# 19.13 Image reconstruction

Give each boid a target pixel sampled from an image.

Balance:

``` text
target attraction
+
flocking
```

At low target force:

-   flock dominates.

At high target force:

-   image becomes recognizable.

This creates a powerful continuum:

``` text
collective autonomy ←────────→ representation
```

------------------------------------------------------------------------

# 19.14 Rule mutation

Allow rule weights to mutate over time.

For example:

``` text
alignment += random(-ε, ε)
```

The collective "culture" slowly changes.

------------------------------------------------------------------------

# 19.15 Evolution

Assign fitness.

Possible goals:

-   survive predators;
-   reach targets;
-   remain cohesive;
-   cover space;
-   create a particular visual density.

Reproduce successful parameter sets.

This connects Boids to the Genetic Algorithm section of the larger
Algorithm Explorer.

------------------------------------------------------------------------

# 19.16 Local rule painting

Allow the user to paint areas of the canvas where behavior changes.

Example:

``` text
red zone:
high separation

blue zone:
high cohesion

green zone:
high alignment
```

Now the artist designs a **behavioral landscape** rather than directly
drawing form.

This is one of the strongest advanced features for the Explorer.

------------------------------------------------------------------------

# 20. Recommended Interactive Controls

## Essential simulation controls

-   Play
-   Pause
-   Reset
-   Single Step
-   Simulation Speed
-   Agent Count

## Core Boids controls

-   Separation Weight
-   Alignment Weight
-   Cohesion Weight
-   Perception Radius
-   Separation Radius
-   Max Speed
-   Max Steering Force

## Perception

-   Field of View
-   Show Neighborhood
-   Show Blind Zone

## Environment

-   Boundary Mode
-   Noise
-   Cursor Force
-   Obstacles

## Rendering

-   Agent Shape
-   Agent Size
-   Show Trails
-   Trail Length
-   Trail Opacity
-   Show Velocity
-   Show Neighbor Connections
-   Color by Speed
-   Color by Local Density
-   Color by Heading
-   Color by Species

------------------------------------------------------------------------

# 21. Rule Isolation Mode

This should be a central educational feature.

Buttons:

``` text
[Separation only]
[Alignment only]
[Cohesion only]
[All rules]
```

### Separation only

Agents disperse.

### Alignment only

Agents synchronize direction but do not necessarily stay together.

### Cohesion only

Agents collapse toward group centers.

### All three

Stable flock-like behavior emerges.

This makes the conceptual mechanism immediately visible.

------------------------------------------------------------------------

# 22. Selected-Agent Inspector

Click one boid.

Display:

``` text
position
velocity
speed
acceleration
neighbor count
separation vector
alignment vector
cohesion vector
final steering vector
```

Draw vectors directly on the canvas.

For example:

``` text
red arrow    = separation
blue arrow   = alignment
green arrow  = cohesion
white arrow  = final steering
```

This converts an invisible behavioral calculation into a visible
diagram.

------------------------------------------------------------------------

# 23. Neighborhood Visualization

When an agent is selected, show:

``` text
perception radius
separation radius
field-of-view cone
detected neighbors
ignored agents
```

This helps answer:

> What can this agent actually "know"?

That question is central to understanding decentralized systems.

------------------------------------------------------------------------

# 24. Behavioral Parameter Space

For Reaction--Diffusion, a natural 2D parameter map is F/k.

For Boids, there are three canonical rule weights, so the space is
higher-dimensional.

Possible interface:

## Triangle / ternary control

Corners:

``` text
SEPARATION
ALIGNMENT
COHESION
```

Drag a point inside the triangle.

The point represents relative rule balance.

This is potentially more intuitive than three sliders.

Example:

``` text
top corner → cohesion dominant
left → separation dominant
right → alignment dominant
center → balanced
```

This could become the signature interface of the Boids Explorer.

------------------------------------------------------------------------

# 25. Presets

Useful presets:

## Balanced Flock

Moderate values for all rules.

## School

High alignment, moderate cohesion.

## Cloud

Cohesion with noise, weaker alignment.

## Scatter

High separation.

## Swarm

Moderate cohesion, lower alignment, higher noise.

## Rigid Formation

High alignment and cohesion.

## Independent

Weak rules.

## Panic

High speed, high separation, high steering.

## Lazy Drift

Low speed, low steering, moderate cohesion.

## Turbulent

Noise + local perception.

Each preset should reveal the actual parameter values.

Presets are starting points, not hidden magic modes.

------------------------------------------------------------------------

# 26. Suggested Explorer Modes

## Mode 1 --- Learn

Controls:

``` text
Separation
Alignment
Cohesion
Play
Reset
```

Include concise explanations.

Goal:

understand the three rules.

------------------------------------------------------------------------

## Mode 2 --- Inspect

Add:

``` text
select agent
show neighborhood
show vectors
single step
```

Goal:

understand individual decisions.

------------------------------------------------------------------------

## Mode 3 --- Explore

Add:

``` text
perception
speed
force
noise
population
ternary rule control
presets
```

Goal:

explore collective behavior.

------------------------------------------------------------------------

## Mode 4 --- Draw

Add:

``` text
trails
persistent canvas
brush styles
color mappings
image export
```

Goal:

use flocking as image-making.

------------------------------------------------------------------------

## Mode 5 --- Environment

Add:

``` text
obstacles
attractors
repulsors
flow fields
image fields
```

Goal:

study flock/environment relationships.

------------------------------------------------------------------------

## Mode 6 --- Experiment

Add:

``` text
species
predators
heterogeneous personalities
sound
camera
rule painting
evolution
```

Goal:

move beyond canonical Boids.

------------------------------------------------------------------------

# 27. Suggested UI Layout

``` text
┌─────────────────────────────────────────────────────────┐
│ FLOCKING / BOIDS EXPLORER                               │
├───────────────┬────────────────────────────┬────────────┤
│               │                            │            │
│ RULES         │                            │ INSPECTOR  │
│               │                            │            │
│ Separation    │                            │ Position   │
│ Alignment     │       SIMULATION           │ Velocity   │
│ Cohesion      │         CANVAS             │ Neighbors  │
│               │                            │ Forces     │
│ Perception    │                            │            │
│ Speed         │                            │            │
│ Force         │                            │            │
│ Noise         │                            │            │
│               │                            │            │
├───────────────┴────────────────────────────┴────────────┤
│                                                       │
│      SEPARATION                                       │
│           △                                           │
│          / \        RULE BALANCE                      │
│         / ● \       TERNARY CONTROL                   │
│        /_____\                                        │
│ ALIGNMENT     COHESION                                │
│                                                       │
├─────────────────────────────────────────────────────────┤
│ Learn | Inspect | Explore | Draw | Environment | Lab   │
└─────────────────────────────────────────────────────────┘
```

The flock should remain visually dominant.

Avoid turning the application into a generic dashboard.

------------------------------------------------------------------------

# 28. Artistic Concepts

# 28.1 Emergence

Boids is one of the clearest computational examples of emergence.

The flock has recognizable group behavior, yet that behavior is not
represented inside any single agent.

This raises a powerful artistic question:

> Where does the form exist if no individual contains the form?

The answer is relational.

The "image" exists in interaction.

------------------------------------------------------------------------

# 28.2 Nature

Boids is inspired by natural flocking, but it should not be confused
with a complete scientific model of birds.

Its value is abstraction.

It asks:

> How little behavioral information is necessary before movement begins
> to look alive?

For artists, this is often more interesting than biological accuracy.

------------------------------------------------------------------------

# 28.3 Individual and collective

Each boid is autonomous but constrained by neighbors.

This produces tension between:

``` text
individuality
and
collectivity
```

Possible conceptual themes:

-   society;
-   conformity;
-   crowds;
-   cooperation;
-   social pressure;
-   decentralization;
-   collective intelligence;
-   group identity.

------------------------------------------------------------------------

# 28.4 Repetition and difference

All agents may follow the same rules.

Yet their trajectories differ because:

-   positions differ;
-   neighbors differ;
-   histories differ;
-   local conditions differ.

Thus:

``` text
same rule ≠ same outcome
```

This is a powerful generative-art principle.

------------------------------------------------------------------------

# 28.5 Transformation

The flock has no permanent shape.

Its form continuously changes through motion.

The image is therefore:

``` text
not an object
but a temporary organization
```

------------------------------------------------------------------------

# 28.6 Drawing and memory

With trails enabled, a moving agent leaves a trace.

Then two temporal layers coexist:

``` text
present = current boid positions
past = accumulated trajectories
```

The image becomes a memory of collective behavior.

------------------------------------------------------------------------

# 28.7 Control and autonomy

The artist controls:

-   rules;
-   parameters;
-   environment;
-   initial conditions;
-   rendering.

But cannot easily predict every trajectory.

The artistic relationship becomes:

``` text
author → defines behavior
system → negotiates outcome
```

rather than:

``` text
author → directly specifies image
```

------------------------------------------------------------------------

# 28.8 Distributed intelligence

There is no leader required in the basic model.

Order arises from distributed local decisions.

This connects Boids to:

-   networks;
-   crowds;
-   decentralized systems;
-   swarm robotics;
-   collective intelligence;
-   political/social metaphors.

The Explorer can make this visible by including a mode where the user
adds a leader and compares:

``` text
leaderless flock
vs
leader-following flock
```

------------------------------------------------------------------------

# 29. Connections to Image-Making

Boids can generate images in several fundamentally different ways.

## Position image

Current positions form the image.

## Trajectory image

Historical paths form the image.

## Network image

Connections between neighbors form the image.

## Density image

Accumulated population density forms the image.

## Force image

Steering vectors form the image.

## Environmental image

Agents reveal invisible obstacles or vector fields through their
movement.

## Representational image

Agents collectively reconstruct a photograph or shape.

This is important conceptually:

> Boids is not one visual style. It is a system for producing relational
> motion data that can be translated into many visual languages.

------------------------------------------------------------------------

# 30. Recommended Technical Architecture

For the first version:

``` text
HTML / CSS
JavaScript
p5.js
```

or:

``` text
React UI
+
Canvas simulation
```

Suggested architecture:

``` text
App
│
├── Simulation
│   ├── Boid[]
│   ├── SpatialGrid
│   ├── Environment
│   └── SimulationSettings
│
├── Behaviors
│   ├── separation
│   ├── alignment
│   ├── cohesion
│   ├── seek
│   ├── flee
│   └── obstacleAvoidance
│
├── Renderer
│   ├── agents
│   ├── trails
│   ├── vectors
│   ├── neighborhoods
│   └── connections
│
└── UI
    ├── controls
    ├── presets
    ├── inspector
    ├── rule balance
    └── export
```

Keep behavior calculations modular.

The coding agent should be able to add new behaviors without rewriting
the simulation core.

------------------------------------------------------------------------

# 31. Suggested Boid Data Structure

``` json
{
  "position": [320, 180],
  "velocity": [1.2, -0.4],
  "acceleration": [0, 0],
  "maxSpeed": 3,
  "maxForce": 0.05,
  "perceptionRadius": 50,
  "separationRadius": 25,
  "weights": {
    "separation": 1.5,
    "alignment": 1.0,
    "cohesion": 1.0
  }
}
```

For heterogeneous flocks, parameters can exist per agent rather than
globally.

------------------------------------------------------------------------

# 32. Suggested Saved Experiment Format

``` json
{
  "model": "boids",
  "population": 300,
  "randomSeed": 81273,
  "rules": {
    "separation": 1.5,
    "alignment": 1.0,
    "cohesion": 1.0
  },
  "perception": {
    "radius": 50,
    "separationRadius": 25,
    "fieldOfView": 360
  },
  "motion": {
    "maxSpeed": 3,
    "maxForce": 0.05,
    "noise": 0.02
  },
  "boundary": "wrap",
  "render": {
    "shape": "triangle",
    "trails": true,
    "trailLength": 80,
    "colorMode": "speed"
  }
}
```

Export/import of experiment JSON will make visual discoveries
reproducible.

------------------------------------------------------------------------

# 33. Important Implementation Warnings

## Do not confuse force with velocity

Separation/alignment/cohesion should usually produce steering
influences, not teleport positions.

## Limit forces

Unlimited steering often creates jitter.

## Normalize carefully

A zero-length vector cannot safely be normalized.

## Use consistent frame timing

If using variable `dt`, scale motion appropriately.

## Boundary distance

With wrap boundaries, naive Euclidean distance across screen edges can
be wrong.

For a mathematically consistent toroidal world, neighbor distance should
also respect wrapping.

## Avoid unnecessary allocation

Creating thousands of temporary vector objects every frame can hurt
browser performance.

## Optimize only after correctness

Start with readable code.

Then add spatial partitioning.

## Separate simulation and appearance

Changing agent color should not alter behavior unless explicitly
intended.

## Deterministic mode

Seed random initialization so experiments can be repeated.

------------------------------------------------------------------------

# 34. Recommended Minimum Viable Product

The first complete version should include:

1.  2D Boids simulation.
2.  Separation, alignment, cohesion.
3.  Real-time sliders for all three weights.
4.  Perception radius.
5.  Separation radius.
6.  Maximum speed.
7.  Maximum steering force.
8.  Agent count.
9.  Play / Pause / Reset.
10. Single-step mode.
11. Wrap / bounce boundary options.
12. Rule isolation.
13. Click-to-select agent.
14. Selected-agent neighborhood display.
15. Force-vector visualization.
16. Trails.
17. Several presets.
18. PNG export.
19. JSON parameter export/import.
20. Responsive browser performance.

------------------------------------------------------------------------

# 35. Recommended Advanced Version

After the core is stable:

1.  ternary separation/alignment/cohesion controller;
2.  field-of-view control;
3.  noise / Vicsek mode;
4.  obstacles;
5.  attractors and repulsors;
6.  predator/prey;
7.  multiple species;
8.  heterogeneous personalities;
9.  flow fields;
10. image-based fields;
11. parameter/rule painting;
12. audio input;
13. camera/body interaction;
14. trajectory recording;
15. density rendering;
16. Voronoi rendering;
17. evolutionary parameters;
18. spatial-grid performance optimization;
19. large-population mode;
20. 3D flocking as an optional later extension.

------------------------------------------------------------------------

# 36. Suggested Experiments for the Student

## Experiment 1 --- Remove one rule

Compare:

``` text
all rules
without separation
without alignment
without cohesion
```

**Question:** Which visual property disappears when each rule is
removed?

------------------------------------------------------------------------

## Experiment 2 --- From individual to collective

Start with:

``` text
10 agents
```

Increase gradually to:

``` text
1000 agents
```

**Question:** At what point does the viewer stop seeing individuals and
begin seeing a collective body?

------------------------------------------------------------------------

## Experiment 3 --- Order and noise

Increase noise gradually.

Measure or display collective alignment.

**Question:** When does coordinated motion become disorder?

------------------------------------------------------------------------

## Experiment 4 --- Social personality

Give 10% of agents extremely low alignment.

**Question:** Can a minority of nonconforming agents visibly alter the
whole flock?

------------------------------------------------------------------------

## Experiment 5 --- Draw with movement

Enable long trails.

Run the same initial state with different rule balances.

**Question:** How does a behavioral rule become a graphic style?

------------------------------------------------------------------------

## Experiment 6 --- Invisible architecture

Place invisible obstacles.

Show only the boids and their trails.

**Question:** Can movement reveal a space that is never directly drawn?

------------------------------------------------------------------------

## Experiment 7 --- Collective portrait

Load a photograph as an attraction field.

Balance:

``` text
flocking
vs
image attraction
```

**Question:** At what point does the swarm become an image?

------------------------------------------------------------------------

## Experiment 8 --- Leaderless versus leader

Run identical flocks.

Version A:

``` text
no leader
```

Version B:

``` text
leader-following force
```

**Question:** How does centralized control change the visual character
of collective movement?

------------------------------------------------------------------------

# 37. Quantitative Measures for an Advanced Explorer

An educational Explorer can display simple metrics.

## Polarization / alignment order

A measure of how similarly agents are moving.

Conceptually:

\[ P = `\frac{1}{N}`{=tex} `\left`{=tex}\| `\sum`{=tex}\_i
`\frac{\mathbf{v}_i}{|\mathbf{v}_i|}`{=tex} `\right`{=tex}\| \]

Interpretation:

``` text
P ≈ 0 → disordered directions
P ≈ 1 → strongly aligned flock
```

## Average neighbor count

Shows local density.

## Mean speed

Useful if speeds vary.

## Number of connected groups

Approximate flock fragmentation.

## Spatial dispersion

Measures how spread out the flock is.

These metrics allow the student to connect:

``` text
visual impression
↔
measurable collective state
```

------------------------------------------------------------------------

# 38. A Strong Conceptual Feature: Micro / Macro View

Provide two synchronized views.

### MICRO

Follow one selected boid.

Show:

-   neighbors;
-   perception;
-   forces;
-   decision.

### MACRO

Show entire flock.

The student can observe:

``` text
local decision
        ↓
global behavior
```

This directly communicates emergence and should be considered a
signature educational feature.

------------------------------------------------------------------------

# 39. A Strong Artistic Feature: Behavior Painting

Create a canvas overlay where the user paints rule fields.

Each pixel or grid cell stores:

``` text
separation multiplier
alignment multiplier
cohesion multiplier
```

Example:

-   red paint = separation zone;
-   blue paint = alignment zone;
-   green paint = cohesion zone.

As boids travel through the painting, their social behavior changes.

The user is therefore not drawing the resulting image.

They are drawing the **conditions of behavior**.

This connects directly to generative art and contemporary computational
authorship.

------------------------------------------------------------------------

# 40. Broader Conceptual Interpretation

Boids changes the fundamental unit of design.

Traditional composition often asks:

``` text
Where should this element be placed?
```

Boids asks:

``` text
How should this element behave in relation to nearby elements?
```

The first produces a configuration.

The second produces a continuously changing system.

This is a significant shift:

``` text
composition
      ↓
relationship
      ↓
behavior
      ↓
emergent composition
```

For an art/design student, this makes Boids relevant beyond simulated
birds.

It offers a model for designing:

-   crowds;
-   typography;
-   moving images;
-   spatial systems;
-   interactive installations;
-   generative drawings;
-   social metaphors;
-   responsive architecture;
-   autonomous visual agents.

------------------------------------------------------------------------

# 41. Comparison with Reaction--Diffusion

Since both algorithms may appear in the same Algorithm Explorer, their
conceptual difference is useful.

## Reaction--Diffusion

Basic unit:

``` text
continuous field / grid cell
```

Interaction:

``` text
chemical-like local reaction + spatial diffusion
```

Typical visual result:

``` text
spots, stripes, labyrinths, evolving textures
```

Primary conceptual emphasis:

``` text
morphogenesis
```

## Boids

Basic unit:

``` text
mobile autonomous agent
```

Interaction:

``` text
perception + steering toward/away from neighbors
```

Typical visual result:

``` text
flocks, streams, clusters, trajectories
```

Primary conceptual emphasis:

``` text
collective behavior
```

Both demonstrate emergence, but through different computational
ontologies:

``` text
Reaction–Diffusion:
field produces form

Boids:
agents produce collective motion
```

------------------------------------------------------------------------

# 42. Instructions for an AI Coding Agent

Use the following brief when implementing the application:

> Build an interactive web-based Flocking / Boids Explorer centered on
> Craig Reynolds' Boids model. The application is intended for an art
> and design student and must function simultaneously as a technically
> understandable simulation, an educational visualization, and a
> creative visual instrument.
>
> Implement the canonical separation, alignment, and cohesion steering
> behaviors as independent modular functions. Users must be able to
> modify their weights in real time and isolate each rule individually.
>
> Make local perception visible. A user should be able to select one
> boid and inspect its perception radius, nearby agents, velocity, and
> the separate steering vectors generated by separation, alignment, and
> cohesion.
>
> Prioritize direct manipulation and immediate visual feedback. Include
> controls for rule weights, perception radius, separation radius, max
> speed, max steering force, population, noise, and boundary behavior.
>
> The simulation canvas should remain visually dominant. Avoid a generic
> dashboard aesthetic; design the interface as a visual laboratory or
> behavioral instrument.
>
> Begin with a readable 2D JavaScript/p5.js or Canvas implementation.
> Keep simulation logic independent from rendering. Once behavior is
> correct, optimize neighbor search with a uniform spatial grid if
> necessary.
>
> Include rule-isolation presets and several behavior presets. Add
> trails so the swarm can become a drawing system.
>
> After the core version is stable, prioritize: ternary rule-balance
> control, obstacles, attractors/repulsors, multiple species, predators,
> image/flow fields, behavior painting, and experiment export/import.
>
> Make experiments reproducible by supporting deterministic random seeds
> and JSON parameter export.

------------------------------------------------------------------------

# 43. Key Takeaways

1.  Boids was introduced by Craig Reynolds as a distributed behavioral
    model for flocking rather than a system of scripted individual
    trajectories.
2.  The canonical rules are **separation, alignment, and cohesion**.
3.  Each agent acts primarily from **local perception**, yet global
    coordinated movement emerges.
4.  Rule weights, perception radius, speed, steering force, density,
    field of view, and noise all strongly affect visible collective
    behavior.
5.  Boids is best understood as a **dynamic agent system**, not as a
    static pattern generator.
6.  The algorithm is highly suitable for creative coding because
    additional behaviors can be composed modularly.
7.  Trails, density fields, networks, image fields, obstacles,
    predators, heterogeneous agents, sound, and camera input can
    transform flocking into an artistic medium.
8.  A particularly useful Explorer feature is **rule isolation**.
9.  A particularly useful conceptual visualization is a synchronized
    **micro/macro view**.
10. A particularly strong artistic extension is **behavior painting**,
    where the artist paints local rules rather than the final image.
11. Boids reframes composition from arranging objects to **designing
    relationships between autonomous elements**.
12. Its deepest artistic connection is to emergence: coherent form can
    belong to the **collective relationship**, rather than to any single
    element.

------------------------------------------------------------------------

# 44. Selected Research Sources

## Foundational source

**Craig W. Reynolds --- "Flocks, Herds, and Schools: A Distributed
Behavioral Model" (SIGGRAPH 1987).**\
Foundational Boids paper. Introduces a distributed behavioral approach
in which independent simulated actors use local perception and simple
behaviors to produce aggregate flock motion.\
https://www.red3d.com/cwr/papers/1987/boids.html

**Craig Reynolds --- Boids: Background and Update.**\
Reynolds' own overview of the model and its canonical separation,
alignment, and cohesion rules.\
https://www.red3d.com/cwr/boids/

## Steering behaviors

**Craig Reynolds --- "Steering Behaviors For Autonomous Characters" (GDC
1999).**\
Extends the behavioral-animation framework with seek, flee, pursuit,
evasion, obstacle avoidance, path following, flocking, leader following,
and other composable steering behaviors.\
https://www.red3d.com/cwr/papers/1999/gdc99steer.html

## Creative coding / implementation

**Processing Foundation --- Flocking, by Daniel Shiffman.**\
Canonical educational implementation of Reynolds' flocking model, with
explicit separation, alignment, cohesion, steering, maximum speed, and
maximum force.\
https://processing.org/examples/flocking

**p5.js --- Flocking example.**\
Browser-oriented creative-coding implementation based on Reynolds and
*The Nature of Code*.\
https://p5js.org/examples/classes-and-objects-flocking/

## Collective-motion theory

**Tamás Vicsek et al. --- "Novel Type of Phase Transition in a System of
Self-Driven Particles" (1995).**\
Introduces the Vicsek model, demonstrating ordered collective motion
from local heading alignment plus noise.\
https://doi.org/10.1103/PhysRevLett.75.1226

**Francesco Ginelli --- "The Physics of the Vicsek Model" (2016).**\
Open review of the model's implementation, physics, symmetries, and
collective-motion behavior.\
https://doi.org/10.1140/epjst/e2016-60066-8

**Iain D. Couzin et al. --- collective animal group model (2002).**\
Important biologically inspired approach using zones of repulsion,
orientation, and attraction plus restricted perception.

## Interactive / artistic precedent

**Mind, Matter & Media Lab --- Hack the Flock.**\
Permanent interactive installation allowing visitors to modify Boids
parameters and source code, emphasizing experimentation and unexpected
results.\
https://www.m3lab.org/public-installations/hack-the-flock

## Architecture / generative design

**Singh & Gu --- "Towards an integrated generative design framework"
(Design Studies, 2012).**\
Reviews swarm intelligence alongside cellular automata, genetic
algorithms, L-systems, and shape grammars as generative-design
approaches in architecture.\
https://doi.org/10.1016/j.destud.2011.06.001

**Wiesenhuetter, Wilde & Noennig --- "Swarm intelligence in
architectural design."**\
Discusses swarm intelligence as a tool for design processes, adaptive
buildings, agent-based planning, and self-organized construction
concepts.

------------------------------------------------------------------------

# 45. Research Note

The wording of the user's source prompt still refers to
"Reaction-Diffusion," "Gray-Scott," and reaction--diffusion pattern
generation. Because this document is requested under the title
**Flocking / Boids**, those items have been interpreted as a template
inherited from the previous Algorithm Explorer task.

For technical accuracy, this document therefore replaces them with the
corresponding Flocking / Boids questions:

``` text
What are Flocking / Boids systems?
What is Reynolds' model?
How do separation, alignment, and cohesion work?
What collective behaviors emerge?
How can agent systems be implemented and artistically modified?
```

The Gray--Scott model belongs to Reaction--Diffusion and should not be
presented as a Boids model.

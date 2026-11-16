# Vampire: The Masquerade 20th Anniversary -- Core Mechanics

Personal horror in a d10 dice-pool system (the Storyteller System).
The players' characters are Kindred: vampires who need blood, hide
from mortals behind the Masquerade, and fight the Beast inside them
while their Humanity slips.

Page references are to the V20 core book (*Vampire: The Masquerade
20th Anniversary Edition*).

**Related V20 files:**
- Combat, damage, frenzy, sunlight, torpor: `systems/vtm-v20/rules-reference.md`
- Chronicle and session procedures, experience: `systems/vtm-v20/session-procedures.md`
- Building a character: `systems/vtm-v20/character-generation.md`

## Dice Pool Resolution

- Pool = **Attribute + Ability** (e.g. Dexterity + Firearms). Some
  rolls use one Trait alone (Strength to lift, Humanity to resist
  degeneration).
- A pool built on a Trait rated up to 10 (Humanity, Path,
  Willpower) never adds another Trait.
- Roll that many d10s against a **difficulty** (always 2-10,
  usually 3-9; 6 when nothing says otherwise).
- Each die at or above the difficulty is one **success**. A **10 is
  always a success**, whatever the difficulty.
- Each **1** cancels one success.

*Source: V20 pp. 247-251*

### Botch

- **Failure:** no successes left once the 1s are taken off.
- **Botch:** not a single success rolled *and* at least one 1. If any
  success came up, even one later cancelled, it is only a failure.
- A botch is a dramatic misfortune the Storyteller describes; it
  should twist the scene, not just embarrass the character.
- Optional: each player and the Storyteller get one "free" botch per
  session (the first one doesn't count).

### Rolling Without an Ability

| Ability group | With 0 dots |
|------|------|
| Talents | Roll the Attribute alone |
| Skills | Roll the Attribute alone at +1 difficulty |
| Knowledges | No roll at all, unless the Storyteller allows it |

*Source: V20 pp. 107, 257*

### Difficulty

| Difficulty | Task |
|:---:|------|
| 3 | Trivial |
| 4 | Easy |
| 5 | Straightforward |
| 6 | Standard (default) |
| 7 | Challenging |
| 8 | Difficult |
| 9 | Extremely difficult |
| 10 | Rare; odd odds (a bigger pool can botch more often) |

*Source: V20 p. 249*

### Degrees of Success

| Successes | Result |
|:---:|--------|
| 1 | Marginal |
| 2 | Moderate |
| 3 | Complete |
| 4 | Exceptional |
| 5+ | Phenomenal |

### Specialties

An Attribute or Ability at 4+ can take a **specialty** (e.g.
Firearms: Pistols). When it applies, each 10 rolled counts as two
successes.

*Source: V20 p. 96*

### Automatic Success

When the pool is at least the difficulty, the Storyteller can skip a
routine roll: the result is one success (marginal). Never in combat
or under stress. Rolling anyway can buy more successes, at the risk
of failing.

*Source: V20 pp. 250-251*

### Trying It Again

After a failed attempt at a task that frustrates (climbing, searching
an archive, interrogating), each retry gets +1 difficulty over the last
(+1, then +2, ...). Not used for things like missed shots in a fight.

*Source: V20 p. 251*

### Multiple Actions

Declare all the actions, take the **smallest** of their pools, and split
that many dice among them. Very different actions can also get a
difficulty increase. **Celerity** grants extra actions without splitting
pools (`disciplines.md`).

*Source: V20 p. 248*

### Reflexive Actions

Take no time and don't use up the turn's action: spending blood to
raise an Attribute, soaking damage, a Humanity roll.

*Source: V20 p. 247*

## Roll Types

*Source: V20 pp. 251-253*

### Simple Roll

One roll, one success needed. Most actions.

### Extended Roll

Roll again at each interval (a turn, a night, ...) and add up
successes until a target number is reached. A botch usually means
starting over, or failing for good if the Storyteller says so.

### Resisted Roll

Each side rolls, often against a difficulty set by the other side's
Traits. The winner keeps only the successes beyond the loser's, so a
contested win is rarely impressive. Resisted and extended together:
each turn, only the margin goes into the running total; first to the
target wins.

### Teamwork

Two or more characters roll their own pools and add the successes.
Pools are never merged. One botch can spoil the whole attempt, and
teamwork can hurt social rolls (too many voices).

## Willpower

**Spending a point:**
- One **automatic success** on an action, declared before the roll.
  Only one per turn. It can't be cancelled, not even by a botch. The
  Storyteller can forbid it on some actions (such as attacks).
- Resist an instinctive reaction (jerking away from sunlight) for a
  turn. The urge can come back.
- Hold off a derangement for a while (with the Storyteller's leave).
- Ignore wound penalties for one turn (not while incapacitated or in
  torpor).
- Take control of one action for a turn during a frenzy or
  Rötschreck (`rules-reference.md`).

**Regaining points:**
- The pool refills completely at the end of each **story** (not
  session), if the Storyteller agrees the characters earned it.
- Storyteller's options: one point each night on waking; one point
  for an outstanding achievement; one to three for acting out the
  character's Nature.

The rating (1-10) only goes up with experience.

*Source: V20 pp. 267-268*

## Traits at a Glance

| Group | Traits |
|-------|--------|
| Physical Attributes | Strength, Dexterity, Stamina |
| Social Attributes | Charisma, Manipulation, Appearance |
| Mental Attributes | Perception, Intelligence, Wits |
| Abilities | Talents, Skills, Knowledges (`skills.md`) |
| Advantages | Disciplines, Backgrounds, Virtues |
| Virtues | Conscience, Self-Control, Courage |
| Morality | Humanity (or a Path of Enlightenment) |
| Willpower | Rating 1-10, spent as points |
| Blood Pool | Vitae held, limited by Generation |

Ratings run 0-5 for mortals and most Kindred (1 poor, 2 average,
3 good, 4 exceptional, 5 superb). Lower Generations can go higher.

## Blood Pool and Generation

The vampire's vitae, in **blood points**. Generation is how far the
character is from Caine; lower is stronger.

| Generation | Max Trait | Blood Pool | Points / Turn |
|:---:|:---:|:---:|:---:|
| 3rd | 10 | ??? | ??? |
| 4th | 9 | 50 | 10 |
| 5th | 8 | 40 | 8 |
| 6th | 7 | 30 | 6 |
| 7th | 6 | 20 | 4 |
| 8th | 5 | 15 | 3 |
| 9th | 5 | 14 | 2 |
| 10th | 5 | 13 | 1 |
| 11th | 5 | 12 | 1 |
| 12th | 5 | 11 | 1 |
| 13th+ | 5 | 10 | 1 |

- **Max Trait:** highest permanent rating (not Humanity, Path or
  Willpower), which matters most for Attributes and Disciplines.
- **Points / Turn:** the most blood the vampire can spend in one
  turn, for any mix of uses.
- Elder vitae is concentrated: one point drunk from an elder can be
  worth two or more.

*Source: V20 pp. 268-270*

### Spending Blood

| Use | Cost |
|-----|------|
| Rise each night | 1 point, whether the vampire goes out or not |
| Heal one bashing or lethal health level | 1 point, while resting; one level per turn (more per turn for low Generations, up to the points / turn limit) |
| Heal one aggravated health level | A full day's rest + 5 points; at the end of that day, each extra level costs 5 more points + 1 Willpower |
| Raise a Physical Attribute by 1 for the scene | 1 point per dot, declared at the start of the turn. Up to Max Trait + 1 freely; dots past that fade 3 turns after the vampire stops spending. Never above 10 |
| Look alive for a scene (flush skin, breathe, have sex) | 8 − Humanity points (free at Humanity 8+). Not possible on a Path |
| Feed blood to another Kindred | As many points as given (three drinks make a blood bond) |
| Make a mortal or animal a ghoul | A dose of vitae |
| Activate a Discipline power | Only when the power says so |

### Feeding

- Up to **3 points per turn** from one vessel.
- Safe limit: about 20% of the vessel's blood (2 points from a
  human). Half the blood means hospital; all of it kills.
- Once the fangs break skin, the **Kiss** makes the victim stop
  resisting. Mortals with Willpower 9+ can fight it for a while; any
  Kindred can try a Self-Control/Instincts roll (difficulty 8).
- A wounded mortal has one fewer blood point per health level lost;
  mortals regain one point a day.

| Vessel | Blood Pool |
|--------|:---:|
| Vampire | 10+ |
| Werewolf | 20 |
| Average human | 10 |
| Child | 5 |
| Cow | 5 |
| Dog | 2 |
| Cat | 1 |
| Plasma bag | 1 |
| Bird | 1/2 |
| Bat / rat | 1/4 |

Animal blood and old blood are less nourishing.

*Source: V20 pp. 269-270*

### Hunger

V20 has no fixed hunger threshold. The Beast presses through three
rules:
- A **Self-Control/Instincts roll can't use more dice than the
  blood pool currently holds**. A vampire on 2 points rolls at most
  2 dice to resist frenzy.
- Blood is a frenzy trigger **when hungry**: smell (difficulty 3),
  sight (4), taste (6), higher in extreme cases
  (`rules-reference.md`).
- At **0 points**, the vampire loses a health level each time the
  rules call for spending blood (such as rising). Past
  Incapacitated this way, it falls into torpor until fed.

*Source: V20 pp. 268, 283, 298*

## Health

Seven health levels. The lowest marked box sets the penalty to every
action except reflexive ones like soak.

| Level | Penalty | Movement |
|-------|:---:|---------|
| Bruised | 0 | Normal |
| Hurt | -1 | Normal |
| Injured | -1 | Half running speed |
| Wounded | -2 | Can't run; loses dice if moving and attacking in one turn |
| Mauled | -2 | Hobble, 3 yards/turn |
| Crippled | -5 | Crawl, 1 yard/turn |
| Incapacitated | -- | Can only spend blood to heal; a vampire with no blood falls into torpor |

Past Incapacitated: torpor, then **Final Death** from aggravated
damage. Damage types (bashing, lethal, aggravated), soak, torpor
length and the optional "extras" rule are in `rules-reference.md`.

*Source: V20 pp. 282-283*

## Virtues, Humanity and Willpower

- **Conscience** — sense of right and wrong; rolled to avoid
  losing Humanity after a sin.
- **Self-Control** — rolled to resist frenzy.
- **Courage** — rolled to face fire and sunlight (Rötschreck).

At character creation: **Humanity = Conscience + Self-Control**,
**Willpower = Courage**. Vampires on a Path of Enlightenment use other
Virtues (Conviction, Instincts) instead (`humanity-paths.md`).

*Source: V20 pp. 80, 120*

## Topics in Other V20 Files

- **Combat** (initiative, maneuvers, damage, soak, staking): `systems/vtm-v20/rules-reference.md`
- **Frenzy and Rötschreck**: `systems/vtm-v20/rules-reference.md`
- **Blood bond, ghouls, diablerie, torpor**: `systems/vtm-v20/rules-reference.md`
- **Humanity hierarchy and Paths of Enlightenment**: `systems/vtm-v20/humanity-paths.md`
- **Clans and weaknesses**: `systems/vtm-v20/clans.md`
- **Disciplines and powers**: `systems/vtm-v20/disciplines.md`
- **Sects, titles, Traditions, boons**: `systems/vtm-v20/sects.md`
- **Experience and chronicle play**: `systems/vtm-v20/session-procedures.md`

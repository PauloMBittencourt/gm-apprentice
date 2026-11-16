# Vampire: The Masquerade 20th Anniversary -- Character Sheet

Blank markdown sheet for a V20 Kindred, laid out like the book's
sheet. Dots are written as numbers (Strength 3). How to fill it in:
`systems/vtm-v20/character-generation.md`.

In a vault, the PC note follows `shared/pc-body-structure.md`: this
sheet goes under `## Stat Sheet`, and the live tracks (blood,
Willpower, health) are kept in `## Current Status` (see the end of
this file).

V20 adds no frontmatter fields. Clan, Generation, sire and sect are
written in the Identity table below; the shared `occupation` field
holds the mortal concept and `age` the apparent age.

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | |
| **Player** | |
| **Chronicle** | |
| **Nature** | |
| **Demeanor** | |
| **Concept** | |
| **Clan** | _(or Caitiff; bloodline if any)_ |
| **Generation** | _(13th unless the Generation Background says otherwise)_ |
| **Sire** | |
| **Sect** | _(Camarilla, Sabbat, Anarch, independent)_ |
| **Embraced** | _(year; apparent age)_ |
| **Haven** | |

---

## Attributes

| Physical | | Social | | Mental | |
|----------|:---:|--------|:---:|--------|:---:|
| Strength | 1 | Charisma | 1 | Perception | 1 |
| Dexterity | 1 | Manipulation | 1 | Intelligence | 1 |
| Stamina | 1 | Appearance | 1 | Wits | 1 |

Note a specialty beside any Attribute at 4+.

---

## Abilities

| Talents | | Skills | | Knowledges | |
|---------|:---:|--------|:---:|------------|:---:|
| Alertness | 0 | Animal Ken | 0 | Academics | 0 |
| Athletics | 0 | Crafts | 0 | Computer | 0 |
| Awareness | 0 | Drive | 0 | Finance | 0 |
| Brawl | 0 | Etiquette | 0 | Investigation | 0 |
| Empathy | 0 | Firearms | 0 | Law | 0 |
| Expression | 0 | Larceny | 0 | Medicine | 0 |
| Intimidation | 0 | Melee | 0 | Occult | 0 |
| Leadership | 0 | Performance | 0 | Politics | 0 |
| Streetwise | 0 | Stealth | 0 | Science | 0 |
| Subterfuge | 0 | Survival | 0 | Technology | 0 |

Specialties (Ability at 4+): _(e.g. Firearms: pistols)_

Secondary Abilities (Hobby Talent, Professional Skill, Expert
Knowledge) go on extra rows, named.

---

## Advantages

### Disciplines

| Discipline | Rating | Powers known |
|------------|:---:|--------------|
| | | |
| | | |
| | | |

Thaumaturgy and Necromancy: list the primary Path, any secondary
Paths, and rituals known by level.

### Backgrounds

| Background | Rating | Who / what |
|------------|:---:|-----------|
| | | |
| | | |
| | | |

### Virtues

| Virtue | Rating |
|--------|:---:|
| Conscience _(or Conviction)_ | 1 |
| Self-Control _(or Instinct)_ | 1 |
| Courage | 1 |

---

## Merits and Flaws

| Merit / Flaw | Type | Cost |
|--------------|------|:---:|
| | Merit | |
| | Flaw | |

---

## Morality, Willpower and Blood

| Trait | Permanent | Current |
|-------|:---:|:---:|
| **Humanity** _(or Path: name)_ | | — |
| **Willpower** | | |
| **Blood Pool** | max by Generation | |
| **Blood per turn** | by Generation | — |

**Clan weakness:** _(one line, from `clans.md`)_

**Derangements:** _(Malkavians: the clan one first)_

---

## Health

| Level | Penalty | Damage |
|-------|:---:|:---:|
| Bruised | 0 | |
| Hurt | -1 | |
| Injured | -1 | |
| Wounded | -2 | |
| Mauled | -2 | |
| Crippled | -5 | |
| Incapacitated | — | |

Mark damage as `/` bashing, `X` lethal, `*` aggravated (worst type in
the top boxes).

---

## Combat

| Stat | Value |
|------|-------|
| **Initiative rating** | Dexterity + Wits |
| **Soak (bashing / lethal)** | Stamina + Fortitude (+ armour) |
| **Soak (aggravated)** | Fortitude (+ armour, fangs and claws only) |
| **Bite** | Dexterity + Brawl, +1 accuracy, Strength +1 aggravated |

| Weapon | Pool | Difficulty | Damage | Range | Rate | Clip | Conceal |
|--------|------|:---:|--------|:---:|:---:|:---:|:---:|
| | | | | | | | |

**Armour:** _(class, rating, penalty)_

---

## Experience

| Total earned | Spent | Unspent |
|:---:|:---:|:---:|
| 0 | 0 | 0 |

---

## In the Vault: Current Status Fields

The PC note's `## Current Status` (kept up to date by session-wrapup)
uses the shared fields plus three V20 ones:

```markdown
**Blood:** {current} / {max}
**Willpower:** {current} / {permanent}
**Health:** {e.g. Hurt (1 lethal), or unhurt}
**Location:** {where the PC is now}
**Condition:** {frenzy risk, staked, torpor, blood bond, derangement flare}
**Carrying:** {narratively-significant items in hand}
**Open threads:**
- {unresolved, forward-looking item}
**Knows (exclusive):** {secret/exclusive information this PC holds}
```

Permanent ratings (Humanity, Willpower rating, Disciplines) stay in the
Stat Sheet; change them only when experience is spent or Humanity is
lost, and say so in the session wrap-up.

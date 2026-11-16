# Vampire: The Masquerade 20th Anniversary -- Character Generation

Step-by-step guide for building a V20 Kindred, from concept to
freebie points, plus experience costs for advancing.

Page references are to the V20 core book.

## Published Site Defaults

When creating a PC entity file, set `display_meta` to control
which fields appear in the character's header on a published
campaign site. Recommended for V20:

```yaml
display_meta: [occupation, age, nationality]
```

V20 uses the shared PC fields as they are: `occupation` holds the
mortal concept (what the character was before the Embrace), and `age`
the apparent age (age at the Embrace). Clan, Generation, sire and sect
live in the Identity table of the Stat Sheet, not in frontmatter
(`systems/vtm-v20/character-sheet.md`).

## Before You Start

- **Every new character is a neonate**: Embraced recently, released
  by the sire, at most about 25 years as Kindred, and knowing little
  of Kindred society. Apparent age is the age at the Embrace.
- **The coterie needs a reason to exist.** Vampires are solitary;
  agree with the troupe why these Kindred work together.
- **The Storyteller sets the frame.** A Camarilla city chronicle may
  rule out Sabbat or independent clans; some clans may be held back as
  antagonists.
- Spend a session on creation and **preludes** (playing out the
  mortal life and the Embrace), one player at a time if needed.

*Source: V20 pp. 79, 83*

## Creation Workflow

1. **Concept** -- concept, Clan, Nature and Demeanor.
2. **Attributes** -- prioritise Physical / Social / Mental: 7 / 5 / 3.
3. **Abilities** -- prioritise Talents / Skills / Knowledges:
   13 / 9 / 5. None above 3 yet.
4. **Advantages** -- Disciplines 3, Backgrounds 5, Virtues 7.
5. **Finishing touches** -- Humanity, Willpower, blood pool; 15
   freebie points; optional Merits and Flaws (up to 7 points of
   Flaws).
6. **Spark of life** -- turn the dots into a person.

*Source: V20 p. 80*

## Step 1: Concept, Clan, Nature and Demeanor

### Concept

Who the character was before the Embrace: a short phrase is enough
("burned-out paramedic", "club-kid dealer"). It has no mechanics, but
it anchors what's left of the person.

| Family | Examples |
|--------|----------|
| Criminal | Mafioso, dealer, carjacker, fence |
| Drifter | Smuggler, junkie, biker, gambler |
| Entertainer | Musician, film star, club kid, model |
| Intellectual | Writer, student, scientist, philosopher |
| Investigator | Detective, beat cop, private eye |
| Kid | Runaway, urchin, gangbanger |
| Outsider | Refugee, conspiracy theorist |
| Politician | Judge, councillor, aide, speechwriter |
| Professional | Engineer, doctor, programmer, lawyer |
| Reporter | Journalist, blogger, paparazzo |
| Scenester | Goth, punk, barfly, hipster |
| Socialite | Dilettante, host, playboy |
| Soldier | Bodyguard, enforcer, mercenary |
| Worker | Trucker, farmer, construction labourer |

### Clan

The vampire's bloodline, always the sire's. Clans, their Disciplines
and weaknesses are in `systems/vtm-v20/clans.md`. A character may also
be **Caitiff** (clanless): no clan Disciplines and no clan weakness,
but scorned.

### Nature and Demeanor

Both are **Archetypes**. **Demeanor** is the mask shown to others and
has no mechanics. **Nature** is the true self, and acting it out
regains Willpower (`mechanics.md`). Archetype list: V20 pp. 87-96.

*Source: V20 pp. 80, 83-84*

## Step 2: Attributes

Every Attribute starts at **1** (Nosferatu and Samedi have
Appearance **0**). Add **7** dots to the primary group, **5** to the
secondary and **3** to the tertiary.

| Group | Attributes |
|-------|------------|
| Physical | Strength, Dexterity, Stamina |
| Social | Charisma, Manipulation, Appearance |
| Mental | Perception, Intelligence, Wits |

*Source: V20 p. 84*

## Step 3: Abilities

No free dots. **13** to the primary group, **9** to the secondary,
**5** to the tertiary. **No Ability above 3** at this step (freebies can
raise it later). Ability list: `systems/vtm-v20/skills.md`.

| Group | What it is |
|-------|------------|
| Talents | Intuitive; usable untrained |
| Skills | Trained; untrained at +1 difficulty |
| Knowledges | Studied; can't be rolled without a dot |

*Source: V20 p. 84*

## Step 4: Advantages

### Disciplines (3 dots)

Spread as the player likes (all three in one, or one each). With these
starting dots, only the **three clan Disciplines**; Caitiff choose any,
with the Storyteller's leave. Freebie dots can buy any Discipline (the
Storyteller may want an explanation). Powers:
`systems/vtm-v20/disciplines.md`.

**More inhuman vampires (optional):** a new character may take **4
Discipline dots and no Backgrounds** (fits the Sabbat).

### Backgrounds (5 dots)

Should fit the concept: a destitute street preacher shouldn't have
Resources. The Storyteller may forbid or push some.

| Background | What it measures |
|------------|------------------|
| Allies | Mortal friends and family who help |
| Alternate Identity | A false identity with papers |
| Black Hand Membership | Sabbat only: Black Hand members to call on |
| Contacts | Information sources |
| Domain | Feeding grounds recognised by Kindred society |
| Fame | Renown among mortals; −1 hunting difficulty per dot |
| Generation | How close to Caine (table below) |
| Herd | Vessels with free, safe access |
| Influence | Political power in mortal society |
| Mentor | A Kindred patron |
| Resources | Wealth, belongings, income |
| Retainers | Followers, guards, servants |
| Rituals | Sabbat only: ritae the character can lead |
| Status | Standing in Kindred society |

**Generation Background:** with no dots, the character is 13th
Generation.

| Dots | Generation | Blood Pool | Points / Turn |
|:---:|:---:|:---:|:---:|
| 0 | 13th | 10 | 1 |
| 1 | 12th | 11 | 1 |
| 2 | 11th | 12 | 1 |
| 3 | 10th | 13 | 1 |
| 4 | 9th | 14 | 2 |
| 5 | 8th | 15 | 3 |

Backgrounds can't be bought with experience later; they change through
play (a new friend, a windfall, diablerie).

### Virtues (7 dots)

Conscience, Self-Control and Courage each start at **1**; add **7**
dots. Vampires on a Path may take **Conviction** in place of
Conscience and **Instinct** in place of Self-Control, each starting at
**0** (Storyteller's leave; it marks the character as a monster). See
`systems/vtm-v20/humanity-paths.md`.

*Source: V20 pp. 82, 85-86, 110-119*

## Step 5: Finishing Touches

1. **Humanity** = Conscience + Self-Control (5 to 9). Path
   characters use the Path's own Virtues.
2. **Willpower** = Courage (1 to 5).
3. **Blood pool:** roll **one d10**; that's the blood the character
   starts play with (the only roll in creation).
4. **Freebie points: 15** to spend.
5. **Merits and Flaws (optional):** up to **7 points of Flaws** for
   extra freebies; Merits cost freebies. List: V20 pp. 479-494.

### Freebie Point Costs

| Trait | Cost per dot |
|-------|:---:|
| Attribute | 5 |
| Ability | 2 |
| Discipline | 7 |
| Background | 1 |
| Virtue | 2 |
| Humanity / Path | 2 |
| Willpower | 1 |

The book records Humanity and Willpower before freebies are spent, and
only says outright that Virtues raised with *experience* leave them
unchanged. Whether a Virtue bought with freebies also raises Humanity
or Willpower is the Storyteller's call; settle it before creation.

*Source: V20 pp. 82, 86*

## Step 6: Spark of Life

The dots aren't the character yet. For each notable Trait, decide why
it's there: what Appearance 3 looks like, where Firearms came from, who
the Ally really is and what they suspect. Then settle the details:
looks, mannerisms, haven, the sire, the Embrace, and what the
character still clings to from mortal life.

*Source: V20 pp. 86-87*

## Experienced Characters

For an ancilla or elder chronicle, build a neonate first, then grant
experience. A rough guide for "idle" Kindred: Discipline dots about
equal to the square root of their age in years.

| Age category | Experience |
|--------------|:---:|
| Neonate | 0-35 |
| Ancilla | 75-220 |
| Elder | 250-600 |
| Methuselah | 1000+ |

*Source: V20 p. 79*

## Experience Costs

| Trait | Cost |
|-------|------|
| New Ability | 3 |
| New Discipline | 10 |
| New Path (Necromancy or Thaumaturgy) | 7 |
| Attribute | current rating × 4 |
| Ability | current rating × 2 |
| Clan Discipline | current rating × 5 |
| Other Discipline | current rating × 7 |
| Caitiff Discipline | current rating × 6 (all of them) |
| Secondary Path (Necromancy or Thaumaturgy) | current rating × 4 |
| Virtue | current rating × 2 |
| Humanity / Path of Enlightenment | current rating × 2 |
| Willpower | current rating × 1 |

- **No Trait rises more than one dot per story.**
- Raising a Virtue does **not** raise Humanity, Path or Willpower.
- A new Ability or Discipline needs a teacher or study in the fiction
  as well as the points; a Mentor helps.
- The Storyteller can refuse a raise the story doesn't justify
  (Dominate that was never used; Humanity after murdering children).
- Backgrounds are not bought with experience.
- Awards per chapter and story: `systems/vtm-v20/session-procedures.md`.

*Source: V20 pp. 122-124*

## Validation Checklist

Check a finished starting character against these:

- [ ] Clan (or Caitiff), Nature and Demeanor chosen.
- [ ] Attributes: each at least 1 (Appearance 0 for Nosferatu/Samedi),
      7/5/3 added before freebies.
- [ ] Abilities: 13/9/5, none above 3 before freebies.
- [ ] Disciplines: 3 dots from clan Disciplines (any for Caitiff), or
      4 and no Backgrounds under the optional rule.
- [ ] Backgrounds: 5 dots (Sabbat-only ones only for Sabbat).
- [ ] Virtues: each starting dot counted, plus 7.
- [ ] Humanity = Conscience + Self-Control; Willpower = Courage (before
      freebies raise them).
- [ ] Freebies: 15 + Flaw points, spent at the costs above; Flaws at
      most 7.
- [ ] No Trait above the Generation's maximum (5 for 8th and higher).
- [ ] Starting blood pool rolled (1d10), not above the Generation's
      pool.

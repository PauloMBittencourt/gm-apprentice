# Attribution and Licensing

## Where the notices live

Each system directory under `skills/ttrpg-expert/systems/` ships one
`NOTICE.md` with the licence notice for the files in it. An install
through `npx skills` copies the skill's folder with it, and not this
document. The individual reference
files carry no notice of their own.

CC-BY 3.0 (section 4(b)) asks for attribution "reasonable to the medium
or means" being used, and the ORC License asks for notices in a
"reasonable manner based on the medium, means, and context" without
specifying where they appear. Neither text says the notice must repeat
on every file, so one per system is used, which also avoids repeating
the same text in every file that is read.

`scripts/attribution_check.py` runs in CI and fails if a system has no
`NOTICE.md`, or if the notice lacks its required text. The Call of Cthulhu notice also records, file by file,
which files derive from BRP, which from Lovecraft's public-domain
fiction, and which are our own descriptions of mechanics.

## Open Game Content

### Dungeons & Dragons System Reference Document 5.1

This work includes material from the System Reference Document
5.1 ("SRD 5.1") by Wizards of the Coast LLC, available at
https://dnd.wizards.com/resources/systems-reference-document. The
SRD 5.1 is licensed under the Creative Commons Attribution 4.0
International License, available at
https://creativecommons.org/licenses/by/4.0/legalcode.

Content derived from the SRD 5.1 is limited to a few item, weapon and
feature names (such as `Rope, Hempen` and `Crossbow, Light`) used in the
D&D Beyond sync tests and comments, where D&D Beyond still spells them
that way.

### Dungeons & Dragons System Reference Document 5.2

This work includes material from the System Reference Document
5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at
https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under
the Creative Commons Attribution 4.0 International License,
available at
https://creativecommons.org/licenses/by/4.0/legalcode.

Content derived from the SRD 5.2 includes: spell indexes and
descriptions, magic item indexes and descriptions, and full
monster stat blocks (ability scores, attacks, damage dice, save
DCs, traits, legendary actions) for 235 creatures.

The publish tool's D&D test fixtures
(`tools/publish/test/fixtures/with-dnd-pc/`) are seven original
characters (Brannoch Vale, Ilse Varn, Oriel Thackeray, Tamsin Reed,
Dov Ashgrove, Perrin Lowe, and Ilse Varn in the layout before
1.10.33), with one creature note (the Otherworldly Steed that Find
Steed calls) and one item note (a Wand of Magic Missiles) for their
links. They use SRD 5.2 names and numbers only (class, subclass,
species, background, feat, spell, skill, equipment and magic item
names; ability scores, proficiency, spell levels, ranges, durations,
hit dice, item weights, item charges and the steed's armour class,
hit points and speed), CC-BY 4.0. Every summary line is written in
our own words; no rules text is copied. The derived numbers,
carried weights and carrying capacities were filled in by
`dnd_sheet.py`, whose carrying factors are the SRD 5.2 Carrying
Capacity table's.

The run sheet reader's test fixtures
(`tools/publish/test/fixtures/run-sheet/`) are original notes whose
stat blocks use SRD 5.2 creature names and stat numbers only (the
Young White Dragon, Ice Mephit and Priest), CC-BY 4.0; no rules text
is copied.

`skills/shared/scripts/dnd_tables.py` holds numbers from the D&D 5.2
SRD (CC-BY 4.0) for the rules checks: each class's hit die, saving
throws, cantrips and prepared spells by level, the spell slot table, the
Warlock's pact slots, the Warlock levels at which a spell of level 6 to 9
is gained, the most cantrips a class option adds, and the level-20 ability
score caps of the Barbarian and Monk. Numbers only; no rules text is
copied. `shared` can install as a skill of its own without this document,
so `skills/shared/NOTICE.md` carries the SRD 5.2 notice for this file and
the SJG notice for `skills/shared/scripts/gurps_calc.py`.

The Python tools' D&D test characters (`tests/fixtures/dnd-pcs/*.md`)
are built from SRD 5.2 names and numbers only (CC-BY 4.0), with no
rules text. `tests/dnd_builder.py` and the D&D rules tests are built the
same way, with invented names for anything meant to be outside the SRD.

### Blades in the Dark / Forged in the Dark

This work is based on Blades in the Dark (found at
https://www.bladesinthedark.com/), product of One Seven Design,
developed and authored by John Harper, and licensed for our use
under the Creative Commons Attribution 3.0 Unported license
(https://creativecommons.org/licenses/by/3.0/).

Content derived from the SRD includes: action ratings and
resolution, position and effect, resistance and armor,
consequences and harm, stress and trauma, downtime activities,
faction mechanics (status, tier, development, faction turn),
crew advancement, playbook and crew-type frameworks, gathering
information, cohort rules, entanglements, ritual crafting, and
score procedures. All content is paraphrased; setting IP
(Doskvol, named factions, named NPCs) is excluded from
distributed files.

The `skills/ttrpg-expert/systems/fitd/` directory ships a
`NOTICE.md` carrying the attribution line above, with both URIs. An
install can ship those files without this document, and CC-BY 3.0 asks
for attribution "reasonable to the medium or means", so the notice
travels with the directory. (The gitignored `personal/` working
copies are excluded from the repo, so no install carries them.)

The publish tool's FitD sheet tests
(`tools/publish/test/helpers/pc-template.js`) fill the PC template
with an original scoundrel that uses a playbook name, a special
ability name and trauma names from the SRD, a one-line paraphrase of
that ability, and no setting names.

### Basic Roleplaying Universal Game Engine

This work includes material from Basic Roleplaying: Universal
Game Engine, available under the ORC License held in the
Library of Congress at TX-307-067 and available online at
https://www.chaosium.com/orclicense. Basic Roleplaying is
Copyright Chaosium Inc.

### Pathfinder Second Edition (Remaster)

This work includes Licensed Material used under the ORC License.

**ORC Notice.** This product is licensed under the ORC License
held in the Library of Congress at TX 9-307-067 and available
online at various locations including https://paizo.com/orclicense
and https://azoralaw.com/orclicense. All warranties are disclaimed
as set forth therein.

**Attribution.** The PF2e files under
`skills/ttrpg-expert/systems/pf2e/` are based on Licensed
Material from Pathfinder Player Core, Pathfinder Player Core 2,
Pathfinder GM Core, Pathfinder Monster Core, and Pathfinder
Monster Core 2 © Paizo Inc., whose rules text is Licensed
Material as declared in each work's own ORC notice (see each
book's notice for its complete attribution chain). All
descriptive text is paraphrased into original summaries;
Reserved Material — including Paizo's setting, characters, and
trade dress beyond what each notice licenses — is not knowingly
included. Content was sourced via an ORC-filtered extraction of
the Foundry VTT pf2e system data and the PF2SRD (ORC)
compilation. This is free, non-commercial material, not
published, endorsed, or specifically approved by Paizo Inc.

The publish tool's PF2e sheet tests
(`tools/publish/test/helpers/pc-template.js`) fill the PC template
with an original character that uses names only (class, order,
ancestry, heritage, background, spell and skill names found in the
ORC dataset), with no rules text and no Reserved Material.

## GURPS

GURPS is a trademark of Steve Jackson Games, and its rules
and art are copyrighted by Steve Jackson Games. All rights
are reserved by Steve Jackson Games. This game aid is the
original creation of AntTheLimey and is released for free
distribution, and not for resale, under the permissions
granted in the
[Steve Jackson Games Online Policy](https://www.sjgames.com/general/online_policy.html).

The GURPS skill files in this project contain trait names,
point costs, page references, and short mechanical notes as
permitted by the SJG Online Policy. Content is curated from
the GURPS Basic Set (Characters and Campaigns) and GURPS
Martial Arts (perk names and page references only), and
organized into topic-based reference files and archetype
chargen kits.
See `skills/ttrpg-expert/systems/gurps-4e/sources.md` for
book coverage status. The `skills/ttrpg-expert/systems/gurps-4e/`
directory ships a `NOTICE.md` carrying the notice above. (The
gitignored `personal/` working copies are excluded from the repo, so no
install carries them.)

**GURPS rules charts in `skills/ttrpg-expert/systems/gurps-4e/`**
Source: *GURPS Basic Set 4th Edition* (Steve Jackson Games), except
where noted.
License: SJG Online Policy
(https://www.sjgames.com/general/online_policy.html).
Transformation: compact markdown tables of values and short notes; the
surrounding explanation is original wording. Item tables (weapons, armor,
gear, skills, spells, traits, modifiers) are benchmarked in CI against
the columns and note lengths of the public GCS master library
(`scripts/license_check.py`). The rules charts below have no GCS
equivalent and are recorded here instead. Page numbers come from the
GURPS rules index and were not checked against a physical copy; where
two pages are given, the first is the chart and the second is where it
is discussed.

- Damage by ST, thrust and swing — `mechanics.md`, "Damage Table":
  B16.
- Attribute and characteristic costs — `mechanics.md`,
  `character-generation.md`: B14–B16.
- Skill cost by difficulty and level — `mechanics.md`, "Skills": B170.
- Active defenses — `mechanics.md`, `combat.md`,
  `character-sheet.md`: B373; quick reference B556.
- Combat maneuvers — `combat.md`, `session-procedures.md`: B363.
- Hit locations, with penalty and DR modifier — `combat.md`: B552,
  discussed at B399.
- Damage types and abbreviations — `combat.md`: B268.
- Size, speed and range modifiers — `combat.md`: B550.
- Encumbrance levels and Basic Lift — `equipment-armor.md`,
  `chargen-kit-combat.md`, `chargen-kit-outdoor.md`,
  `character-sheet.md`: B17.
- Hiking and daily march — `chargen-kit-outdoor.md`: B351.
- Reaction table and modifiers — `social-rules.md`,
  `chargen-kit-social.md`: B559–B561.
- Self-control numbers and frequency of appearance — `social-rules.md`,
  `character-generation.md`: B120.
- Reputation and recognition — `social-rules.md`: B27.
- Language comprehension — `chargen-kit-social.md`: B24.
- Starting wealth by tech level — `character-generation.md`: B27.
- Character point totals by power level — `character-generation.md`:
  B487.
- Mana levels — `magic-rules.md`, `chargen-kit-magic.md`: B235.
- Energy cost reduction at high skill — `chargen-kit-magic.md`: B238.
- Power source modifiers, talents, anti-powers and psionic abilities —
  `powers-rules.md`, `chargen-kit-powers.md`: sourced from the GURPS
  Powers line; page numbers are not recorded in the files.

**`tests/shared-cases/gurps-calc.json`**
Source: `skills/shared/scripts/gurps_calc.py` in this repository, which
follows *GURPS Basic Set 4th Edition* (Steve Jackson Games).
License: SJG Online Policy
(https://www.sjgames.com/general/online_policy.html).
Transformation: the encumbrance level names and multipliers and the nine
skills that encumbrance penalises are copied from `gurps_calc.py`; the
case inputs and results are our own arithmetic. Names and numbers only.

**`tools/publish/lib/templates/gurps/blocks/reference.js`**
Source: *GURPS Basic Set 4th Edition* (Steve Jackson Games).
Tables reproduced: Humanoid Hit Location (p. B552) and
Size & Speed/Range (p. B550).
License: SJG Online Policy
(https://www.sjgames.com/general/online_policy.html).
Transformation: reproduced as an optional collapsible
reference appendix with citation, displayed only when the
user expands the details element.

**`tools/publish/lib/templates/gurps/blocks/tohit-rules.js`, `tools/publish/lib/templates/gurps/tohit-data.js`**
Source: *GURPS Basic Set 4th Edition*, *GURPS Martial Arts* and
*GURPS High-Tech* (Steve Jackson Games).
License: SJG Online Policy
(https://www.sjgames.com/general/online_policy.html).
Transformation: modifier names and numbers used in a sum, each
with its page reference in a code comment. Names and numbers only.

## Vampire: The Masquerade 20th Anniversary Edition

Vampire: The Masquerade and World of Darkness are trademarks of
Paradox Interactive AB. This is unofficial fan material, not
approved or endorsed by Paradox Interactive. V20 has no open
licence; the intended basis is the
[Dark Pack Agreement](https://paradoxinteractive.com/games/world-of-darkness/community/dark-pack-agreement).
Required notice: "Portions of the materials are the copyrights and
trademarks of Paradox Interactive AB, and are used with permission.
All rights reserved. For more information please visit
worldofdarkness.com." The pack's `NOTICE.md` carries it.
**Status: work in progress.** Maintainer approval of the Dark Pack
terms (non-commercial only; the Dark Pack logo wherever the material
is promoted) is still pending.

**System pack in `skills/ttrpg-expert/systems/vtm-v20/`**
Source: *Vampire: The Masquerade 20th Anniversary Edition* (Onyx Path
Publishing / Paradox Interactive).
License: Dark Pack Agreement (maintainer approval pending).
Transformation: mechanics summarised in original wording, as short
tables of names, costs, dice pools and difficulties, with a
`*Source: V20 p. X*` page reference on each section. No rules text,
setting prose or art is reproduced; elder powers and rituals above
level 5 are listed by name only. Each file was checked against the
book for accuracy. The directory ships a `NOTICE.md` carrying the
notice above.

- `mechanics.md`, `rules-reference.md` — dice, actions, combat, health,
  blood, Willpower, frenzy and Rötschreck: V20 Chapters Five and Six
  (pp. 247–302).
- `character-generation.md`, `character-sheet.md` — creation steps,
  freebie and experience costs: V20 Chapter Three (pp. 79–124) and
  the merits and flaws appendix (pp. 479–494).
- `clans.md` — the thirteen clans, Caitiff and their weaknesses: V20
  Chapter Two (pp. 33–73), with bloodlines from Chapter Ten
  (pp. 396–439) by name only.
- `disciplines.md` — Disciplines, Thaumaturgy and Necromancy paths and
  rituals: V20 Chapter Four (pp. 128–243).
- `humanity-paths.md` — degeneration, Humanity, Conviction and
  Instinct, eight Paths of Enlightenment (Hierarchies of Sins condensed
  to one paraphrased line per rating, rationales omitted), derangements:
  V20 Chapter Seven (pp. 309–339) and Chapter Six (pp. 289–292).
- `skills.md` — the 30 Abilities and the dramatic systems that use
  them: V20 Chapter Three (pp. 100–110) and Chapters Five and Six
  (pp. 254–266).
- `sects.md` — sects, the Six Traditions (paraphrased, not quoted),
  the Code of Milan (paraphrased), titles and boons: V20 Chapter One
  (pp. 20–26) and Chapter Two (pp. 38–47).
- `creatures.md` — ghouls, hunters and True Faith, werewolves, mages,
  faeries, ghosts, demons, animals and swarms; NPC templates reduced to
  key numbers: V20 Chapter Nine (pp. 368–392) and Appendix
  (pp. 496–503).
- `equipment-weapons.md` — melee, ranged and armour charts (names and
  numbers only, brand-name examples dropped): V20 pp. 280–281.
- `session-procedures.md` — chronicle building, prelude, hunting
  scenes, hunger, storytelling techniques and experience awards: V20
  Chapter Eight (pp. 345–366) and pp. 122–124.

## D&D Beyond

D&D Beyond is a service of Wizards of the Coast LLC. This project is
not affiliated with it and redistributes nothing from it.

`skills/shared/scripts/dnd_ddb.py` reads a public character at the
user's request and writes names, numbers and short key facts into the
user's own vault. The sync tests use invented characters, with SRD 5.1
and 5.2 names (both CC-BY 4.0).

## Referenced Frameworks and Concepts

The following frameworks and concepts are referenced in this
project's skill files with attribution to their creators:

- **The Three Clue Rule** and **Node-Based Scenario Design**
  by Justin Alexander (The Alexandrian,
  https://thealexandrian.net/)
- **Return of the Lazy Dungeon Master** and the Lazy DM
  prep method by Mike Shea (Sly Flourish,
  https://slyflourish.com/)
- **Five Room Dungeon** and **Campaign Seed Recipe** by
  Johnn Four (Roleplaying Tips,
  https://roleplayingtips.com/)
- **Action-Oriented Monsters** by Matthew Colville (MCDM,
  https://mcdm.gg/)
- **3-Line NPC** by Johnn Four (Roleplaying Tips)
- **The Monsters Know What They're Doing** by Keith Ammann
  (https://themonstersknow.com/)
- **Fronts** from Apocalypse World by D. Vincent Baker
- **Progress Clocks** from Blades in the Dark by John Harper
  (CC-BY 3.0, see above)
- **Adventure Shapes** and **Momentous & Inertial Adventure
  Design** by Scott Rehm (The Angry GM,
  https://theangrygm.com/)
- **CATS Method** (Concept/Aim/Tone/Subject) by Patrick
  O'Leary
- **Petersen's Onion Layer** by Sandy Petersen
- **Story-to-Campaign Adaptation** by Mythcreants
  (https://mythcreants.com/)

## Lovecraft Mythos

The works of H.P. Lovecraft referenced in this project are
in the public domain. Call of Cthulhu game-specific
expressions, trade dress, and setting content are Copyright
Chaosium Inc.

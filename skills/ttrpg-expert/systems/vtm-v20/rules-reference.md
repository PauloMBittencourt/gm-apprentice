# Vampire: The Masquerade 20th Anniversary -- Rules Reference

Rules for play beyond the core dice: combat, damage and soak,
torpor, fire and sunlight, frenzy and Rötschreck, the blood bond,
diablerie, and daytime. Core resolution, Willpower, blood and health
are in `systems/vtm-v20/mechanics.md`. Weapon and armour stats are in
`systems/vtm-v20/equipment-weapons.md`.

Page references are to the V20 core book.

## Combat Turns

A combat turn is about three seconds, in three stages.

### Stage One: Initiative

- Each combatant rolls **1d10 + initiative rating** (Dexterity +
  Wits). Highest acts first. Faster option: Dexterity + Wits + 6, no
  roll.
- Ties: higher rating first; still tied, both act at once.
- Wound penalties come off the rating; Celerity dots not used for
  extra actions add to it.
- **Declare in reverse order** (slowest first), so faster characters
  can react. Declare now any multiple actions, Disciplines and
  Willpower.
- A character can **delay** and act at any later point, even to
  interrupt someone slower.
- Extra actions (including Celerity's) all happen at the **end of the
  turn**, in initiative order. Defensive extras happen when needed.

### Stage Two: Attack

| Attack | Pool |
|--------|------|
| Unarmed close combat | Dexterity + Brawl |
| Armed close combat | Dexterity + Melee |
| Guns | Dexterity + Firearms |
| Thrown weapons | Dexterity + Athletics |

Default difficulty 6. No successes: a miss. A botch: the gun jams,
the blade breaks, an ally gets hit.

### Stage Three: Resolution

- Damage pool = the weapon or maneuver's damage **+ one die per
  extra success** on the attack roll (successes beyond the first).
- Roll damage at difficulty 6; each success is one health level.
- A damage pool never drops below one die. Damage rolls and soak
  rolls **can't botch**.
- Describe the result in the fiction, not just as numbers.

*Source: V20 pp. 271-273*

## Combat Maneuvers

Maneuvers use difficulty 6 unless they say otherwise; "accuracy" adds
dice to the attack roll.

### General Maneuvers

- **Abort:** swap a declared action for a block, dodge or parry before
  acting. Needs a Willpower roll (difficulty 6, reflexive) or a
  Willpower point. Failed roll: carry out the original action.
- **Ambush:** attacker's Dexterity + Stealth resisted by the target's
  Perception + Alertness. Attacker wins: one free attack, with the
  extra successes added to the attack pool. Tie: attacker still goes
  first, but the target may defend. Target wins: normal initiative.
  Someone already fighting can't be ambushed.
- **Blind fighting:** +2 difficulty; ranged attacks impossible.
  Heightened Senses and Eyes of the Beast help.
- **Flank / rear attacks:** +1 die from the flank, +2 from behind.
- **Movement:** half running distance and still act in the turn.
- **Multiple opponents (close combat):** +1 difficulty to attack and
  defend per opponent after the first (max +4).

### Targeting

| Target | Difficulty | Damage |
|--------|:---:|:---:|
| Medium (limb, briefcase) | +1 | No modifier |
| Small (hand, head, phone) | +2 | +1 |
| Precise (eye, heart, lock) | +3 | +2 |

### Defensive Maneuvers

A defence is a **resisted roll** against the attack. The attack hits
only if it scores more successes, and then only with the excess.

| Maneuver | Pool | Stops |
|----------|------|-------|
| Block | Dexterity + Brawl | Bashing hand-to-hand attacks; lethal or aggravated ones only with Fortitude or armour |
| Dodge | Dexterity + Athletics | Any attack, given room to move; against guns, ends behind cover or prone |
| Parry | Dexterity + Melee | Brawl and Melee attacks; parrying a bare-handed attacker with a lethal weapon can hurt them (weapon damage + extra successes) |

- Defences can be part of a multiple action (strike, then block).
- **Full defence:** spend the whole turn defending; full pool on the
  first defence, one die less on each one after.

*Source: V20 pp. 274-275*

### Close Combat Maneuvers

| Maneuver | Pool | Accuracy | Difficulty | Damage |
|----------|------|:---:|:---:|--------|
| Bite | Dexterity + Brawl | +1 | Normal | Strength +1, aggravated; needs a clinch, hold or tackle first |
| Claw | Dexterity + Brawl | Normal | Normal | Strength +1; aggravated with Feral Claws, lethal with Vicissitude bone spurs |
| Clinch | Strength + Brawl | Normal | Normal | Strength; carries over each turn |
| Disarm | Dexterity + Melee | Normal | +1 | Special: successes beyond the target's Strength knock the weapon away |
| Hold | Strength + Brawl | Normal | Normal | None; carries over until the target wins a Strength + Brawl contest |
| Kick | Dexterity + Brawl | Normal | +1 | Strength +1 |
| Strike | Dexterity + Brawl | Normal | Normal | Strength |
| Sweep | Dexterity + Brawl/Melee | Normal | +1 | Strength; knockdown (Dexterity + Athletics, difficulty 8, to stay up) |
| Tackle | Strength + Brawl | Normal | +1 | Strength +1; both roll Dexterity + Athletics (difficulty 7) or fall |
| Weapon Strike | Dexterity + Melee | Normal | Normal | Weapon |

- Unarmed attacks do bashing damage unless the maneuver says
  otherwise. Every reference to Strength includes **Potence**.
- **The Kiss as an attack:** resolved like a bite but inflicts no
  damage; once it lands, the vampire drains at the normal rate and
  the victim usually can't resist. Licking the wound closes it.
- **Clinch:** the first turn deals Strength damage; after that,
  each side either deals Strength damage automatically or tries to
  break free (resisted Strength + Brawl). Nothing else until it ends.
- **Weapon length:** someone held off by a longer weapon must close a
  yard first and loses a die from the attack.

*Source: V20 pp. 276-277, 279*

### Ranged Combat Maneuvers

| Maneuver | Accuracy | Difficulty | Notes |
|----------|:---:|:---:|-------|
| Aiming | +1 per turn (max Perception) | Normal | Needs Firearms 1; a scope adds +2 the first turn; nothing else that turn; not on targets faster than a walk |
| Automatic Fire | +10 | +2 | Empties the clip (must be half full); damage as one bullet; no targeting |
| Multiple Shots | Split pool | Normal | One shot per target, up to the gun's rate |
| Strafing | +10 | +2 | Empties the clip over up to 3 yards; successes shared among targets; dodges at +1 |
| Three-Round Burst | +2 | +1 | Uses three rounds; damage as one bullet |
| Two Weapons | Split pool | +1 off-hand | A multiple action |
| Reloading | -- | -- | One full turn; can be part of a multiple action |

**Range:** up to the listed range at difficulty 6; up to twice that at
difficulty 8; within 2 yards (point blank) at difficulty 4.

**Cover:**

| Cover | Attacker's difficulty |
|-------|:---:|
| Light (prone) | +1 |
| Good (behind a wall) | +2 |
| Superior (only the head shows) | +3 |

Shooting back from cover is at one less than the listed penalty.
Penalties stack when both sides are in cover.

*Source: V20 pp. 277-278*

### Maneuver Complications

- **Blinded:** attacks against the target get +2 dice; the blind
  character is at +2 difficulty on everything.
- **Dazed:** damage that gets past soak is more than the target's
  Stamina (mortals) or Stamina + 2 (vampires) in one attack: the target
  loses its next turn.
- **Immobilized:** +2 dice to hit a held but struggling target;
  automatic hits on one fully helpless (bound, staked).
- **Knockdown:** roll Dexterity + Athletics. Success: up at once, -2
  initiative next turn. Failure: next action spent getting up. Botch: a
  bashing level from the fall.

### Stake Through the Heart

Target the heart (**difficulty 9**) with a wooden stake and deal at
least **three health levels** of damage: the vampire is paralysed, not
destroyed, until the stake comes out. Still aware (and can use
sensory powers like Auspex), but can't move or spend blood.

*Source: V20 pp. 279-280*

## Damage, Torpor and Death

### Damage Types and Soak

| Type | Sources | Mortals soak with | Vampires soak with | Mark |
|------|---------|------|------|:---:|
| Bashing | Fists, clubs, falls; **guns against vampires** (unless aimed at the head) | Stamina | Stamina + Fortitude; damage left after soak is **halved** (round down) | / |
| Lethal | Blades, bullets (against mortals, or a vampire's head), stakes | Can't soak | Stamina + Fortitude | X |
| Aggravated | Fire, sunlight, vampire fangs, Feral Claws, werewolf teeth and claws | Can't soak (taken as lethal; no harm from sunlight) | **Fortitude only** | * |

- **Soak** is a reflexive roll (no action, no split pool) at
  difficulty 6. Each success takes one health level off the damage.
- Aggravated is marked above lethal, lethal above bashing; normal
  damage is always healed first.
- Guns against vampires: bashing, unless the shooter targets the head
  (difficulty 8), then lethal.

*Source: V20 pp. 272-273, 284-285*

### Armour

Adds its rating to soak against bashing, lethal, and aggravated
damage from fangs and claws. **Never against fire or sunlight.** Its
penalty comes off Dexterity-based pools. If one attack's damage dice
are at least twice the rating, the armour is destroyed. Targeting an
unprotected spot ignores it (usually +1 or +2 difficulty). Ratings:
`equipment-weapons.md`.

*Source: V20 pp. 274, 280*

### Optional Rule: Extras

Nameless thugs (mortals, ghouls) get only four health levels: Hurt
(-1), Maimed (-3), Incapacitated, Dead. They retreat, surrender or drop
after a few hits, so the real fight can start.

*Source: V20 p. 284*

### Torpor and Final Death

- **Incapacitated:** collapses; can only spend blood to heal. More
  bashing or lethal damage sends a vampire into torpor; one more
  aggravated level is Final Death.
- **Torpor from blood loss:** at 0 blood, each time blood must be
  spent the vampire loses a health level instead. Past Incapacitated
  it falls into torpor, and rises as soon as someone feeds it a blood
  point.
- **Torpor from wounds** lasts a time set by Humanity or Path (table
  below). Then spend a blood point and make an Awakening roll; on a
  failure, try again the next night. With no blood it can't rise
  until fed. It rises at Crippled and should feed at once.
- **Voluntary torpor:** a deeper day-sleep; the vampire can rise after
  half the time with an Awakening roll and needs no nightly blood.
- **Final Death:** one aggravated level past Incapacitated or in
  torpor, or massive bodily destruction (beheaded, crushed, shredded).
- **Mortals** have no torpor: past Incapacitated, they die.

| Humanity / Path | Torpor length |
|:---:|------|
| 10 | One day |
| 9 | Three days |
| 8 | One week |
| 7 | Two weeks |
| 6 | One month |
| 5 | One year |
| 4 | One decade |
| 3 | Five decades |
| 2 | One century |
| 1 | Five centuries |
| 0 | A millennium or more |

### Deterioration

A staked or paralysed vampire still burns one blood point a night. Once
empty, it loses a health level a day, withering into a mummified
husk; after about a week (Incapacitated) it falls into torpor and needs
at least four blood points to rise. It wakes ravenous and attacks the
nearest blood. A favourite torture of hunters and the Sabbat.

*Source: V20 pp. 282-284, 293*

## Fire, Sunlight and Other Hazards

### Fire

Aggravated, ignores armour, soaked with **Fortitude only**. The fire's
heat sets the soak difficulty; its size sets the damage. Fire damage
is **automatic** each turn in contact: no damage roll.

| Soak difficulty | Heat |
|:---:|------|
| 3 | Candle |
| 5 | Torch |
| 7 | Bunsen burner |
| 8 | Electrical fire |
| 9 | Chemical fire |
| 10 | Molten metal |

| Levels / turn | Size |
|:---:|------|
| 1 | Torch; part of the body in the flames |
| 2 | Bonfire; half the body |
| 3 | Raging inferno; the whole body |

Burned to Mauled: -1 Appearance until healed to Bruised. To Crippled or
Incapacitated: -2.

*Source: V20 p. 297*

### Sunlight

Aggravated and automatic each turn. Only a vampire with **Fortitude**
can soak it, with a pool equal to the Fortitude rating alone. Looking
into direct sun blinds at once. Moonlight is mostly harmless.

| Soak difficulty | Light |
|:---:|------|
| 3 | Faint light through a closed curtain; heavy cloud; twilight |
| 5 | Fully covered: heavy clothes, sunglasses, gloves, wide hat |
| 7 | Indirect light through a window or thin curtain |
| 9 | Outdoors on a cloudy day; one direct ray; sun in a mirror |
| 10 | Direct, unclouded sun |

| Levels / turn | Exposure |
|:---:|------|
| 1 | A small part (a hand, part of the face) |
| 2 | A large part (a leg, an arm, the head) |
| 3 | Half the body or more (thin clothes) |

*Source: V20 p. 302*

### Other Hazards

- **Falling:** one die of bashing damage per 10 feet (3 m), soaked
  normally; sharp landings may make it lethal. At 100 feet (30 m) or
  more: 10 dice of lethal damage, and armour counts at half.
- **Electrocution:** lethal damage each turn of contact (wall socket 1,
  security fence 2, car battery or junction box 3, main line or subway
  rail 4). Pull away with a Strength roll (difficulty 5 for vampires).
  A botched soak makes it aggravated.
- **Disease:** vampires don't get sick but can carry blood-borne
  illness from victim to victim. Intelligence + Medicine (difficulty 7)
  spots it; a failure means a Stamina roll (difficulty 6) to avoid
  infection; a botch makes the vampire a carrier.
- **Temperature:** extreme heat (over 100 °C) can count as fire; deep
  cold can cost blood or Dexterity dice.
- **Drugs and alcohol in the victim's blood** affect the vampire who
  drinks it (see the book for each drug).

*Source: V20 pp. 295-296, 301-302*

## The Beast

### Frenzy

The Beast takes over in rage or hunger. Usually lasts a scene.

**Resisting:** a **Self-Control** roll (never more dice than the
current blood pool) against the provocation's difficulty, often 6-8.
If the frenzy would lead to an atrocity (killing an innocent), the
Storyteller can use 9 − Conscience instead. Vampires with Instincts
always frenzy and try to steer it (`humanity-paths.md`).

- **Five successes** in total resist it completely.
- Each success short of five holds the Beast off for a turn; roll
  again to add more.
- **Failure:** the character frenzies.
- **Botch:** stays in frenzy as long as the Storyteller says, and may
  gain a related derangement.

| Provocation | Difficulty |
|-------------|:---:|
| Smell of blood (when hungry) | 3+ |
| Sight of blood (when hungry) | 4+ |
| Being harassed | 4 |
| Life-threatening situation | 4 |
| Malicious taunts | 4 |
| Physical provocation | 6 |
| Taste of blood (when hungry) | 6+ |
| Loved one in danger | 7 |
| Outright public humiliation | 8 |

**In frenzy:**
- Ignores all wound penalties until it ends.
- +2 difficulty for others to Dominate or mentally control the
  vampire; −2 difficulty for the vampire to resist such control.
- Never needs Willpower rolls; immune to Rötschreck.
- Hungry: feeds from the nearest vessel without care. Angry: destroys
  the cause, then anyone near, friends included.
- **Willpower point:** control one action for a turn (let the victim
  run, let someone apologise). It doesn't end the frenzy.
- Acts committed in frenzy can call for degeneration rolls.

The Camarilla sees frenzy as shameful weakness; the Sabbat tries to
ride it.

*Source: V20 pp. 297-299*

### Rötschreck (the Red Fear)

Panic before fire or sunlight: the vampire flees blindly and tears
through anything in the way. Harmless sources under the vampire's
control (a lit cigarette at a club) don't trigger it unless they turn
threatening.

**Resisting:** a **Courage** roll; five successes in total resist it
completely, fewer hold it off for a while. Failure: flight. Botch:
immediate frenzy, lasting as long as the Storyteller says. Restraining
a vampire in Rötschreck gets you attacked. A Willpower point keeps
control for one turn.

| Provocation | Difficulty |
|-------------|:---:|
| Lighting a cigarette | 3 |
| Sight of a torch | 5 |
| Bonfire | 6 |
| Obscured sunlight | 7 |
| Being burned | 7 |
| Direct sunlight | 8 |
| Trapped in a burning building | 9 |

*Source: V20 p. 299*

## Vitae Between Kindred

### Blood Bond

Drinking a single vampire's blood on **three separate nights** makes
the drinker (mortal, ghoul or Kindred) its **thrall**, bound to the
**regnant**. The Embrace counts as the first drink.

| Drinks | Effect |
|:---:|--------|
| 1 | Strong feelings toward the vampire, love or hate |
| 2 | The vampire matters in the drinker's life; harming them may need a Willpower roll; Social rolls against the drinker at −1 difficulty |
| 3 | Full bond: the regnant comes before lovers and family; can **Dominate** the thrall by voice alone (no eye contact); resisting their mind control is at +2 difficulty |

- A full bond is exclusive: no second regnant until it fades, and it
  wipes out all lesser bonds. Lesser bonds to several vampires can
  exist side by side.
- Feeding and good treatment strengthen it; neglect and abuse wear it
  down.
- Higher Generation still can't Dominate lower, bond or not.
- **Resisting for a moment:** Willpower roll (usually difficulty 8, max
  9) needing as many successes as drinks taken, then spend a Willpower
  point. Freedom lasts from a scene (plotting against the regnant) down
  to a turn (attacking them); more Willpower extends it.
- **Breaking it:** no contact and no drinks for (12 − Willpower) months
  lowers it one step; down to zero ends it. Killing the regnant may
  shatter it, or not.

### The Vaulderie (Sabbat)

The Sabbat's communal blood rite. Each participant gets a **Vinculum**
rating (1-10) toward each other member, rolled on a die the first time
and adjusted at each later rite (higher roll: +1; a 1: −1). Vinculi
never fade, and repeated rites can wear down a blood bond (the vampire
must enter the rite nearly empty).

| Vinculum | Loyalty |
|:---:|------|
| 10 | Would die or kill for them |
| 8-9 | Would face great danger or spend major resources |
| 6-7 | Would fight for them, even at moderate risk |
| 4-5 | Helps when it's no great risk or bother |
| 2-3 | Loyal only while it suits own plans |
| 1 | No pull at all |

When Vinculi pull in different directions, roll each party's Vinculum
as a pool: difficulty 5 for the one the character would favour
anyway, 7 for the others. Most successes wins the character's help.

*Source: V20 pp. 286-289*

### Diablerie

Drinking a vampire's soul. The Camarilla's worst crime.

1. Drain all the victim's blood, taken straight from the body.
2. Keep drinking: extended **Strength** roll (difficulty 9). Each
   success is one automatic, unsoakable aggravated level on the
   victim. When its last level goes, the soul passes to the
   diablerist and the body begins to rot.
3. Only one diablerist per victim. Attacks against a vampire
   mid-diablerie are at **difficulty 2**.

**Rewards:**
- Euphoria: Self-Control/Instincts roll (difficulty 10 − Humanity or
  Path) to keep control. Some Kindred become addicts.
- Victim of lower Generation: the diablerist's Generation drops by one
  (more if the victim was five or more Generations lower, or ancient),
  with all its benefits.
- Elder vitae can raise Disciplines by a dot or more for a scene.

**Perils:**
- **Aura stains:** black veins visible to Aura Perception, lasting
  years equal to the Generation gap (minimum one). The Path of Blood
  can detect it for centuries.
- **Taint:** for a month per Generation gained, sensitive Kindred feel
  something is wrong: Perception roll (difficulty 12 − their Humanity).
  Path followers rarely notice.
- **Humanity:** at least one dot lost, with no roll. Vicious cases also
  get a Conscience roll (difficulty 8) to avoid losing more.
- The Inner Circle allows diablerie only by a sire on a childe under a
  blood hunt. Hunters may drain the victim dry but must stop there.

*Source: V20 pp. 293-295*

## Daytime

### Awakening

A vampire disturbed in its haven by day rolls **Perception (+ Auspex)**
at difficulty 8 to notice. To wake: **Humanity or Path** roll
(difficulty 8). Each success is one turn awake; five successes, the
whole scene. Failure: back to sleep (can try again if disturbed again);
botch: asleep until sunset.

While up during the day, **no pool can exceed the Humanity or Path
rating**.

*Source: V20 pp. 262-263*

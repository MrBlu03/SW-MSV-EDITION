# SW-MSV-EDITION vs PHB Format Comparison Report

> Comprehensive audit of all 19 MSV XML files against the official PHB XML format used by Aurora Builder.

---

## Table of Contents

1. [Systematic Issues (All Files)](#1-systematic-issues-all-files)
2. [sw-msv-edition.index](#2-sw-msv-editionindex)
3. [source.xml](#3-sourcexml)
4. [languages.xml](#4-languagesxml)
5. [backgrounds.xml](#5-backgroundsxml)
6. [weapons.xml](#6-weaponsxml)
7. [items-armor.xml](#7-items-armorxml)
8. [items-tools.xml](#8-items-toolsxml)
9. [items-instruments.xml](#9-items-instrumentsxml)
10. [items-explosives.xml](#10-items-explosivesxml)
11. [items-healing.xml](#11-items-healingxml)
12. [feats.xml](#12-featsxml)
13. [proficiencies.xml](#13-proficienciesxml)
14. [species.xml](#14-speciesxml)
15. [fighting-styles.xml](#15-fighting-stylesxml)
16. [maneuvers.xml](#16-maneuversxml)
17. [class-knight.xml](#17-class-knightxml)
18. [class-warrior.xml](#18-class-warriorxml)
19. [class-scout.xml](#19-class-scoutxml)
20. [class-marauder.xml](#20-class-marauderxml)
21. [class-inquisitor.xml](#21-class-inquisitorxml)
22. [Summary of Severity Levels](#22-summary-of-severity-levels)

---

## 1. Systematic Issues (All Files)

These issues appear consistently across most or all MSV files.

### 1a. Missing `<info>` Blocks (CRITICAL)

**Affects:** ALL files except `source.xml` and `sw-msv-edition.index`

Every PHB XML file has an `<info>` block as the first child of `<elements>`. This is used by Aurora Builder for version tracking and file updates.

**PHB Pattern (from fighter-champion.xml):**
```xml
<elements>
  <info>
    <update version="0.0.1">
      <file name="fighter-champion.xml" url="https://raw.githubusercontent.com/.../fighter-champion.xml" />
    </update>
  </info>
  <!-- elements follow -->
</elements>
```

**What to add** to each file as the first child of `<elements>`:
```xml
<info>
  <update version="0.0.1">
    <file name="FILENAME.xml" url="https://raw.githubusercontent.com/YourRepo/.../FILENAME.xml" />
  </update>
</info>
```

**Files needing `<info>` block added after `<elements>` tag:**
| File | Line to insert after |
|------|---------------------|
| languages.xml | Line 2 |
| backgrounds.xml | Line 2 |
| weapons.xml | Line 2 |
| items-armor.xml | Line 2 |
| items-tools.xml | Line 2 |
| items-instruments.xml | Line 2 |
| items-explosives.xml | Line 2 |
| items-healing.xml | Line 2 |
| feats.xml | Line 2 |
| proficiencies.xml | Line 2 |
| species.xml | Line 2 |
| fighting-styles.xml | Line 2 |
| maneuvers.xml | Line 2 |
| class-knight.xml | Line 2 |
| class-warrior.xml | Line 2 |
| class-scout.xml | Line 2 |
| class-marauder.xml | Line 2 |
| class-inquisitor.xml | Line 2 |

**Severity: CRITICAL** — Aurora Builder uses `<info>` for update checking. Without it, files won't auto-update.

---

### 1b. `<sheet>` Description Verbosity (LOW-MEDIUM)

**Affects:** All class files (knight, warrior, scout, marauder, inquisitor)

PHB `<sheet>` descriptions are **concise summaries** with Aurora Builder template variables like `{{level:fighter}}`, `{{strength:modifier}}`, etc. MSV files copy the full `<description>` text verbatim into `<sheet>`.

**PHB Pattern (Remarkable Athlete):**
```xml
<sheet>
  <description>When you make a running long jump, the distance you can cover increases by {{strength:modifier}} feet.</description>
</sheet>
```

**MSV Pattern (Know Your Enemy, class-warrior.xml ~L367):**
```xml
<sheet>
  <description>If you spend at least 1 minute observing or interacting with another creature outside combat, you can learn certain information about its capabilities compared to your own. The GM tells you if the creature is your equal, superior, or inferior in regard to two of the following characteristics of your choice: Strength score, Dexterity score, Constitution score, Armour Class, Current Hit Points.</description>
</sheet>
```

**Fix:** Shorten all `<sheet><description>` entries to concise summaries. Use template variables where applicable.

**Severity: LOW** — Functional but creates cluttered character sheets.

---

## 2. sw-msv-edition.index

**Status: ✅ GOOD** — Properly formatted with `<info>` block, `<name>`, `<description>`, `<author>`, and `<update>` with file listings.

No issues found.

---

## 3. source.xml

**Status: ✅ MOSTLY GOOD** — Has proper `<info>` block and well-formed Source element.

### Minor Notes:
- **Line ~25-26:** Has `<set name="supplement">true</set>` and `<set name="homebrew">true</set>` — these setters don't exist in the PHB source.xml but are **intentional for homebrew sources** and are correct.
- No fixes needed.

**Severity: NONE**

---

## 4. languages.xml

### Issue 4a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 4b: ALL Languages Missing `<setters>` Block (HIGH)
**Lines affected:** Every `<element>` in the file (~Lines 3–225)

PHB languages have setters for `standard`/`exotic`, `speakers`, and `script`. All MSV languages have NONE of these.

**PHB Pattern (Common):**
```xml
<element name="Common" type="Language" source="Player's Handbook" id="ID_LANGUAGE_COMMON">
  <supports>Standard</supports>
  <description>
    <p>Common is spoken by most inhabitants...</p>
  </description>
  <setters>
    <set name="standard">true</set>
    <set name="speakers">Humans</set>
    <set name="script">Common</set>
  </setters>
</element>
```

**MSV Pattern (Galactic Basic, ~L3):**
```xml
<element name="Galactic Basic" type="Language" source="SW-MSV-Edition" id="ID_LANGUAGE_GALACTIC_BASIC">
  <supports>Standard</supports>
  <description>
    <p>The standard language of the galaxy...</p>
  </description>
</element>
```

**Fix:** Add `<setters>` block to every language element with `standard`/`exotic`, `speakers`, and `script` values.

**Example fix for Galactic Basic:**
```xml
<element name="Galactic Basic" type="Language" source="SW-MSV-Edition" id="ID_LANGUAGE_GALACTIC_BASIC">
  <supports>Standard</supports>
  <description>
    <p>The standard language of the galaxy...</p>
  </description>
  <setters>
    <set name="standard">true</set>
    <set name="speakers">Most species</set>
    <set name="script">Aurebesh</set>
  </setters>
</element>
```

**Severity: HIGH** — Languages won't display properly in the compendium without these setters.

---

## 5. backgrounds.xml

### Issue 5a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 5b: ALL Backgrounds Missing `<setters>` with `short` Description (MEDIUM)
**Lines affected:** Every Background element

**PHB Pattern (Soldier background):**
```xml
<setters>
  <set name="short">You are a soldier who has served in a military organization.</set>
</setters>
```

**Fix:** Add `<setters>` block with `short` to each background:
```xml
<setters>
  <set name="short">Brief one-line summary of the background.</set>
</setters>
```

### Issue 5c: Missing Personality Trait/Ideal/Bond/Flaw `<select type="List">` Blocks (HIGH)
**Lines affected:** ALL backgrounds

The personality traits, ideals, bonds, and flaws are included in the HTML `<description>` as lists, but they are NOT provided as functional `<select type="List">` elements in `<rules>`. In the PHB, these are selectable dropdown lists on the character sheet.

**PHB Pattern (Soldier background):**
```xml
<rules>
  <!-- ... skill/tool grants ... -->
  <select name="Personality Trait" type="List" number="2">
    <item id="1" name="I'm always polite and respectful." />
    <item id="2" name="I'm haunted by memories of war..." />
    <!-- etc -->
  </select>
  <select name="Ideal" type="List">
    <item id="1" name="Greater Good. Our lot is to lay down our lives..." />
    <!-- etc -->
  </select>
  <select name="Bond" type="List">
    <item id="1" name="I would still lay down my life for the people I served with." />
    <!-- etc -->
  </select>
  <select name="Flaw" type="List">
    <item id="1" name="The monstrous enemy we faced in battle still leaves me quivering..." />
    <!-- etc -->
  </select>
</rules>
```

**MSV Current:** Traits are listed in HTML `<description>` only — not functional.

**Fix:** Add `<select type="List">` blocks for Personality Trait (number="2"), Ideal, Bond, and Flaw inside each background's `<rules>` block, pulling the items from the `<description>` lists.

**Severity: HIGH** — Personality traits, ideals, bonds, and flaws won't appear as selectable options.

### Issue 5d: Missing Background Feature Elements (MEDIUM)
**Lines affected:** ALL backgrounds

PHB backgrounds have a separate Background Feature element and a `<grant type="Background Feature">` rule. MSV backgrounds have no Background Feature elements at all.

**PHB Pattern:**
```xml
<!-- In the background element's rules: -->
<grant type="Background Feature" id="ID_WOTC_PHB_BACKGROUND_FEATURE_MILITARY_RANK" />

<!-- Separate element: -->
<element name="Military Rank" type="Background Feature" source="Player's Handbook" id="ID_WOTC_PHB_BACKGROUND_FEATURE_MILITARY_RANK">
  <supports>Background Feature</supports>
  <description>...</description>
  <sheet alt="Military Rank" />
</element>
```

**Fix:** Create a Background Feature element for each background and add a `<grant>` rule in the background to grant it.

**Severity: MEDIUM** — Background features won't show on character sheet but other background elements work.

### Issue 5e: Skill Proficiency `<select>` Using Pipe-Separated IDs (LOW)
**Lines affected:** All background `<rules>` blocks

The skill selects use `supports="ID_PROFICIENCY_SKILL_DECEPTION|ID_PROFICIENCY_SKILL_INVESTIGATION|..."` which is **valid Aurora Builder syntax** for ID-based OR matching. This works correctly but differs from the PHB's keyword approach (`supports="Skill,Soldier"`).

**Current (functional):**
```xml
<select type="Proficiency" name="Skill Proficiency (Agent)" number="2"
  supports="ID_PROFICIENCY_SKILL_DECEPTION|ID_PROFICIENCY_SKILL_INVESTIGATION|ID_PROFICIENCY_SKILL_STEALTH|ID_PROFICIENCY_SKILL_INSIGHT" />
```

**Severity: LOW** — Functionally correct, just a style difference.

---

## 6. weapons.xml

### Issue 6a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 6b: Weapons Have Non-Standard `<rules>` with `<stat>` Entries (HIGH)
**Lines affected:** Every weapon element's `<rules>` block

PHB weapons do NOT have `<rules>` blocks with stat entries. The ability score and weapon type are determined internally by Aurora Builder based on weapon properties and supports tags. MSV weapons incorrectly include these:

**MSV Pattern (blaster pistol, ~L126):**
```xml
<rules>
  <stat name="ability" value="dexterity" />
  <stat name="type" value="Simple Ranged" />
  <grant type="Action" id="ID_ACTION_SHOOT"/>
  <grant type="Action" id="ID_ACTION_QUICK_SHOT"/>
</rules>
```

**PHB Pattern (Longbow, items-weapons.xml):**
```xml
<!-- NO <rules> block at all on weapons -->
```

**What `<stat name="ability">` and `<stat name="type">` do:** These are NOT recognized Aurora Builder stat names for weapons. They will be silently ignored or could cause unexpected behavior. The weapon type and ability score are determined by the `<supports>` tag (which already identifies the weapon category).

**Fix:** Remove `<stat name="ability" value="dexterity" />` and `<stat name="type" value="..." />` from ALL weapon `<rules>` blocks. The `<grant type="Action">` lines can stay if those Action elements are properly defined.

Also remove `<stat name="prerequisite" value="Strength 11" />` from weapons like slugthrower pistol (~L290) — prerequisites on weapons aren't handled this way.

**Severity: HIGH** — Could cause parse warnings or unexpected behavior.

### Issue 6c: Custom `<set name="reload">` Setter (LOW)
**Lines affected:** Every weapon element's `<setters>` block

The `<set name="reload">16</set>` setter is not used in PHB weapons. Aurora Builder may or may not recognize it.

**Severity: LOW** — If not recognized, it will be silently ignored. The value is captured in description text anyway.

### Issue 6d: `Action` Elements at Top of File (LOW)  
**Lines ~3–100:** Contains elements like `Strike`, `Shoot`, `Quick Shot`, `Dart`, `Rocket`, `Whip`, `Flame` with `type="Action"`.

`type="Action"` is a valid Aurora Builder element type. These are granted by weapons via `<grant type="Action" id="..."/>`. This pattern works.

**Severity: LOW** — Non-standard but functional.

### Issue 6e: Custom Damage Types (MEDIUM)
Some weapons use custom damage types not native to D&D 5e: `energy`, `ion`, `sonic`, `kinetic`. These are used in `<set name="damage" type="energy">`.

**Fix:** These are intentionally custom for Star Wars — fine for homebrew. Just ensure they're consistent throughout.

**Severity: LOW** — Intentional homebrew customization.

---

## 7. items-armor.xml

### Issue 7a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 7b: Custom `ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_KINETIC` (MEDIUM)
**Lines ~198:** Heavy armor grants:
```xml
<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_KINETIC" />
```

This ID needs to be defined somewhere as a Condition element, or it will fail silently. Standard PHB only uses `ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_` for standard D&D damage types (fire, cold, lightning, etc.). "Kinetic" is custom.

**Fix:** Ensure `ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_KINETIC` is defined as an element somewhere in your files (it doesn't appear to be in any file read). If not defined, create it or remove the grant.

**Severity: MEDIUM** — Grant will fail silently if the condition element doesn't exist.

### Issue 7c: Shield Generators Missing `armorClass` on Some (LOW)
**Lines ~230-280:** Small/Medium/Large Shield Generators have no `<set name="armorClass">` — they don't add AC, only grant temporary HP via actions. This is fine if intentional but different from standard shields.

**Severity: LOW** — Intentional design choice.

### Issue 7d: Action Elements Defined Inline (LOW)
**Lines ~300-330:** Shield Generator Action elements are defined in this file. While functional, it would be cleaner to put all Action elements in a dedicated file or at least together.

**Severity: LOW** — Organizational preference, not functional issue.

---

## 8. items-tools.xml

### Issue 8a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 8b: Equipment Items Type (LOW)
**Lines ~300+:** Jumppack, Hoverpack, Jetpack items use `<set name="type">Equipment</set>` instead of `"Tool"`.

PHB tools use `<set name="type">Tool</set>`. Since these are equipment rather than tools, `Equipment` makes sense, but Aurora Builder may handle the `type` setter differently.

**Severity: LOW** — May affect how they appear in the equipment category.

---

## 9. items-instruments.xml

### Issue 9a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

**Status: ✅ OTHERWISE GOOD** — Format matches PHB pattern well. Instruments correctly use `<supports>ID_INTERNAL_TOOL_MUSICAL_INSTRUMENT</supports>`, proper setters for category, cost, weight, slot, type, and proficiency.

---

## 10. items-explosives.xml

### Issue 10a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 10b: Same Weapon `<rules>` Issues as weapons.xml (HIGH)
Explosives are typed as `type="Weapon"` and have the same non-standard `<stat name="ability">` and `<stat name="type">` rules as weapons.xml.

**Fix:** Same as weapons.xml Issue 6b — remove the invalid `<stat>` rules.

### Issue 10c: Consumable Nature Not Reflected (LOW)
Grenades, detonators, and mines are one-use consumables but are modeled as permanent weapons. There's no mechanism to consume/remove them after use. This is a design limitation rather than a formatting error.

**Severity: LOW** — Design choice, not format error.

---

## 11. items-healing.xml

### Issue 11a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 11b: Minimal Format (MEDIUM)
Healing items appear to be very minimal — missing `<set name="type">` setter and possibly other standard Item setters.

**PHB Pattern for items:**
```xml
<setters>
  <set name="category">...</set>
  <set name="cost" currency="gp">X</set>
  <set name="weight" lb="X">X lb.</set>
  <set name="type">Potion</set>
</setters>
```

**Fix:** Add complete `<setters>` blocks with category, cost, weight, and type.

**Severity: MEDIUM** — Items may not display correctly in equipment lists.

---

## 12. feats.xml

### Issue 12a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 12b: Feats Missing `<sheet>` Tags (MEDIUM)
**Lines affected:** ALL feat elements

Feats only have `<compendium display="true"/>` but no `<sheet>` tag. PHB feats have both.

**PHB Pattern:**
```xml
<element name="Alert" type="Feat" source="Player's Handbook" id="ID_WOTC_PHB_FEAT_ALERT">
  <description>
    <p>Always on the lookout for danger...</p>
  </description>
  <sheet>
    <description>You can't be surprised while conscious. +5 to initiative. Other creatures don't gain advantage on attack rolls against you as a result of being unseen by you.</description>
  </sheet>
</element>
```

**MSV Pattern (Tough, ~L209):**
```xml
<element name="Tough" type="Feat" source="SW-MSV-Edition" id="ID_SW_FEAT_TOUGH">
  <compendium display="true"/>
  <description>
    <p>Your hit point maximum increases by 2 for every level you have gained</p>
  </description>
  <rules>
    <stat name="hp" value="level*2" />
  </rules>
</element>
```

**Fix:** Add `<sheet><description>` to each feat with a concise summary for the character sheet.

**Severity: MEDIUM** — Feat descriptions won't appear on the character sheet.

### Issue 12c: Some Feats Missing `<requirements>` (LOW)
Feats with prerequisites (like ability score minimums) should have a `<requirements>` element. Check each feat against its source material for prerequisites.

**Severity: LOW** — Aurora Builder won't enforce prerequisites, allowing invalid selections.

---

## 13. proficiencies.xml

### Issue 13a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 13b: `<supports>` Tag Formatting/Indentation (LOW)
**Lines affected:** Most proficiency elements (~L200-653)

The `<supports>` tag is inconsistently indented and appears outside the expected nesting level:

**Current (odd formatting):**
```xml
<element name="Weapon: Blaster Rifle" type="Proficiency" id="..." source="SW-MSV-Edition">
  <description><p>Blaster Rifle proficiency</p></description>

    <supports>ID_INTERNAL_PROFICIENCY_WEAPON</supports>
</element>
```

**Should be:**
```xml
<element name="Weapon: Blaster Rifle" type="Proficiency" id="..." source="SW-MSV-Edition">
  <supports>ID_INTERNAL_PROFICIENCY_WEAPON</supports>
  <description><p>Blaster Rifle proficiency</p></description>
</element>
```

**Severity: LOW** — XML is still valid but looks inconsistent. The blank line before `<supports>` and extra indentation is cosmetic.

### Issue 13c: Slash Character in Element ID (MEDIUM)
**Line ~237:**
```xml
id="ID_MSV_PROFICIENCY_WEAPON_PROFICIENCY_MINIGUN/ROTARY_CANNON"
```

The `/` character in an element ID could cause issues with Aurora Builder's internal ID resolution or XML path lookups.

**Fix:** Replace with underscore:
```xml
id="ID_MSV_PROFICIENCY_WEAPON_PROFICIENCY_MINIGUN_ROTARY_CANNON"
```
And update any references to this ID elsewhere.

**Severity: MEDIUM** — May cause ID lookup failures.

### Issue 13d: Healing Items Labeled as "Weapon" Proficiencies (LOW)
**Lines ~500-540:** Proficiency elements for Kolto/Bacta Packs are named `"Weapon: Minor Kolto Pack"` etc. and have `<supports>ID_INTERNAL_PROFICIENCY_WEAPON</supports>`. These aren't weapons — they're healing items.

**Fix:** Consider renaming to `"Item: Minor Kolto Pack"` or creating a separate support category. However, if the healing items in items-healing.xml reference these proficiency IDs as weapon proficiencies, changing them would break those references.

**Severity: LOW** — Naming/categorization issue, not a functional break.

### Issue 13e: Category Proficiencies May Need `<supports>` (MEDIUM)
The top-level category proficiencies (Simple Blasters, Martial Blasters, Simple Vibroweapons, Martial Vibroweapons, Lightsaber, etc.) at the beginning of the file — verify they have proper `<supports>` tags. From the data read, some category proficiencies may be missing `<supports>ID_INTERNAL_PROFICIENCY_WEAPON</supports>`.

**Fix:** Ensure all category proficiencies have appropriate support tags.

**Severity: MEDIUM** — Could affect proficiency granting chains.

---

## 14. species.xml

### Issue 14a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 14b: ALL Race Elements Missing `<sheet display="false" />` (HIGH)
**Lines affected:** Every Race element

PHB races have `<sheet display="false" />` to prevent the race name from appearing as a separate feature on the character sheet.

**PHB Pattern (Human):**
```xml
<element name="Human" type="Race" source="Player's Handbook" id="ID_RACE_HUMAN">
  <!-- ... -->
  <sheet display="false" />
  <!-- ... -->
</element>
```

**Fix:** Add `<sheet display="false" />` to every Race element.

**Severity: HIGH** — Race name will appear as an extra feature entry on the character sheet.

### Issue 14c: ALL Race Elements Missing Name/Height/Weight Setters (MEDIUM)
**Lines affected:** Every Race element

PHB races have setters for randomized names and physical characteristics.

**PHB Pattern:**
```xml
<setters>
  <set name="names" type="male">Albert, Cedric, ...</set>
  <set name="names" type="female">Alice, Catherine, ...</set>
  <set name="names" type="surname">Ashdown, Blackwood, ...</set>
  <set name="names-format">{{name}} {{surname}}</set>
  <set name="height" modifier="2d10">4'8"</set>
  <set name="weight" modifier="2d4">110 lb.</set>
</setters>
```

**Fix:** Add `<setters>` blocks with name lists, height, and weight for each species. These feed the random name generator and physical description on the character sheet.

**Severity: MEDIUM** — Random name generator and physical characteristics won't work.

### Issue 14d: Non-Standard Resistance/Immunity/Vulnerability `<stat>` Rules (HIGH)
**Lines affected:** Multiple Race elements (Chagrian ~L250, Devaronian ~L380, Protocol Droid ~L440, etc.)

MSV uses `<stat name="resistant" value="poison"/>` which is NOT a valid Aurora Builder stat. PHB uses `<grant type="Condition">` instead.

**MSV Pattern (Chagrian, ~L252):**
```xml
<stat name="resistant" value="poison"/>
```

**PHB Pattern:**
```xml
<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_POISON" />
```

**Affected entries:**
- `<stat name="resistant" value="poison"/>` → `<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_POISON" />`
- `<stat name="resistant" value="necrotic"/>` → `<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_NECROTIC" />`
- `<stat name="resistant" value="psychic"/>` → `<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_RESISTANCE_PSYCHIC" />`
- `<stat name="immune" value="poison"/>` → `<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_IMMUNITY_POISON" />`
- `<stat name="vulnerable" value="ion"/>` → `<grant type="Condition" id="ID_INTERNAL_CONDITION_DAMAGE_VULNERABILITY_ION" />` (custom, needs defining)

**Fix:** Replace all `<stat name="resistant/immune/vulnerable">` entries with proper `<grant type="Condition">` entries.

**Severity: HIGH** — Resistances/immunities/vulnerabilities won't actually be applied to the character.

### Issue 14e: Racial Trait Elements Used Without Defining Them (MEDIUM)
Several races grant Racial Traits like:
```xml
<grant type="Racial Trait" id="ID_RACE_TRAIT_CHAGRIAN_POISON_RESILIENCE"/>
```

These Racial Trait elements need to be defined somewhere. Verify each granted trait ID has a corresponding element definition.

**Fix:** Create any missing Racial Trait elements, or remove grants for undefined traits.

**Severity: MEDIUM** — Grants to undefined elements fail silently.

### Issue 14f: Inconsistent Indentation (LOW)
**Lines affected:** Throughout species.xml

Some lines have extra leading spaces creating misaligned XML:
```xml
      <stat name="innate speed:swim" value="30" bonus="base"/>
      <grant type="Racial Trait" id="ID_RACE_TRAIT_CHAGRIAN_POISON_RESILIENCE"/>
<select type="Sub Race" name="Chagrian Subrace" supports="ID_RACE_CHAGRIAN" optional="true"/>
```

The `<select>` line should be indented to match siblings.

**Severity: LOW** — Cosmetic, XML is still valid.

---

## 15. fighting-styles.xml

### Issue 15a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

**Status: ✅ OTHERWISE GOOD** — Fighting styles properly use `<supports>Fighting Style</supports>`, have good `<sheet>` descriptions, and match PHB format.

---

## 16. maneuvers.xml

### Issue 16a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 16b: ALL Maneuvers Missing `<sheet>` Tags (MEDIUM)
**Lines affected:** All 21 maneuver elements

Maneuvers ONLY have `<description>` — no `<sheet>` tag at all. This means they won't display on the character sheet.

**PHB equivalent pattern:**
```xml
<element name="Commander's Strike" type="Class Feature" ...>
  <supports>Maneuver, Battle Master</supports>
  <description>
    <p>When you take the Attack action on your turn...</p>
  </description>
  <sheet>
    <description>When you take the Attack action on your turn, you can forgo one attack and direct an ally to strike with a reaction. Add the superiority die to the ally's damage roll.</description>
  </sheet>
</element>
```

**Fix:** Add `<sheet><description>` to every maneuver with a concise summary.

**Severity: MEDIUM** — Maneuver descriptions won't show on the character sheet.

---

## 17. class-knight.xml

### Issue 17a: Missing `<info>` block (CRITICAL)
See [Systematic Issue 1a](#1a-missing-info-blocks-critical).

### Issue 17b: Class Element Missing `<sheet display="false">` (HIGH)
**Line ~3:** The Knight class element has no `<sheet>` tag.

**PHB Pattern (Fighter):**
```xml
<element name="Fighter" type="Class" ...>
  <sheet display="false">
    <description>A master of martial combat, skilled with a variety of weapons and armor.</description>
  </sheet>
  <!-- ... -->
</element>
```

**Fix:** Add `<sheet display="false">` with a short description to the Knight class element.

### Issue 17c: Class Element Missing `<setters>` (HIGH)
**Line ~3:** The Knight class element is missing standard class setters.

**PHB Pattern:**
```xml
<setters>
  <set name="short">A holy warrior bound to a sacred oath.</set>
  <set name="hd">d10</set>
</setters>
```

**Fix:** Add `<setters>` with `short` and `hd` to the Knight class element.

### Issue 17d: No Class Features Table in Description (MEDIUM)
The Knight class `<description>` should include a class features table showing what features are gained at each level.

**PHB Pattern:**
```xml
<description>
  <p>...</p>
  <h5 class="caption">THE FIGHTER</h5>
  <table class="class-features">
    <thead>
      <tr><td>Level</td><td>Proficiency Bonus</td><td>Features</td></tr>
    </thead>
    <tr><td>1st</td><td>+2</td><td>Fighting Style, Second Wind</td></tr>
    <!-- ... -->
  </table>
  <div element="ID_WOTC_PHB_CLASS_FEATURE_FIGHTINGSTYLE_FIGHTER" />
  <!-- ... -->
</description>
```

**Fix:** Add a `<table class="class-features">` and `<div element="ID_..."/>` references for each class feature to the class description.

### Issue 17e: No `<multiclass>` Block (LOW)
PHB classes have a `<multiclass>` block defining multiclassing prerequisites and grants. If multiclassing is intended for the Knight, this should be added.

**Severity: LOW** — Only matters if multiclassing is supported in your game.

### Issue 17f: Archetypes (Lightsaber Forms) Missing `<sheet display="false" />` (MEDIUM)
**Lines ~460-726:** All Lightsaber Form Archetype elements lack `<sheet display="false" />`.

**PHB Pattern (Champion):**
```xml
<element name="Champion" type="Archetype" ...>
  <sheet display="false">
    <description>The archetypal Champion focuses on raw physical power.</description>
  </sheet>
</element>
```

**Fix:** Add `<sheet display="false">` to each Archetype element.

### Issue 17g: ASI/Feat Feature Directly Selects Feats (LOW)
The Feat class feature uses `<select type="Feat">` directly. PHB uses an intermediate Ability Score Improvement element that offers both ASI and optional feat selection. This is a design choice for your system (no ASI, just feats), so it's fine if intentional.

**Severity: LOW** — Intentional design choice.

---

## 18. class-warrior.xml

### Issue 18a–18e: Same Class-Level Issues as Knight
- Missing `<info>` block (CRITICAL)
- Missing `<sheet display="false">` on class (HIGH)
- Missing `<setters>` with `short` and `hd` (HIGH)
- No class features table (MEDIUM)
- No `<multiclass>` block (LOW)

### Issue 18f: Stub Class Features with No Content (MEDIUM)
**Lines ~200-215:** Elements like `ID_CLASS_WARRIOR_FEATURE_JETTROOPER` and `ID_CLASS_WARRIOR_FEATURE_BRUTE` have placeholder descriptions:
```xml
<element id="ID_CLASS_WARRIOR_FEATURE_JETTROOPER" name="Jettrooper" type="Class Feature" source="SW-MSV-Edition">
  <description>
    <p>Jettrooper - See Warrior class description for details.</p>
  </description>
</element>
```

These have no `<sheet>`, `<rules>`, or meaningful content. If they're supposed to just point users to the subclass, they should at least have `<sheet display="false" />`.

**Fix:** Either flesh out with proper descriptions and `<sheet>` tags, or add `<sheet display="false" />` to suppress them from the character sheet.

### Issue 18g: Archetypes Missing `<sheet display="false" />` (MEDIUM)
**Lines ~250+:** Battle Master, Brute, and Jettrooper Archetype elements lack `<sheet display="false" />`.

Same fix as Knight Issue 17f.

### Issue 18h: Weapon Modification Improvements Not Mechanically Linked (MEDIUM)
**Line ~425:** The "Improved Weapons Modification" feature at level 18 says "Each weapon modification you own turns into the improved version" but has no `<rules>` to actually swap base modifications for improved versions.

The improved modifications (`<supports>Improved Weapon Modification</supports>`) exist as elements but are never granted or selectable.

**Fix:** Either:
1. Add rules that grant the improved versions when the level 18 feature is gained
2. Or create a mechanism to swap base mods for improved mods

**Severity: MEDIUM** — Level 18 feature is non-functional.

---

## 19. class-scout.xml

### Issue 19a–19e: Same Class-Level Issues as Knight/Warrior
- Missing `<info>` block (CRITICAL)
- Missing `<sheet display="false">` on class (HIGH)
- Missing `<setters>` with `short` and `hd` (HIGH)
- No class features table (MEDIUM)
- No `<multiclass>` block (LOW)

### Issue 19f: Archetypes Missing `<sheet display="false" />` (MEDIUM)
Thief, Assassin, and Operative Archetype elements lack `<sheet display="false" />`.

---

## 20. class-marauder.xml

### Issue 20a–20e: Same Class-Level Issues as Knight/Warrior
- Missing `<info>` block (CRITICAL)
- Missing `<sheet display="false">` on class (HIGH)
- Missing `<setters>` with `short` and `hd` (HIGH)
- No class features table (MEDIUM)
- No `<multiclass>` block (LOW)

### Issue 20f: Archetypes (Lightsaber Forms) Missing `<sheet display="false" />` (MEDIUM)
All Marauder Lightsaber Form Archetype elements lack `<sheet display="false" />`.

### Issue 20g: Duplicate Lightsaber Forms (Intentional) (NONE)
The Marauder has the same Lightsaber Forms as the Knight but with different IDs and different resource costs (Rage vs Focus). This duplication is **correct** — each class needs its own version.

---

## 21. class-inquisitor.xml

### Issue 21a–21e: Same Class-Level Issues as Knight/Warrior
- Missing `<info>` block (CRITICAL)
- Missing `<sheet display="false">` on class (HIGH)
- Missing `<setters>` with `short` and `hd` (HIGH)
- No class features table (MEDIUM)
- No `<multiclass>` block (LOW)

### Issue 21f: Archetype Grants Use `<grant type="Spell">` Instead of `<grant type="Archetype Feature">` (MEDIUM)
**Lines ~230-380:** Shadow, Trickster, and Manipulator archetypes grant their abilities using `<grant type="Spell">`:
```xml
<rules>
  <grant type="Spell" id="ID_SUBCLASS_SHADOW_ABILITY_FORCE_BLIND" level="3" />
</rules>
```

**PHB Pattern (Champion):**
```xml
<rules>
  <grant type="Archetype Feature" id="ID_WOTC_PHB_ARCHETYPE_FEATURE_IMPROVEDCRITICAL" level="3" />
</rules>
```

This works because the abilities ARE defined as type="Spell", but it means the archetype itself doesn't grant "Archetype Feature" types — it grants Spells directly. As long as the Spell elements exist and have `<supports>Inquisitor</supports>`, this is functional.

**Severity: MEDIUM** — Functional but non-standard. Could cause issues if Aurora Builder expects Archetype grants to be Archetype Feature type.

### Issue 21g: Compressed Whitespace in Setters (LOW)
**Lines ~250-400:** Some Spell setters are compressed onto single lines:
```xml
<setters>      <set name="keywords">force</set>      <set name="level">0</set>
```

**Fix:** Format each setter on its own line for readability.

**Severity: LOW** — Cosmetic, XML is still valid.

---

## 22. Summary of Severity Levels

### CRITICAL (Must Fix — Will Break Functionality)
| Issue | Files | Description |
|-------|-------|-------------|
| 1a | 18 files | Missing `<info>` blocks |

### HIGH (Should Fix — Features Won't Work Correctly)
| Issue | Files | Description |
|-------|-------|-------------|
| 4b | languages.xml | All languages missing `<setters>` |
| 5c | backgrounds.xml | Missing personality/ideal/bond/flaw selects |
| 6b | weapons.xml, items-explosives.xml | Non-standard `<stat>` rules on weapons |
| 14b | species.xml | All races missing `<sheet display="false" />` |
| 14d | species.xml | Non-standard resistance/immunity `<stat>` rules |
| 17b,18a,19a,20a,21a | All class files | Class missing `<sheet display="false">` |
| 17c,18a,19a,20a,21a | All class files | Class missing `short`/`hd` setters |

### MEDIUM (Should Fix — Quality/Display Issues)
| Issue | Files | Description |
|-------|-------|-------------|
| 5b | backgrounds.xml | Missing `short` setter |
| 5d | backgrounds.xml | Missing Background Feature elements |
| 7b | items-armor.xml | Custom condition ID may not exist |
| 11b | items-healing.xml | Minimal item format |
| 12b | feats.xml | Missing `<sheet>` tags |
| 14c | species.xml | Missing name/height/weight setters |
| 14e | species.xml | Racial Trait elements may be undefined |
| 16b | maneuvers.xml | Missing `<sheet>` tags |
| 17d+ | All class files | No class features tables |
| 17f+ | All class files | Archetypes missing `<sheet display="false" />` |
| 18f | class-warrior.xml | Stub features with no content |
| 18h | class-warrior.xml | Improved Weapon Mods not mechanically linked |
| 13c | proficiencies.xml | Slash in element ID |
| 13e | proficiencies.xml | Category proficiencies may need `<supports>` |
| 21f | class-inquisitor.xml | Archetypes grant Spell type instead of Archetype Feature |

### LOW (Optional — Cosmetic/Style Differences)
| Issue | Files | Description |
|-------|-------|-------------|
| 1b | All class files | Verbose `<sheet>` descriptions |
| 5e | backgrounds.xml | Pipe-separated skill support IDs (valid) |
| 6c | weapons.xml | Custom `reload` setter |
| 6d | weapons.xml | Action elements in weapon file |
| 6e | weapons.xml | Custom damage types |
| 7c | items-armor.xml | Shield generators without armorClass |
| 8b | items-tools.xml | Equipment type instead of Tool |
| 12c | feats.xml | Some feats missing `<requirements>` |
| 13b | proficiencies.xml | Inconsistent indentation |
| 13d | proficiencies.xml | Healing items labeled as weapons |
| 14f | species.xml | Inconsistent indentation |
| 17e+ | All class files | No `<multiclass>` blocks |
| 17g | class-knight.xml | Direct feat select (intentional) |
| 21g | class-inquisitor.xml | Compressed whitespace |

---

## Recommended Fix Priority

1. **Add `<info>` blocks to all 18 files** — Quick win, highest impact
2. **Fix species.xml resistance/immunity stats** — Breaks core racial features
3. **Remove non-standard `<stat>` rules from weapons** — Prevent parse issues
4. **Add `<sheet display="false" />` to all classes and races** — Fix character sheet clutter
5. **Add `<setters>` to all classes (`short`, `hd`)** — Fix class display
6. **Add `<setters>` to all languages** — Fix language display
7. **Add `<sheet>` tags to feats and maneuvers** — Fix character sheet display
8. **Add `<sheet display="false" />` to all archetypes** — Fix character sheet clutter
9. **Add personality/ideal/bond/flaw selects to backgrounds** — Enable trait selection
10. **Add class features tables to class descriptions** — Complete class documentation

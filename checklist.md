# SW-MSV-Edition Functionality Checklist

This checklist verifies that each XML file in the SW-MSV-Edition project functions correctly in Aurora Builder according to the specifications in the SOURCE/ text files. Each section checks if the XML implementation matches the source and if the elements work as intended.

## Species (species.xml vs SOURCE/Species.txt)

- [ ] All 24 species from source are implemented (Bith, Bothan, Cathar, Chagrian, Chiss, Devaronian, Protocol Droid, Combat Droid, Duros, Ewok, Gamorrean, Geonosian, Gran, Human, Ithorian, Jawa, Kaleesh, Kel Dor, Mirialan, Mon Calamari, Nautolan, Neimoidian, Ortolan, Rakata)
- [ ] Ability score increases apply correctly (+2/+1 or +1 x4 for humans)
- [ ] Racial proficiencies are granted (e.g., stealth for Cathar, insight for Bothan)
- [x] Special abilities function (e.g., Ithorian breath weapon, droid Tune-Up) - Now implemented as actions
- [ ] Size, speed, age, and languages are correctly set
- [ ] Vulnerabilities and resistances are applied (e.g., sonic for Bith, ion for droids)
- [ ] Human standard/variant selections work properly
- [ ] Cyborg subraces grant correct cybernetic enhancements
- [ ] All IDs are unique and follow format ID_RACE_[NAME]
- [ ] Display settings allow traits to be visible and functional on character sheet

## Classes

### Warrior (class-warrior.xml vs SOURCE/Warrior Class.txt)

- [ ] All class features implemented (Fighting Style, Second Wind, Action Surge, etc.)
- [ ] Subclass selections work (Champion, Battle Master, etc.)
- [ ] Hit dice, proficiencies, and equipment correct
- [ ] Ability score improvements at correct levels
- [ ] Maneuvers for Battle Master subclass function
- [ ] IDs follow format ID_CLASS_WARRIOR_[FEATURE]

### Scout (class-scout.xml vs SOURCE/Scout Class.txt)

- [ ] Ranger-like features implemented (Favored Enemy, Natural Explorer, etc.)
- [ ] Subclass selections work
- [ ] Spellcasting if applicable
- [ ] Proficiencies and equipment correct

### Marauder (class-marauder.xml vs SOURCE/Marauder Class.txt)

- [ ] Barbarian-like features (Rage, Unarmored Defense, etc.)
- [ ] Subclass selections
- [x] Spell save DC and ability modifier displayed (spellcasting present)
- [ ] Rage damage increases correctly

### Knight (class-knight.xml vs SOURCE/Knight Class.txt)

- [ ] Paladin-like features (Divine Sense, Lay on Hands, etc.)
- [ ] Subclass selections
- [x] Spellcasting and auras work (spellcasting stat present)
- [ ] Oath features implemented

### Inquisitor (class-inquisitor.xml vs SOURCE/Inquisitor Class.txt)

- [ ] Unique features implemented
- [x] Spellcasting works (spellcasting stat present)
- [ ] Force-related abilities function

## Backgrounds (backgrounds.xml vs SOURCE/Background.txt)

- [x] All backgrounds implemented
- [x] Proficiencies granted correctly
- [x] Equipment and features work
- [x] IDs follow format ID_BACKGROUND_[NAME]

## Feats (feats.xml vs SOURCE/Feats.txt)

- [x] All feats implemented
- [ ] Prerequisites enforced
- [ ] Effects apply correctly (most are descriptive, not automatic)
- [x] IDs follow format ID_FEAT_[NAME]

## Fighting Styles (fighting-styles.xml vs SOURCE/Fighting Styles.txt)

- [ ] All fighting styles implemented
- [x] Effects work (e.g., Dueling +2 damage is not automatically applied - requires manual tracking, Marksmanship +attack works)
- [ ] Prerequisites if any
- [ ] IDs follow format ID_FIGHTING_STYLE_[NAME]

## Items

### Weapons (weapons.xml vs SOURCE/Weapons and Items.txt)

- [ ] All weapons implemented
- [ ] Damage, range, properties correct
- [ ] Actions listed in descriptions
- [ ] Modifiers applied correctly
- [ ] Weapon types displayed
- [ ] Special abilities work (e.g., Wrist Launcher attachments)
- [ ] IDs follow format ID_WEAPON_[NAME]

### Armor (items-armor.xml vs SOURCE/Weapons and Items.txt)

- [ ] All armor types implemented
- [ ] AC calculations correct
- [ ] Properties (stealth disadvantage, etc.)
- [ ] Shield generators give temporary HP
- [ ] IDs follow format ID_ARMOR_[NAME]

### Healing Items (items-healing.xml vs SOURCE/Weapons and Items.txt)

- [ ] Healing amounts correct
- [ ] Usage restrictions
- [ ] IDs follow format ID_ITEM_HEALING_[NAME]

### Explosives (items-explosives.xml vs SOURCE/Weapons and Items.txt)

- [ ] Damage and effects correct
- [ ] IDs follow format ID_ITEM_EXPLOSIVE_[NAME]

### Tools (items-tools.xml vs SOURCE/Weapons and Items.txt)

- [ ] Tool proficiencies granted
- [ ] IDs follow format ID_ITEM_TOOL_[NAME]

### Instruments (items-instruments.xml vs SOURCE/Weapons and Items.txt)

- [ ] Musical instrument proficiencies
- [ ] IDs follow format ID_ITEM_INSTRUMENT_[NAME]

## Languages (languages.xml vs SOURCE/Languages.txt)

- [x] All languages implemented
- [x] IDs follow format ID_LANGUAGE_[NAME]

## Maneuvers (maneuvers.xml vs SOURCE/Maneuvers.txt)

- [x] All maneuvers implemented
- [ ] Effects work correctly
- [ ] Prerequisites if any
- [x] IDs follow format ID_MANEUVER_[NAME]

## Proficiencies (proficiencies.xml)

- [ ] All proficiency types implemented
- [ ] IDs follow format ID_PROFICIENCY_[TYPE]_[NAME]

## Source (source.xml)

- [ ] Contains necessary metadata for the edition
- [ ] IDs correct

## General Functionality Checks

- [ ] All XML files load without errors in Aurora Builder
- [x] No broken ID references (verified by validate_content.py)
- [ ] Character creation works for all combinations
- [ ] Stat calculations are correct
- [ ] Proficiencies appear on character sheet
- [ ] Special abilities are usable
- [ ] Multiclassing works if applicable
- [ ] Level progression is correct
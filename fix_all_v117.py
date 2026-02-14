#!/usr/bin/env python3
"""
Comprehensive fix script for SW-MSV-Edition v1.1.7
Handles all species, feats, items, class, and formatting fixes.
"""
import xml.etree.ElementTree as ET
import re
import os

os.chdir(r'C:\Users\james\OneDrive\Docs and windows stuff\documenten\GitHub\SW-MSV-EDITION')

changes_log = []

def log(msg):
    changes_log.append(msg)
    print(msg)

# Abbreviation map used across all files
abbreviation_map = {
    'Your STR score': 'Your Strength score',
    'Your DEX score': 'Your Dexterity score',
    'Your CON score': 'Your Constitution score',
    'Your WIS score': 'Your Wisdom score',
    'Your INT score': 'Your Intelligence score',
    'Your CHAR score': 'Your Charisma score',
    'Your CHA score': 'Your Charisma score',
    'STR or CHAR score': 'Strength or Charisma score',
    'STR or DEX score': 'Strength or Dexterity score',
    'DEX or INT score': 'Dexterity or Intelligence score',
    'INT or WIS score': 'Intelligence or Wisdom score',
    'WIS or CHAR score': 'Wisdom or Charisma score',
    ', DEX score increases': ', Dexterity score increases',
    ', CHA score increases': ', Charisma score increases',
    ', CHAR score increases': ', Charisma score increases',
    ', CON score increases': ', Constitution score increases',
    ', WIS score increases': ', Wisdom score increases',
    ', INT score increases': ', Intelligence score increases',
    ', STR score increases': ', Strength score increases',
    'DEX modifier': 'Dexterity modifier',
    'STR modifier': 'Strength modifier',
    'CON modifier': 'Constitution modifier',
    'WIS modifier': 'Wisdom modifier',
    'INT modifier': 'Intelligence modifier',
    'CHA modifier': 'Charisma modifier',
    'CHAR modifier': 'Charisma modifier',
    '+ DEX mod': '+ Dexterity modifier',
    '+ CON mod': '+ Constitution modifier',
    'DEX +1': 'Dexterity +1',
    'DEX +2': 'Dexterity +2',
    'STR +1': 'Strength +1',
    'STR +2': 'Strength +2',
    'CON +1': 'Constitution +1',
    'CON +2': 'Constitution +2',
    'WIS +1': 'Wisdom +1',
    'WIS +2': 'Wisdom +2',
    'INT +1': 'Intelligence +1',
    'INT +2': 'Intelligence +2',
    'CHA +1': 'Charisma +1',
    'CHA +2': 'Charisma +2',
    'CHAR +1': 'Charisma +1',
    'CHAR +2': 'Charisma +2',
    'DEX save': 'Dexterity save',
    'STR save': 'Strength save',
    'CON save': 'Constitution save',
    'WIS save': 'Wisdom save',
    'INT save': 'Intelligence save',
    'CHA save': 'Charisma save',
    'CHAR save': 'Charisma save',
    '12 + DEX': '12 + Dexterity',
    '13 + DEX': '13 + Dexterity',
    'AC = 12 + DEX': 'AC = 12 + Dexterity',
    'AC = 13 + DEX': 'AC = 13 + Dexterity',
}

def fix_abbreviations(root):
    """Fix ability score abbreviations in all text nodes of a tree."""
    count = 0
    for elem in root.iter():
        if elem.text:
            original = elem.text
            for old, new in abbreviation_map.items():
                elem.text = elem.text.replace(old, new)
            if elem.text != original:
                count += 1
        if elem.tail:
            original = elem.tail
            for old, new in abbreviation_map.items():
                elem.tail = elem.tail.replace(old, new)
            if elem.tail != original:
                count += 1
    return count

# ============================================================
# PART 1: SPECIES FIXES (species.xml)
# ============================================================
log("=== PART 1: SPECIES FIXES ===")

tree = ET.parse('species.xml')
root = tree.getroot()

# --- 1a. Fix Bothan, Rattataki, Sullustan size to Medium (not Small) ---
for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    if eid in ('ID_RACE_BOTHAN', 'ID_RACE_RATTATAKI', 'ID_RACE_SULLUSTAN'):
        rules = elem.find('rules')
        if rules is not None:
            for grant in rules.findall('grant'):
                if grant.get('id') == 'ID_SIZE_SMALL':
                    grant.set('id', 'ID_SIZE_MEDIUM')
                    log(f"  Fixed {eid}: Size Small -> Medium")

# --- 1b. Fix vibro-axe proficiency typo (VIRBO -> VIBRO, hyphen -> underscore) ---
for elem in root.iter():
    if elem.tag == 'grant':
        gid = elem.get('id', '')
        if 'VIRBO-AXE' in gid or 'VIRBO_AXE' in gid:
            elem.set('id', 'ID_MSV_PROFICIENCY_WEAPON_PROFICIENCY_VIBRO_AXE')
            log(f"  Fixed vibro-axe proficiency typo in grant")

# --- 1c. Add Mando'a language to Protocol Droid ---
for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_RACE_PROTOCOL_DROID':
        rules = elem.find('rules')
        has_mandoa = any(g.get('id') == 'ID_LANGUAGE_MANDOA_LANGUAGE' for g in rules.findall('grant'))
        if not has_mandoa:
            lang_grant = ET.SubElement(rules, 'grant')
            lang_grant.set('type', 'Language')
            lang_grant.set('id', 'ID_LANGUAGE_MANDOA_LANGUAGE')
            log("  Added Mando'a language to Protocol Droid")

# --- 1d. Add natural armor AC rules to all natural armor traits ---
natural_armor_traits = {
    'ID_RACE_TRAIT_GEONOSIAN_NATURAL_ARMOR': 12,
    'ID_RACE_TRAIT_NAUTOLAN_NATURAL_ARMOR': 12,
    'ID_RACE_TRAIT_TALZ_NATURAL_ARMOR': 12,
    'ID_RACE_TRAIT_TRANDOSHAN_NATURAL_ARMOR': 12,
    'ID_RACE_TRAIT_WEEQUAY_NATURAL_ARMOR': 13,
    'ID_RACE_TRAIT_WOOKIE_NATURAL_ARMOR': 13,
}

for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    if eid in natural_armor_traits:
        ac_value = natural_armor_traits[eid]
        rules = elem.find('rules')
        if rules is None:
            rules = ET.SubElement(elem, 'rules')
        # Check if stat already exists
        has_ac = any(s.get('name') == 'ac:unarmored:base' for s in rules.findall('stat'))
        if not has_ac:
            stat = ET.SubElement(rules, 'stat')
            stat.set('name', 'ac:unarmored:base')
            stat.set('value', str(ac_value))
            stat.set('bonus', 'base')
            log(f"  Added natural armor AC={ac_value} rules to {eid}")

# --- 1e. Add HP per level display traits for Gamorrean and Gran ---
for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    
    if eid == 'ID_RACE_GAMORREAN':
        rules = elem.find('rules')
        # Remove inline hp stat
        for stat in list(rules.findall('stat')):
            if stat.get('name') == 'hp' and stat.get('value') == 'level':
                rules.remove(stat)
                log("  Removed inline HP stat from Gamorrean")
        # Add trait grant
        if not any(g.get('id') == 'ID_RACE_TRAIT_GAMORREAN_DURABLE' for g in rules.findall('grant')):
            trait = ET.SubElement(rules, 'grant')
            trait.set('type', 'Racial Trait')
            trait.set('id', 'ID_RACE_TRAIT_GAMORREAN_DURABLE')
            log("  Added Durable trait grant to Gamorrean")
    
    elif eid == 'ID_RACE_GRAN':
        rules = elem.find('rules')
        for stat in list(rules.findall('stat')):
            if stat.get('name') == 'hp' and stat.get('value') == 'level':
                rules.remove(stat)
                log("  Removed inline HP stat from Gran")
        if not any(g.get('id') == 'ID_RACE_TRAIT_GRAN_DURABLE' for g in rules.findall('grant')):
            trait = ET.SubElement(rules, 'grant')
            trait.set('type', 'Racial Trait')
            trait.set('id', 'ID_RACE_TRAIT_GRAN_DURABLE')
            log("  Added Durable trait grant to Gran")

# Create Gamorrean and Gran Durable trait elements
for species_name, trait_id in [('Gamorrean', 'ID_RACE_TRAIT_GAMORREAN_DURABLE'), ('Gran', 'ID_RACE_TRAIT_GRAN_DURABLE')]:
    if not any(e.get('id') == trait_id for e in root.findall('.//element')):
        durable = ET.SubElement(root, 'element')
        durable.set('name', 'Durable')
        durable.set('type', 'Racial Trait')
        durable.set('source', 'SW-MSV-Edition')
        durable.set('id', trait_id)
        desc = ET.SubElement(durable, 'description')
        p = ET.SubElement(desc, 'p')
        p.text = 'Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.'
        sheet = ET.SubElement(durable, 'sheet')
        sd = ET.SubElement(sheet, 'description')
        sd.text = '+1 HP per level.'
        rules = ET.SubElement(durable, 'rules')
        stat = ET.SubElement(rules, 'stat')
        stat.set('name', 'hp')
        stat.set('value', 'level')
        log(f"  Created {trait_id} trait element")

# --- 1f. Update Rakata Consume Corpse ---
for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_RACE_TRAIT_RAKATA_CONSUME_CORPSE':
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = 'As an Action, eat a corpse to gain temporary Hit Points equal to your hit die + Constitution modifier.'
        sheet = elem.find('sheet')
        if sheet is not None:
            for d in list(sheet.findall('description')):
                sheet.remove(d)
            sd = ET.SubElement(sheet, 'description')
            sd.text = 'Action: Eat a corpse to gain temp HP = hit die + Constitution modifier.'
        log("  Updated Rakata Consume Corpse ability")

# --- 1g. Update Small Build to include energy shields ---
for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_RACE_TRAIT_SMALL_BUILD':
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = 'You can only wield two-handed weapons if they have the versatile property. You cannot use physical or energy shields.'
        sheet = elem.find('sheet')
        if sheet is not None:
            for d in list(sheet.findall('description')):
                sheet.remove(d)
            sd = ET.SubElement(sheet, 'description')
            sd.text = 'Can only wield two-handed weapons if versatile. Cannot use physical or energy shields.'
        log("  Updated Small Build to include energy shields")

# --- 1h. Rename Ithorian Breath to Sonic Scream ---
for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_ACTION_ITHORIAN_BREATH':
        elem.set('name', 'Sonic Scream')
        log("  Renamed Ithorian Breath -> Sonic Scream")

# --- 1i. Fix abbreviations in species.xml ---
abbrev_count = fix_abbreviations(root)
log(f"  Fixed {abbrev_count} abbreviation instances in species.xml")

# Save species.xml
tree.write('species.xml', encoding='utf-8', xml_declaration=True)
log("  Saved species.xml")

# ============================================================
# PART 2: FEATS FIXES (feats.xml)
# ============================================================
log("\n=== PART 2: FEATS FIXES ===")

tree = ET.parse('feats.xml')
root = tree.getroot()

for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    
    # --- 2a. Actor: reword + expertise ---
    if eid == 'ID_SW_FEAT_ACTOR':
        new_desc = 'Your Charisma increases by 1 to a max of 20. You gain proficiency in Performance and Deception. If you already have proficiency, gain expertise instead.'
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = new_desc
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Updated Actor feat description")
    
    # --- 2b. Athlete: restrict to STR or DEX ---
    elif eid == 'ID_SW_FEAT_ATHLETE':
        rules = elem.find('rules')
        for sel in list(rules.findall('select')):
            if sel.get('type') == 'Ability Score Improvement':
                rules.remove(sel)
        sel = ET.SubElement(rules, 'select')
        sel.set('type', 'Racial Trait')
        sel.set('name', 'Ability Score Increase (Athlete)')
        sel.set('supports', 'Athlete ASI')
        sel.set('number', '1')
        log("  Fixed Athlete feat to STR/DEX only")
    
    # --- 2c. Blaster Pistol Expert -> Blaster Expert ---
    elif eid == 'ID_SW_FEAT_BLASTER_PISTOL_EXPERT':
        elem.set('name', 'Blaster Expert')
        new_desc = 'When you make a ranged attack within melee range, the attack roll does not have disadvantage.'
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = new_desc
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Renamed Blaster Pistol Expert -> Blaster Expert")
    
    # --- 2d. Dual Wielder: update description ---
    elif eid == 'ID_SW_FEAT_DUAL_WIELDER':
        new_desc = 'When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack and you gain a +1 bonus to Armour Class while wielding a melee weapon in each hand. You cannot dual-wield two-handed weapons.'
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = new_desc
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Updated Dual Wielder feat description")
    
    # --- 2e. Lightly Armoured: fix spelling, restrict to STR/DEX ---
    elif eid == 'ID_SW_FEAT_LIGHTELY_ARMOURED':
        elem.set('name', 'Lightly Armoured')
        rules = elem.find('rules')
        for sel in list(rules.findall('select')):
            if sel.get('type') == 'Ability Score Improvement':
                rules.remove(sel)
        sel = ET.SubElement(rules, 'select')
        sel.set('type', 'Racial Trait')
        sel.set('name', 'Ability Score Increase (Lightly Armoured)')
        sel.set('supports', 'Lightly Armoured ASI')
        sel.set('number', '1')
        log("  Fixed Lightly Armoured spelling and restricted to STR/DEX")
    
    # --- 2f. Medium Armour Master: fix name spelling ---
    elif eid == 'ID_SW_FEAT_MEDIUM_ARMOR_MASTER':
        elem.set('name', 'Medium Armour Master')
        log("  Fixed Medium Armor -> Armour spelling")
    
    # --- 2g. Moderately Armoured: restrict to STR/DEX ---
    elif eid == 'ID_SW_FEAT_MODERATELY_ARMOURED':
        rules = elem.find('rules')
        for sel in list(rules.findall('select')):
            if sel.get('type') == 'Ability Score Improvement':
                rules.remove(sel)
        sel = ET.SubElement(rules, 'select')
        sel.set('type', 'Racial Trait')
        sel.set('name', 'Ability Score Increase (Moderately Armoured)')
        sel.set('supports', 'Moderately Armoured ASI')
        sel.set('number', '1')
        log("  Fixed Moderately Armoured to STR/DEX only")
    
    # --- 2h. Polearm Master: fix corrupted sheet description ---
    elif eid == 'ID_SW_FEAT_POLEARM_MASTER':
        new_desc = 'When attacking with a lightstaff, lightsaber pike, vibrostaff, vibrospear, electrostaff, vibropike you can make an Opportunity Attack when a target comes within range.'
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Fixed Polearm Master corrupted sheet description")
    
    # --- 2i. Sentinel: fix truncated description ---
    elif eid == 'ID_SW_FEAT_SENTINEL':
        new_desc = "When an enemy within melee range attacks an ally, you can use a reaction to make a weapon attack against that enemy. Target ally must not have the Sentinel Feat. You gain Advantage on Opportunity Attacks, and when you hit a creature with an Opportunity Attack, it can no longer move for the rest of its turn."
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Fixed Sentinel feat truncated sheet description")
    
    # --- 2j. Shield Master: update description for energy shields ---
    elif eid == 'ID_SW_FEAT_SHIELD_MASTER':
        new_desc = "You gain a +2 bonus to Dexterity Saving Throws while wielding a physical or energy shield. If a force ability forces you to make a Dexterity Saving Throw, you can use a reaction to shield yourself and diminish the effect's damage. On a failed Saving Throw, you only take half damage. On a successful Saving Throw, you don't take any damage."
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = new_desc
        sheet = elem.find('sheet')
        for d in list(sheet.findall('description')):
            sheet.remove(d)
        sd = ET.SubElement(sheet, 'description')
        sd.text = new_desc
        log("  Updated Shield Master description for energy shields")

# Create ASI trait elements for Athlete, Lightly Armoured, Moderately Armoured (STR/DEX only)
for feat_name, support_name in [('Athlete', 'Athlete ASI'), ('Lightly Armoured', 'Lightly Armoured ASI'), ('Moderately Armoured', 'Moderately Armoured ASI')]:
    for ability_name, stat_name in [('Strength', 'strength'), ('Dexterity', 'dexterity')]:
        trait_id = f'ID_SW_FEAT_{feat_name.upper().replace(" ", "_")}_{stat_name.upper()}'
        if not any(e.get('id') == trait_id for e in root.findall('.//element')):
            trait = ET.SubElement(root, 'element')
            trait.set('name', f'{ability_name} +1')
            trait.set('type', 'Racial Trait')
            trait.set('source', 'SW-MSV-Edition')
            trait.set('id', trait_id)
            supports = ET.SubElement(trait, 'supports')
            supports.text = support_name
            compendium = ET.SubElement(trait, 'compendium')
            compendium.set('display', 'false')
            desc = ET.SubElement(trait, 'description')
            p = ET.SubElement(desc, 'p')
            p.text = f'Your {ability_name} score increases by 1.'
            sheet = ET.SubElement(trait, 'sheet')
            sheet_desc = ET.SubElement(sheet, 'description')
            sheet_desc.text = f'+1 {ability_name}'
            rules_el = ET.SubElement(trait, 'rules')
            stat = ET.SubElement(rules_el, 'stat')
            stat.set('name', stat_name)
            stat.set('value', '1')

log("  Created STR/DEX ASI trait options for Athlete, Lightly/Moderately Armoured")

# Fix abbreviations in feats.xml
abbrev_count = fix_abbreviations(root)
log(f"  Fixed {abbrev_count} abbreviation instances in feats.xml")

tree.write('feats.xml', encoding='utf-8', xml_declaration=True)
log("  Saved feats.xml")

# ============================================================
# PART 3: ITEMS/WEAPONS FIXES
# ============================================================
log("\n=== PART 3: ITEMS/WEAPONS FIXES ===")

# --- 3a. Fix thermal detonator spelling ---
tree = ET.parse('items-explosives.xml')
root = tree.getroot()

for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_ITEM_THERMAL_DETENATOR':
        elem.set('name', 'thermal detonator')
        elem.set('id', 'ID_ITEM_THERMAL_DETONATOR')
        log("  Fixed thermal detenator -> thermal detonator (name and ID)")

tree.write('items-explosives.xml', encoding='utf-8', xml_declaration=True)
log("  Saved items-explosives.xml")

# --- 3b. Add Dart action to Stealth Pistol ---
tree = ET.parse('weapons.xml')
root = tree.getroot()

for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    
    if eid == 'ID_WEAPON_STEALTH_PISTOL':
        rules = elem.find('rules')
        has_dart = any(g.get('id') == 'ID_ACTION_DART' for g in rules.findall('grant'))
        if not has_dart:
            dart = ET.SubElement(rules, 'grant')
            dart.set('type', 'Action')
            dart.set('id', 'ID_ACTION_DART')
            log("  Added Dart action grant to Stealth Pistol")

    # --- 3c. Wrist Blaster -> Wrist Launcher with Wrist Blaster Attachment ---
    elif eid == 'ID_WEAPON_WRIST_BLASTER':
        elem.set('name', 'Wrist Launcher with Wrist Blaster Attachment')
        desc = elem.find('description')
        for p in list(desc):
            desc.remove(p)
        p1 = ET.SubElement(desc, 'p')
        strong = ET.SubElement(p1, 'strong')
        strong.text = 'Wrist Launcher with Wrist Blaster Attachment'
        p2 = ET.SubElement(desc, 'p')
        em = ET.SubElement(p2, 'em')
        em.text = 'Simple Blaster'
        p3 = ET.SubElement(desc, 'p')
        em2 = ET.SubElement(p3, 'em')
        em2.text = '1d6 energy damage, power cell, range 30/120, Reload 8, Dexterity modifier'
        p4 = ET.SubElement(desc, 'p')
        p4.text = "This wrist-mounted launcher with blaster attachment fires energy bolts. It can't be disarmed, you can still use your hand but can't use the weapon when holding something."
        p5 = ET.SubElement(desc, 'p')
        strong2 = ET.SubElement(p5, 'strong')
        strong2.text = 'Actions:'
        p6 = ET.SubElement(desc, 'p')
        p6.text = '\u2022 Shoot: As an Action, Make a ranged attack. On hit: 1d6 energy damage + your Dexterity modifier.'
        p7 = ET.SubElement(desc, 'p')
        p7.text = '\u2022 Quick Shot: As a Bonus Action, Make a quick hipfire shot. On hit: 1d6 energy damage without modifiers.'
        log("  Renamed Wrist Blaster -> Wrist Launcher with Wrist Blaster Attachment")

tree.write('weapons.xml', encoding='utf-8', xml_declaration=True)
log("  Saved weapons.xml")

# --- 3d. Fix Jumppack/Hoverpack/Jetpack descriptions to match boots ---
tree = ET.parse('items-tools.xml')
root = tree.getroot()

for elem in root.findall('.//element'):
    eid = elem.get('id', '')
    
    if eid == 'ID_ITEM_JUMPPACK':
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = 'As a Bonus Action, jump up to 25 feet vertically or horizontally. Provokes opportunity attacks when leaving or landing in enemy melee range. Requires jumppack proficiency.'
        log("  Updated Jumppack description to match Jump Boots")
    
    elif eid == 'ID_ITEM_HOVERPACK':
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = 'As a Bonus Action, hover up to 15 feet in the air on the same spot for 2 turns. Cannot move. While hovering, you have advantage on ranged attacks and disadvantage on Dexterity saving throws. Provokes opportunity attacks when leaving or landing in enemy melee range. Requires hoverpack proficiency.'
        log("  Updated Hoverpack description to match Hover Boots")
    
    elif eid == 'ID_ITEM_JETPACK':
        desc = elem.find('description')
        for p in list(desc.findall('p')):
            desc.remove(p)
        p = ET.SubElement(desc, 'p')
        p.text = 'As a Bonus Action, jump up to 30 feet or hover up to 15 feet in the air. Can move up to 10 feet while hovering. While hovering, you have advantage on ranged attacks and no disadvantage on Dexterity saving throws. Provokes opportunity attacks when leaving or landing in enemy melee range. Requires jumppack, hoverpack, and jetpack proficiency.'
        log("  Updated Jetpack description to match Jet Boots")
    
    elif eid == 'ID_ITEM_ROCKETPACK':
        setters = elem.find('setters')
        has_slot = False
        for s in setters.findall('set'):
            if s.get('name') == 'slot':
                s.text = 'body'
                has_slot = True
        if not has_slot:
            slot = ET.SubElement(setters, 'set')
            slot.set('name', 'slot')
            slot.text = 'body'
        log("  Updated Rocketpack: set slot=body")

tree.write('items-tools.xml', encoding='utf-8', xml_declaration=True)
log("  Saved items-tools.xml")

# ============================================================
# PART 4: CLASS FIXES
# ============================================================
log("\n=== PART 4: CLASS FIXES ===")

# --- 4a. Marauder Fast Movement: add +10 speed rule ---
tree = ET.parse('class-marauder.xml')
root = tree.getroot()

for elem in root.findall('.//element'):
    if elem.get('id') == 'ID_CLASS_MARAUDER_FEATURE_FAST_MOVEMENT':
        rules = elem.find('rules')
        if rules is None:
            rules = ET.SubElement(elem, 'rules')
        has_speed = any(s.get('name') == 'speed' for s in rules.findall('stat'))
        if not has_speed:
            stat = ET.SubElement(rules, 'stat')
            stat.set('name', 'speed')
            stat.set('value', '10')
            log("  Added +10 speed rule to Marauder Fast Movement")

abbrev_count = fix_abbreviations(root)
if abbrev_count:
    log(f"  Fixed {abbrev_count} abbreviation instances in class-marauder.xml")
tree.write('class-marauder.xml', encoding='utf-8', xml_declaration=True)
log("  Saved class-marauder.xml")

# --- Fix abbreviations in all remaining XML files ---
all_xml_files = [
    'fighting-styles.xml', 'class-knight.xml', 'class-inquisitor.xml', 
    'class-scout.xml', 'class-warrior.xml', 'backgrounds.xml', 
    'items-armor.xml', 'items-explosives.xml', 'items-healing.xml', 
    'items-instruments.xml', 'items-tools.xml', 'languages.xml', 
    'maneuvers.xml', 'proficiencies.xml', 'weapons.xml'
]

for xml_file in all_xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    abbrev_count = fix_abbreviations(root)
    if abbrev_count > 0:
        log(f"  Fixed {abbrev_count} abbreviation instances in {xml_file}")
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# ============================================================
# PART 5: VERSION BUMP (1.1.6 -> 1.1.7)
# ============================================================
log("\n=== PART 5: VERSION BUMP ===")

all_files = [
    'backgrounds.xml', 'class-inquisitor.xml', 'class-knight.xml', 'class-marauder.xml',
    'class-scout.xml', 'class-warrior.xml', 'feats.xml', 'fighting-styles.xml',
    'items-armor.xml', 'items-explosives.xml', 'items-healing.xml', 'items-instruments.xml',
    'items-tools.xml', 'languages.xml', 'maneuvers.xml', 'proficiencies.xml',
    'source.xml', 'species.xml', 'weapons.xml', 'sw-msv-edition.index'
]

for filename in all_files:
    if not os.path.exists(filename):
        continue
    tree = ET.parse(filename)
    root = tree.getroot()
    for elem in root.iter():
        if elem.tag == 'update' and 'version' in elem.attrib:
            elem.attrib['version'] = '1.1.7'
            break
    tree.write(filename, encoding='utf-8', xml_declaration=True)

log("  All files bumped to version 1.1.7")

# ============================================================
# SUMMARY
# ============================================================
log("\n=== SUMMARY ===")
log(f"Total changes logged: {len(changes_log)}")
print("\nAll changes complete!")

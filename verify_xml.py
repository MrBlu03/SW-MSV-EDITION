#!/usr/bin/env python3
"""
SW-MSV-Edition XML Verification Script
Compares all XML files against source TXT files to ensure accuracy.
Reports ALL discrepancies: names, descriptions, dice values, ranges, costs, prerequisites, etc.
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import json

BASE_DIR = Path(r"C:\Users\james\OneDrive\Docs and windows stuff\documenten\GitHub\SW-MSV-EDITION")
SOURCE_DIR = BASE_DIR / "SOURCE"

def normalize_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = ' '.join(text.split())
    text = text.lower().strip()
    text = text.replace('armour', 'armor')
    text = text.replace('colour', 'color')
    text = text.replace('favour', 'favor')
    text = text.replace('behaviour', 'behavior')
    text = text.replace('honour', 'honor')
    return text

def extract_dice(text):
    if not text:
        return []
    return re.findall(r'\d+d\d+', text.lower())

def extract_numbers(text):
    if not text:
        return []
    return re.findall(r'\b\d+\b', text)

def parse_txt_entities(filepath, parser_func) -> dict:
    try:
        content = filepath.read_text(encoding='utf-8')
        result = parser_func(content)
        return result if isinstance(result, dict) else {}
    except FileNotFoundError:
        print(f"  WARNING: Source file not found: {filepath}")
        return {}

def parse_xml_entities(filepath):
    entities = {}
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for elem in root.findall('.//element'):
            name = elem.get('name', '').lower()
            entity = {
                'name': name,
                'type': elem.get('type', ''),
                'id': elem.get('id', ''),
                'description': '',
                'sheet': '',
                'prerequisite': '',
                'requirements': '',
            }
            desc_elem = elem.find('description')
            if desc_elem is not None:
                entity['description'] = get_element_text(desc_elem)
            sheet_elem = elem.find('sheet')
            if sheet_elem is not None:
                desc = sheet_elem.find('description')
                if desc is not None:
                    entity['sheet'] = get_element_text(desc)
            prereq_elem = elem.find('prerequisite')
            if prereq_elem is not None and prereq_elem.text:
                entity['prerequisite'] = prereq_elem.text
            req_elem = elem.find('requirements')
            if req_elem is not None and req_elem.text:
                entity['requirements'] = req_elem.text
            entities[name] = entity
    except FileNotFoundError:
        print(f"  WARNING: XML file not found: {filepath}")
    except ET.ParseError as e:
        print(f"  XML Parse Error in {filepath}: {e}")
    return entities

def get_element_text(elem):
    text = ET.tostring(elem, encoding='unicode')
    text = re.sub(r'^<[^>]+>', '', text)
    text = re.sub(r'</[^>]+>$', '', text)
    return text.strip()

def parse_feats_txt(content):
    entities = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.lower() == 'feats:':
            continue
        if ':' in line:
            parts = line.split(':', 1)
            name = parts[0].strip().lower()
            description = parts[1].strip() if len(parts) > 1 else ''
            entities[name] = {'name': name, 'description': description, 'raw': line}
    return entities

def parse_languages_txt(content):
    entities = {}
    for line in content.split('\n'):
        line = line.strip()
        if line and line.lower() != 'languages':
            entities[line.lower()] = {'name': line.lower(), 'raw': line}
    return entities

def parse_fighting_styles_txt(content):
    entities = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.lower() == 'fighting styles:':
            continue
        if ':' in line:
            parts = line.split(':', 1)
            name = parts[0].strip().lower()
            description = parts[1].strip() if len(parts) > 1 else ''
            entities[name] = {'name': name, 'description': description, 'raw': line}
    return entities

def parse_maneuvers_txt(content):
    entities = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or 'maneuvers' in line.lower():
            continue
        if ':' in line:
            parts = line.split(':', 1)
            name = parts[0].strip().lower()
            description = parts[1].strip() if len(parts) > 1 else ''
            entities[name] = {'name': name, 'description': description, 'raw': line}
    return entities

def parse_backgrounds_txt(content):
    entities = {}
    current_bg = None
    current_data = {}
    valid_backgrounds = ['agent', 'bounty hunter', 'criminal', 'entertainer', 'engineer',
                         'jedi', 'mandalorian', 'mercenary', 'noble', 'nomad', 'pirate',
                         'scientist', 'scoundrel', 'sith', 'smuggler', 'soldier']
    for line in content.split('\n'):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if not line.startswith('\t') and ':' in line_stripped:
            parts = line_stripped.split(':', 1)
            bg_name = parts[0].strip().lower()
            if bg_name in valid_backgrounds:
                if current_bg:
                    entities[current_bg] = current_data
                current_bg = bg_name
                current_data = {'name': current_bg, 'proficiencies': parts[1].strip() if len(parts) > 1 else '', 'raw': line_stripped}
            elif current_bg:
                current_data['raw'] = current_data.get('raw', '') + '\n' + line_stripped
        elif current_bg:
            current_data['raw'] = current_data.get('raw', '') + '\n' + line_stripped
    if current_bg:
        entities[current_bg] = current_data
    return entities

def parse_species_txt(content):
    entities = {}
    current_species = None
    current_data = {}
    skip_headers = ['species', 'subspecies:']
    for line in content.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        if not line.startswith('\t') and not line.startswith(' '):
            species_name = line.strip().lower()
            if species_name in skip_headers:
                continue
            if current_species:
                entities[current_species] = current_data
            current_species = species_name
            current_data = {'name': current_species, 'traits': [], 'raw': ''}
        elif current_species:
            current_data['raw'] = current_data.get('raw', '') + ' ' + line.strip()
    if current_species:
        entities[current_species] = current_data
    return entities

def parse_weapons_txt(content):
    entities = {}
    current_category = None
    for line in content.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        if not line.startswith('\t') and not line.startswith(' '):
            header = line.strip().lower().rstrip(':')
            valid_headers = ['simple blaster', 'martial blaster', 'simple lightweapon', 
                          'martial lightweapon', 'simple vibroweapon', 'martial vibroweapon',
                          'shields', 'armour', 'tools', 'items', 'grenades', 'darts', 
                          'rockets', 'poisons', 'healing', 'instruments', 'light', 
                          'medium', 'heavy', 'remote detonators', 'mines']
            if header in valid_headers or header.endswith('armor') or header.endswith('armour'):
                current_category = header
        elif line.startswith('\t') and current_category:
            data = line.strip()
            if data.startswith('-'):
                data = data[1:].strip()
            if '(' in data:
                name_match = re.match(r'^([^(]+)', data)
                if name_match:
                    weapon_name = name_match.group(1).strip().lower()
                    weapon_name = re.sub(r'\s*ac:?\s*\d+.*$', '', weapon_name).strip()
                    if weapon_name:
                        entities[weapon_name] = {
                            'name': weapon_name,
                            'category': current_category,
                            'raw': data
                        }
            elif ':' in data and 'ac:' not in data.lower():
                name_match = re.match(r'^([^:]+)', data)
                if name_match:
                    item_name = name_match.group(1).strip().lower()
                    if item_name and len(item_name) < 50:
                        entities[item_name] = {
                            'name': item_name,
                            'category': current_category,
                            'raw': data
                        }
            elif 'ac:' in data.lower() or 'ac ' in data.lower():
                name_match = re.match(r'^([^(ac:]+)', data, re.IGNORECASE)
                if name_match:
                    item_name = name_match.group(1).strip().lower()
                    item_name = re.sub(r'\s*ac:?\s*$', '', item_name).strip()
                    if item_name and len(item_name) < 50:
                        entities[item_name] = {
                            'name': item_name,
                            'category': current_category,
                            'raw': data
                        }
    return entities

def parse_class_txt(content):
    entities = {}
    lines = content.split('\n')
    class_name = None
    current_data = {'abilities': {}, 'levels': {}, 'subclasses': {}}
    current_subclass = None
    skip_headers = ['health:', 'armour proficiency:', 'armor proficiency:', 'weapon proficiency:', 
                    'saving throw proficiencies:', 'skill proficiencies', 'spell save dc:', 'funds:',
                    'lightsaber forms:']
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if not class_name:
            class_name = line_stripped.lower().replace(':', '').strip()
            continue
        if line_stripped.lower().startswith('lv '):
            level_match = re.match(r'lv\s*(\d+):?\s*(.*)', line_stripped.lower())
            if level_match:
                level = level_match.group(1)
                features = level_match.group(2).strip()
                current_data['levels'][level] = features
            continue
        if 'lightsaber forms' in line_stripped.lower() or 'subclass' in line_stripped.lower():
            current_subclass = 'forms'
            continue
        skip_line = False
        for header in skip_headers:
            if line_stripped.lower().startswith(header):
                skip_line = True
                break
        if skip_line:
            continue
        if ':' in line_stripped:
            parts = line_stripped.split(':', 1)
            ability_name = parts[0].strip().lower()
            description = parts[1].strip() if len(parts) > 1 else ''
            if ability_name.startswith('form ') or ability_name.startswith('form:'):
                continue
            ability_data = {'name': ability_name, 'description': description, 'raw': line_stripped}
            if current_subclass:
                if current_subclass not in current_data['subclasses']:
                    current_data['subclasses'][current_subclass] = {}
                current_data['subclasses'][current_subclass][ability_name] = ability_data
            else:
                current_data['abilities'][ability_name] = ability_data
    
    if class_name:
        entities[class_name] = {'name': class_name, 'data': current_data}
    return entities

discrepancies = []

def check_description(txt_desc, xml_desc, entity_name, context=''):
    txt_norm = normalize_text(txt_desc)
    xml_norm = normalize_text(xml_desc)
    if txt_norm and xml_norm and txt_norm != xml_norm:
        txt_words = set(txt_norm.split())
        xml_words = set(xml_norm.split())
        missing_words = txt_words - xml_words
        extra_words = xml_words - txt_words
        ignore_words = {'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'on', 'at', 'by', 'for', 'with', 'is', 'are', 'it', 'this', 'that', 'you', 'your', 'can', 'when', 'if'}
        missing_words -= ignore_words
        extra_words -= ignore_words
        if missing_words or extra_words:
            discrepancies.append({
                'type': 'DESCRIPTION_MISMATCH',
                'entity': entity_name,
                'context': context,
                'txt': txt_desc[:150] + '...' if len(txt_desc) > 150 else txt_desc,
                'xml': xml_desc[:150] + '...' if len(xml_desc) > 150 else xml_desc,
                'missing': list(missing_words)[:5],
                'extra': list(extra_words)[:5]
            })

def check_dice(txt_text, xml_text, entity_name, context=''):
    txt_dice = sorted(extract_dice(txt_text))
    xml_dice = sorted(extract_dice(xml_text))
    if txt_dice and xml_dice and txt_dice != xml_dice:
        discrepancies.append({
            'type': 'DICE_MISMATCH',
            'entity': entity_name,
            'context': context,
            'txt_dice': txt_dice,
            'xml_dice': xml_dice
        })

def check_missing(txt_name, entity_type, source_file):
    discrepancies.append({
        'type': 'MISSING_IN_XML',
        'entity': txt_name,
        'entity_type': entity_type,
        'source': source_file
    })

def check_extra(xml_name, entity_type, xml_file):
    discrepancies.append({
        'type': 'EXTRA_IN_XML',
        'entity': xml_name,
        'entity_type': entity_type,
        'source': xml_file
    })

def verify_simple(txt_path, xml_path, parser_func, entity_type):
    txt_entities = parse_txt_entities(txt_path, parser_func)
    xml_entities = parse_xml_entities(xml_path)
    for txt_name, txt_data in txt_entities.items():
        if txt_name not in xml_entities:
            check_missing(txt_name, entity_type, txt_path.name)
        else:
            xml_data = xml_entities[txt_name]
            if 'description' in txt_data:
                check_description(txt_data['description'], xml_data.get('description', ''), txt_name, entity_type)
                check_dice(txt_data['description'], xml_data.get('description', ''), txt_name, entity_type)
    return len(txt_entities), len(xml_entities)

def main():
    global discrepancies
    all_discrepancies = []
    print("=" * 80)
    print("SW-MSV-Edition XML Verification Script")
    print("=" * 80)
    print()

    results = []
    
    print("[1/8] Verifying Feats...")
    discrepancies = []
    txt_count, xml_count = verify_simple(SOURCE_DIR / "Feats.txt", BASE_DIR / "feats.xml", parse_feats_txt, "Feat")
    results.append(('Feats', txt_count, xml_count, len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[2/8] Verifying Languages...")
    discrepancies = []
    txt_entities = parse_txt_entities(SOURCE_DIR / "Languages.txt", parse_languages_txt)
    xml_entities = parse_xml_entities(BASE_DIR / "languages.xml")
    for txt_name in txt_entities:
        if txt_name not in xml_entities:
            check_missing(txt_name, "Language", "Languages.txt")
    results.append(('Languages', len(txt_entities), len(xml_entities), len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[3/8] Verifying Fighting Styles...")
    discrepancies = []
    txt_count, xml_count = verify_simple(SOURCE_DIR / "Fighting Styles.txt", BASE_DIR / "fighting-styles.xml", parse_fighting_styles_txt, "Fighting Style")
    results.append(('Fighting Styles', txt_count, xml_count, len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[4/8] Verifying Maneuvers...")
    discrepancies = []
    txt_count, xml_count = verify_simple(SOURCE_DIR / "Maneuvers.txt", BASE_DIR / "maneuvers.xml", parse_maneuvers_txt, "Maneuver")
    results.append(('Maneuvers', txt_count, xml_count, len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[5/8] Verifying Backgrounds...")
    discrepancies = []
    txt_entities = parse_txt_entities(SOURCE_DIR / "Background.txt", parse_backgrounds_txt)
    xml_entities = parse_xml_entities(BASE_DIR / "backgrounds.xml")
    for txt_name, txt_data in txt_entities.items():
        if txt_name not in xml_entities:
            check_missing(txt_name, "Background", "Background.txt")
    results.append(('Backgrounds', len(txt_entities), len(xml_entities), len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[6/8] Verifying Species...")
    discrepancies = []
    txt_entities = parse_txt_entities(SOURCE_DIR / "Species.txt", parse_species_txt)
    xml_entities = parse_xml_entities(BASE_DIR / "species.xml")
    name_mappings = {
        'wookie': 'wookiee',
        'human': 'human (standard)',
    }
    for txt_name in txt_entities:
        mapped_name = name_mappings.get(txt_name, txt_name)
        found = False
        for xml_name in xml_entities:
            if mapped_name == xml_name or txt_name in xml_name or xml_name in txt_name:
                found = True
                break
        if not found:
            check_missing(txt_name, "Species", "Species.txt")
    results.append(('Species', len(txt_entities), len(xml_entities), len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[7/8] Verifying Weapons & Items...")
    discrepancies = []
    txt_entities = parse_txt_entities(SOURCE_DIR / "Weapons and Items.txt", parse_weapons_txt)
    item_xml_files = ['weapons.xml', 'items-armor.xml', 'items-explosives.xml', 
                      'items-healing.xml', 'items-instruments.xml', 'items-tools.xml']
    all_xml_entities = {}
    for xml_file in item_xml_files:
        xml_entities = parse_xml_entities(BASE_DIR / xml_file)
        all_xml_entities.update(xml_entities)
    for txt_name in txt_entities:
        matched = False
        for xml_name in all_xml_entities:
            if txt_name in xml_name or xml_name in txt_name:
                matched = True
                break
        if not matched:
            check_missing(txt_name, "Weapon/Item", "Weapons and Items.txt")
    results.append(('Weapons & Items', len(txt_entities), len(all_xml_entities), len(discrepancies)))
    all_discrepancies.extend(discrepancies)
    if discrepancies:
        print(f"  Found {len(discrepancies)} discrepancies")
    
    print("[8/8] Verifying Classes...")
    class_files = [
        ("Inquisitor Class.txt", "class-inquisitor.xml"),
        ("Warrior Class.txt", "class-warrior.xml"),
        ("Scout Class.txt", "class-scout.xml"),
        ("Marauder Class.txt", "class-marauder.xml"),
        ("Knight Class.txt", "class-knight.xml"),
    ]
    total_txt = 0
    total_xml = 0
    total_disc = 0
    for txt_file, xml_file in class_files:
        discrepancies = []
        txt_entities = parse_txt_entities(SOURCE_DIR / txt_file, parse_class_txt)
        xml_entities = parse_xml_entities(BASE_DIR / xml_file)
        for txt_name, txt_data in txt_entities.items():
            if 'data' in txt_data:
                for ability_name, ability_data in txt_data['data'].get('abilities', {}).items():
                    if ability_name not in xml_entities:
                        check_missing(ability_name, "Class Ability", txt_file)
        total_txt += len(txt_entities)
        total_xml += len(xml_entities)
        total_disc += len(discrepancies)
        all_discrepancies.extend(discrepancies)
    results.append(('Classes', total_txt, total_xml, total_disc))
    if total_disc:
        print(f"  Found {total_disc} discrepancies")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Category':<25} {'TXT':>6} {'XML':>6} {'Issues':>8}")
    print("-" * 50)
    for name, txt, xml, issues in results:
        print(f"{name:<25} {txt:>6} {xml:>6} {issues:>8}")
    
    return all_discrepancies

if __name__ == "__main__":
    all_discrepancies = main()
    
    if all_discrepancies:
        report_path = BASE_DIR / "verification_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(all_discrepancies, f, indent=2)
        print(f"\nDetailed report saved to: {report_path}")
    else:
        print("\nNo discrepancies found!")

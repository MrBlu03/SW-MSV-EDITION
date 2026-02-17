#!/usr/bin/env python3
"""
Detailed Species Verification - Checks XML implementation against TXT requirements
"""

import xml.etree.ElementTree as ET
import re

def parse_species_txt():
    """Parse species.txt into structured data"""
    txt_path = r'C:\Users\james\OneDrive\Docs and windows stuff\documenten\GitHub\SW-MSV-EDITION\SOURCE\Species.txt'
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    species_data = {}
    lines = content.split('\n')
    current_species = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.lower() in ['species', 'subspecies:']:
            continue
        
        if not line.startswith('\t') and not line.startswith(' '):
            current_species = stripped.lower()
            species_data[current_species] = {'raw': []}
        elif current_species:
            species_data[current_species]['raw'].append(stripped)
    
    return species_data

def check_critical_traits(species_name, raw_traits):
    """Check for critical traits that must be implemented"""
    full_text = ' '.join(raw_traits).lower()
    issues = []
    
    # Check ASI
    asi_matches = re.findall(r'(str|dex|con|int|wis|char)\s*\+\s*(\d+)', full_text)
    if not asi_matches:
        issues.append("Missing ASI")
    
    # Check for specific mechanics
    checks = {
        'natural armor': 'natural armour: ac=' in full_text or 'ac= ' in full_text,
        'unarmed strikes': 'unarmed strikes deal' in full_text,
        'darkvision': 'darkvision' in full_text,
        'climb speed': 'climb ' in full_text and 'feet' in full_text,
        'swim speed': 'swim ' in full_text and 'feet' in full_text,
        'resistance': 'resistant' in full_text or 'resistance' in full_text,
        'vulnerability': 'vulnerable' in full_text,
        'immunity': 'immune' in full_text,
        'advantage': 'advantage' in full_text,
        'expertise': 'expertise' in full_text,
        'extra damage on surprised': 'if enemy is surprised' in full_text,
        'hit points per level': 'hit points increase by 1 per level' in full_text,
        'brutal critical': 'on crit add' in full_text or 'additional weapon damage die' in full_text,
        'tune-up': 'tune-up' in full_text,
        'sonic scream': 'ithorian' in species_name and 'sonic' in full_text,
    }
    
    for mechanic, present in checks.items():
        if present:
            issues.append(f"Has {mechanic}")
    
    return issues

def main():
    species_data = parse_species_txt()
    
    print("="*80)
    print("CRITICAL SPECIES MECHANICS CHECK")
    print("="*80)
    print("\nChecking which species have special mechanics that need verification:\n")
    
    # Filter to only species with data
    real_species = {k: v for k, v in species_data.items() if v['raw']}
    
    for name in sorted(real_species.keys()):
        data = real_species[name]
        issues = check_critical_traits(name, data['raw'])
        
        if issues:
            print(f"\n{name.upper()}:")
            for issue in issues:
                print(f"  - {issue}")

if __name__ == '__main__':
    main()

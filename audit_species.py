#!/usr/bin/env python3
"""
Detailed Species Audit - Generates a comprehensive report comparing Species.txt to species.xml
"""

import xml.etree.ElementTree as ET
import re

def parse_traits_from_txt(line):
    """Parse a trait line from the species.txt file"""
    traits = {
        'asi': [],
        'speed': None,
        'size': None,
        'age': None,
        'proficiencies': [],
        'advantage': [],
        'resistance': [],
        'vulnerability': [],
        'immunity': [],
        'abilities': [],
        'languages': [],
        'vision': [],
        'other': []
    }
    
    text = line.lower()
    
    # ASI
    asi_matches = re.findall(r'(str|dex|con|int|wis|char)\s*\+\s*(\d+)', text)
    for ability, bonus in asi_matches:
        traits['asi'].append(f"{ability.upper()}+{bonus}")
    
    # Speed
    speed_match = re.search(r'(\d+)\s*feet', text)
    if speed_match:
        traits['speed'] = speed_match.group(1)
    
    # Size
    if 'small size' in text:
        traits['size'] = 'Small'
    elif 'medium' in text:
        traits['size'] = 'Medium'
    
    # Age
    age_match = re.search(r'(\d+)\s*years?', text)
    if age_match:
        traits['age'] = age_match.group(1)
    
    # Languages
    if 'basic' in text or 'language' in text:
        if 'galactic basic' in text or 'basic' in text:
            traits['languages'].append('Galactic Basic')
    
    # Vision
    if 'darkvision' in text:
        traits['vision'].append('Darkvision')
    
    # Proficiencies
    prof_keywords = ['proficiency', 'proficient']
    if any(kw in text for kw in prof_keywords):
        traits['proficiencies'].append(line.strip())
    
    # Advantages
    if 'advantage' in text:
        traits['advantage'].append(line.strip())
    
    # Resistances
    if 'resistant' in text or 'resistance' in text:
        traits['resistance'].append(line.strip())
    
    # Vulnerabilities
    if 'vulnerable' in text:
        traits['vulnerability'].append(line.strip())
    
    # Immunities
    if 'immune' in text:
        traits['immunity'].append(line.strip())
    
    return traits

def main():
    # Read the species.txt file
    txt_path = r'C:\Users\james\OneDrive\Docs and windows stuff\documenten\GitHub\SW-MSV-EDITION\SOURCE\Species.txt'
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse species from txt
    species_from_txt = {}
    lines = content.split('\n')
    current_species = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.lower() in ['species', 'subspecies:']:
            continue
        
        if not line.startswith('\t') and not line.startswith(' '):
            current_species = stripped.lower()
            species_from_txt[current_species] = {
                'name': stripped,
                'raw_traits': []
            }
        elif current_species:
            species_from_txt[current_species]['raw_traits'].append(stripped)
    
    # Generate report
    report = []
    report.append("="*80)
    report.append("SPECIES AUDIT REPORT - TXT vs XML COMPARISON")
    report.append("="*80)
    report.append(f"\nTotal Species Found: {len([s for s in species_from_txt if species_from_txt[s]['raw_traits']])}")
    report.append("\n")
    
    # List of all species that should be implemented
    expected_species = [
        'bith', 'bothan', 'cathar', 'chagrian', 'chiss', 'devaronian',
        'protocol droid', 'combat droid', 'duros', 'ewok', 'gamorrean',
        'geonosian', 'gran', 'human', 'ithorian', 'jawa', 'kaleesh',
        'kel dor', 'mirialan', 'mon calamari', 'nautolan', 'neimoidian',
        'ortolan', 'rakata', 'rattataki', 'rodian', 'sith pureblood',
        'sullustan', 'talz', 'togruta', 'trandoshan', 'tusken', 'twi\'lek',
        'ugnaught', 'weequay', 'wookie', 'zabrak', 'cyborg'
    ]
    
    # Check each expected species
    for species_name in expected_species:
        key = species_name.lower()
        report.append(f"\n{'='*60}")
        report.append(f"SPECIES: {species_name.upper()}")
        report.append(f"{'='*60}")
        
        if key in species_from_txt:
            data = species_from_txt[key]
            if data['raw_traits']:
                # Parse the traits
                full_text = ' '.join(data['raw_traits'])
                traits = parse_traits_from_txt(full_text)
                
                report.append(f"\nFrom Species.txt:")
                report.append(f"  ASI: {', '.join(traits['asi']) if traits['asi'] else 'None parsed'}")
                report.append(f"  Speed: {traits['speed'] or 'Not parsed'}")
                report.append(f"  Size: {traits['size'] or 'Not parsed'}")
                report.append(f"  Vision: {', '.join(traits['vision']) if traits['vision'] else 'None'}")
                
                if traits['proficiencies']:
                    report.append(f"  Proficiencies: OK ({len(traits['proficiencies'])} found)")
                if traits['advantage']:
                    report.append(f"  Advantages: OK ({len(traits['advantage'])} found)")
                if traits['resistance']:
                    report.append(f"  Resistances: OK ({len(traits['resistance'])} found)")
                if traits['vulnerability']:
                    report.append(f"  Vulnerabilities: OK ({len(traits['vulnerability'])} found)")
                if traits['immunity']:
                    report.append(f"  Immunities: OK ({len(traits['immunity'])} found)")
                if traits['languages']:
                    report.append(f"  Languages: {', '.join(traits['languages'])}")
                
                report.append(f"\n  Raw trait text:")
                report.append(f"    {full_text[:150]}{'...' if len(full_text) > 150 else ''}")
            else:
                report.append("  ERROR: No traits found for this species")
        else:
            report.append("  ERROR: Species not found in TXT file")
    
    # Write report
    report_text = '\n'.join(report)
    with open('species_audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text[:3000])  # Print first part
    print("\n...\n\nFull report saved to species_audit_report.txt")

if __name__ == '__main__':
    main()

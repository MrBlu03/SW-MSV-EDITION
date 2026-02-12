import xml.etree.ElementTree as ET
import os
from collections import defaultdict

# Collect all defined IDs
defined_ids = set()
xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]
for xml_file in xml_files:
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for elem in root.iter():
            if 'id' in elem.attrib:
                defined_ids.add(elem.attrib['id'])
    except Exception as e:
        print(f'Error parsing {xml_file}: {e}')

print(f'Total defined IDs: {len(defined_ids)}')

# Collect all referenced IDs
referenced_ids = defaultdict(list)
for xml_file in xml_files:
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for elem in root.iter():
            # Check for grant elements
            if elem.tag == 'grant' and 'id' in elem.attrib:
                referenced_ids[elem.attrib['id']].append(xml_file)
            # Check for supports elements
            elif elem.tag == 'supports':
                if elem.text:
                    referenced_ids[elem.text.strip()].append(xml_file)
            # Check for other potential references (like in descriptions or other attributes)
            for attr, value in elem.attrib.items():
                if attr != 'id' and value.startswith('ID_'):
                    referenced_ids[value].append(xml_file)
    except Exception as e:
        print(f'Error parsing {xml_file}: {e}')

print(f'Total referenced IDs: {len(referenced_ids)}')

# Find undefined references
undefined = []
for ref_id, files in referenced_ids.items():
    if ref_id not in defined_ids:
        undefined.append((ref_id, files))

if undefined:
    print(f'\nUNDEFINED REFERENCES ({len(undefined)}):')
    for ref_id, files in sorted(undefined):
        print(f'  {ref_id}: {sorted(set(files))}')
else:
    print('\nNo undefined references found.')

# Check for potential issues in specific files
print('\nChecking for other potential issues...')

# Check proficiencies.xml for non-MSV IDs (should only have custom ones now)
try:
    tree = ET.parse('proficiencies.xml')
    root = tree.getroot()
    non_msv_profs = []
    for elem in root.iter():
        if 'id' in elem.attrib and elem.attrib['id'].startswith('ID_PROFICIENCY_') and not elem.attrib['id'].startswith('ID_MSV_PROFICIENCY_'):
            non_msv_profs.append(elem.attrib['id'])
    if non_msv_profs:
        print(f'WARNING: Found {len(non_msv_profs)} core proficiency IDs still in proficiencies.xml:')
        for prof in non_msv_profs:
            print(f'  {prof}')
    else:
        print('✓ proficiencies.xml only contains MSV-prefixed custom proficiencies.')
except Exception as e:
    print(f'Error checking proficiencies.xml: {e}')

# Check for duplicate names (case-insensitive)
names = defaultdict(list)
for xml_file in xml_files:
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for elem in root.iter():
            if 'name' in elem.attrib:
                names[elem.attrib['name'].lower()].append((elem.attrib['name'], xml_file))
    except:
        pass

duplicate_names = {k: v for k, v in names.items() if len(v) > 1}
if duplicate_names:
    print(f'\nDUPLICATE NAMES (case-insensitive) ({len(duplicate_names)}):')
    for name_lower, instances in sorted(list(duplicate_names.items())[:10]):
        print(f'  \"{name_lower}\": {instances}')
else:
    print('✓ No duplicate names found.')
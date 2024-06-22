import json

# File paths
file1 = 'reference1.json'
file2 = 'reference2.json'

# Read JSON data from files
with open(file1, 'r') as f1, open(file2, 'r') as f2:
    dict1 = json.load(f1)
    dict2 = json.load(f2)

# Merge dictionaries
merged_dict = {**dict1, **dict2}

# Convert the merged dictionary back to a compact JSON string
compact_json = json.dumps(merged_dict, separators=(',', ':'))

# Optionally, write the compact JSON to a new file
output_file = 'reference.json'
with open(output_file, 'w') as f_out:
    f_out.write(compact_json)


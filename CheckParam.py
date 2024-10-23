from fitparse import FitFile
from collections import defaultdict
#check if this push worked
#and check the commit
def analyze_fit_file(file_path):
    fitfile = FitFile(file_path)
    
    # Dictionary to store field information
    fields_info = defaultdict(lambda: {'type': set(), 'sample': None})

    # Iterate through all messages
    for message in fitfile.messages:
        for field in message:
            field_name = field.name
            fields_info[field_name]['type'].add(type(field.value).__name__)
            if fields_info[field_name]['sample'] is None:
                fields_info[field_name]['sample'] = field.value

    # Print the results
    print(f"Fields available in {file_path}:")
    print("-" * 60)
    print(f"{'Field Name':<30} {'Data Type(s)':<20} {'Sample Value'}")
    print("-" * 60)
    
    for field, info in sorted(fields_info.items()):
        types = ', '.join(sorted(info['type']))
        sample = str(info['sample'])
        if len(sample) > 20:
            sample = sample[:17] + '...'
        print(f"{field:<30} {types:<20} {sample}")

# Usage
fit_file_path = 'FitFiles\91301803.fit'
analyze_fit_file(fit_file_path)

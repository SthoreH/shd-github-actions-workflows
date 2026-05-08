# shared-actions/composite/token-replacer/main.py
import os
import json
import sys

def run_replacement():
    # 1. Load inputs from environment variables
    files_raw = os.environ.get('INPUT_FILES', '').strip()
    vars_json = os.environ.get('INPUT_VARS', '{}').strip()

    if not files_raw or files_raw == 'null':
        print(">> [Token Replacer] No files provided for replacement. Skipping step.")
        return

    try:
        variables = json.loads(vars_json)
    except json.JSONDecodeError as e:
        print(f">> [Token Replacer] Error: Failed to parse vars JSON: {e}")
        sys.exit(1)

    # 2. Process each file in the list
    file_list = files_raw.split()
    
    for file_path in file_list:
        # Security Check: Prevent directory traversal or modifying CI internals
        normalized_path = os.path.normpath(file_path)
        if normalized_path.startswith("..") or ".github" in normalized_path:
            print(f">> [Token Replacer] Access Denied: {file_path} is restricted.")
            continue

        if not os.path.exists(normalized_path):
            print(f">> [Token Replacer] Warning: File not found: {file_path}")
            continue

        print(f">> [Token Replacer] Processing tokens in: {normalized_path}")
        
        try:
            with open(normalized_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 3. Perform string replacement for each key in variables
            for key, value in variables.items():
                # Matches pattern ${key}
                placeholder = f"${{{key}}}"
                if placeholder in content:
                    # Ensuring the value is cast to string (e.g. for numbers/booleans)
                    content = content.replace(placeholder, str(value))

            # 4. Save changes only if something actually changed
            if content != original_content:
                with open(normalized_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f">> [Token Replacer] Successfully updated: {normalized_path}")
            else:
                print(f">> [Token Replacer] No tokens found in: {normalized_path}")

        except Exception as e:
            print(f">> [Token Replacer] Failed to process {file_path}: {str(e)}")

if __name__ == "__main__":
    run_replacement()
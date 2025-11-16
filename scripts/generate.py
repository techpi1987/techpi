from datetime import datetime

# This script generates or updates a file that will be committed by the GitHub Actions workflow.
output_path = 'scripts/generated.txt'

now = datetime.utcnow().isoformat() + 'Z'
content = f"Auto-generated timestamp: {now}\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)

print(f"Wrote to {output_path}: {content.strip()}")

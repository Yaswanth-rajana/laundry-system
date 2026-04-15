import re

with open('README.md', 'r') as f:
    text = f.read()

# 1. Fix Access System Section
old_access = """Access the System
Interface	URL
Web UI	http://localhost:8000/frontend.html
API Docs	http://localhost:8000/docs
API Root	http://localhost:8000"""

new_access = """## 🌐 Access the System

- Web UI: http://localhost:8000/frontend.html  
- API Docs: http://localhost:8000/docs  
- API Root: http://localhost:8000"""
text = text.replace(old_access, new_access)

# 2 & 3. Fix Sample API Call
old_sample = """Sample API Call
bash
# Create an order
curl -X POST http://localhost:8000/orders \\
  -H "Content-Type: application/json" \\
  -d '{
    "customer_name": "Raj Kumar",
    "phone": "9876543210",
    "garments": [
      {"type": "Shirt", "quantity": 2},
      {"type": "Pants", "quantity": 1}
    ]
  }'"""
new_sample = """## Create an order

```bash
curl -X POST http://localhost:8000/orders \\
  -H "Content-Type: application/json" \\
  -d '{
    "customer_name": "Raj Kumar",
    "phone": "9876543210",
    "garments": [
      {"type": "Shirt", "quantity": 2},
      {"type": "Pants", "quantity": 1}
    ]
  }'
```"""
text = text.replace(old_sample, new_sample)

# 4. Fix Inline Python Blocks
# Look for blocks that start with '\npython\n'
import re
# We need to replace \npython\n<content>\n<Text starting with Non-space>
# Actually, the user asked to fix `python\n` with ````python\n`. And properly close them.
# I can just find '\npython\n' and replace it with '\n```python\n'
text = text.replace('\npython\n', '\n```python\n')
# Now we need to close the backticks. Wait, Python scripts will be properly closed if they end where another markdown element starts, but it's hard to parse accurately in a small script.
# Let's fix them manually or with regex.
# Actually, let's fix the specific instances.
# And fix project structure block.
old_structure = """📁 Project Structure
text
DryClean/
│
├── app/                    # Backend (routes, services, storage)
├── frontend.html           # Web UI
├── requirements.txt
└── README.md"""

new_structure = """## 📁 Project Structure

```text
DryClean/
│
├── app/                    # Backend (routes, services, storage)
├── frontend.html           # Web UI
├── requirements.txt
└── README.md
```"""
text = text.replace(old_structure, new_structure)

# Fix tables!
def fix_table_format(match):
    lines = match.group(0).strip().split('\n')
    new_lines = []
    # add | to start and end, replace tabs with |
    header = True
    for line in lines:
        if not line.strip(): continue
        replaced = "| " + line.replace('\t', ' | ') + " |"
        new_lines.append(replaced)
        if header:
            # create separator
            cols = len(line.split('\t'))
            sep = "|" + "|".join(["---" for _ in range(cols)]) + "|"
            new_lines.append(sep)
            header = False
    return '\n'.join(new_lines) + '\n'

# Table 1: Feature Description Status
# We can regex match lines containing tabs. A block of lines containing tabs is a table.
# Exclude lines that start with spaces (code blocks).
blocks = re.split(r'(\n(?:[^\n\t]+\t[^\n]+\n)+)', text)
for i in range(1, len(blocks), 2):
    if blocks[i].startswith('\n'):
        blocks[i] = '\n' + fix_table_format(re.match(r'\n(.*)', blocks[i], re.DOTALL))

text = "".join(blocks)

with open('README.md', 'w') as f:
    f.write(text)


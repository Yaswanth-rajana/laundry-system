with open('README.md', 'r') as f:
    lines = f.readlines()

out = []
in_code = False
for line in lines:
    # if it's the start of a block we previously mangled:
    if line.startswith('```python'):
        out.append(line)
        in_code = True
        continue
    
    if in_code:
        # Detect end of code block. Usually it's followed by a non-indented text, or header, or "Business value:", "Problem:", "My Fix:"
        if line.startswith('Problem:') or line.startswith('My Fix:') or line.startswith('Why ') or line.startswith('Business value:') or line.startswith('AI suggested') or line.startswith('Failure ') or line.startswith('##') or line.startswith('What AI') or line.startswith('AI\'s '):
            out.append('```\n')
            in_code = False
            out.append(line)
            continue
        # Also fix closing before another ```python
        if line.startswith('```python'):
            out.append('```\n')
            in_code = False
            out.append(line)
            in_code = True
            continue
            
    out.append(line)

# Handle end of file
if in_code:
    out.append('```\n')

# Find the Request/Response blocks which were also just text:
text = "".join(out)

import re
text = re.sub(r'\nhttp\n', r'\n```http\n', text)
text = re.sub(r'\njson\n', r'\n```json\n', text)
text = re.sub(r'\nbash\n', r'\n```bash\n', text)

with open('README.md', 'w') as f:
    f.write(text)

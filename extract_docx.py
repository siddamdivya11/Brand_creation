import xml.etree.ElementTree as ET
import os

try:
    path = 'temp_bizforge_extracted/word/document.xml'
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        exit(1)

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    tree = ET.parse(path)
    text_content = []
    
    for p in tree.iter(f"{{{ns['w']}}}p"):
        texts = [node.text for node in p.iter(f"{{{ns['w']}}}t") if node.text]
        if texts:
            text_content.append(''.join(texts))
            
    print("\n".join(text_content))

except Exception as e:
    print(f"Error parsing XML: {e}")

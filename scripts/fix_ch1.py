
import os

# Try multiple possible path encodings
base = "D:/document/"
# The dir with Arabic name
for entry in os.listdir(base):
    if "نموذج" in entry:
        dirname = entry
        break

vdir = os.path.join(base, dirname, "فصول")
for entry in os.listdir(vdir):
    if entry.startswith("01-الفصل") and "__" not in entry and "orig" not in entry and "المعاد" not in entry:
        filepath = os.path.join(vdir, entry)
        print(f"Found active file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"Size: {len(content)} chars")
        print(f"القصر count: {content.count('القصر')}")
        print(f"نورك count: {content.count('نورك')}")
        print(f"أعرفها from القصائد present: {'أعرفها من القصائد' in content}")
        print(f"تبخَّر present: {'تبخَّر' in content}")
        print(f"رقّة present: {'رقّةٌ' in content}")
        print(f"البيت لا ينام present: {'البيتَ لا ينامُ' in content}")

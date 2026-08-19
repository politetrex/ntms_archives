from lib.fetch import fetchContent, writeContent
import os
import time
files = {}
# archived/final/*.txt
for filename in os.listdir("archived/final"):
    if filename.endswith(".txt"):
        with open(os.path.join("archived/final", filename), "r", encoding="utf-8", errors="surrogateescape") as f:
            files[filename] = f.read()
for i in range(5000):
    for filename, content in files.items():
        print(f"Writing {filename} to note.ms...")
        writeContent(filename, "This content is refreshed by politetrex with 3.33Hz. \n\n"+content)
        time.sleep(0.3)  # Add a small delay to avoid overwhelming the server
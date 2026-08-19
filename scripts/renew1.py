from lib.fetch import fetchContent, writeContent
import os, time, random
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
        time.sleep(random.uniform(1,2))  # Add a delay to avoid overwhelming the server and causing rate limiting
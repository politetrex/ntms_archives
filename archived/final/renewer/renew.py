# fetch most recent articles from archived/beifen******** (asteriks is date)
# then put to archived/final/

import argparse
import os
import re
from datetime import datetime


def find_snapshot_dirs(archive_root):
    """Return all snapshot directories matching beifenYYYYMMDD, oldest to newest."""
    pattern = re.compile(r"^beifen(\d{8})$")
    matches = []

    if not os.path.isdir(archive_root):
        raise FileNotFoundError(f"Archive root does not exist: {archive_root}")

    for entry in os.listdir(archive_root):
        full_path = os.path.join(archive_root, entry)
        if not os.path.isdir(full_path):
            continue
        match = pattern.match(entry)
        if not match:
            continue
        try:
            snapshot_date = datetime.strptime(match.group(1), "%Y%m%d")
            matches.append((snapshot_date, full_path, entry))
        except ValueError:
            continue

    if not matches:
        raise FileNotFoundError(f"No snapshot directories found under {archive_root}")

    matches.sort(key=lambda item: item[0])
    return [path for _, path, _ in matches]


def merge_snapshots(snapshot_dirs, target_dir):
    """For each article, keep the newest version from the newest snapshot that contains it."""
    os.makedirs(target_dir, exist_ok=True)
    copied = set()

    for snapshot_dir in snapshot_dirs:
        for name in sorted(os.listdir(snapshot_dir)):
            src_path = os.path.join(snapshot_dir, name)
            if not os.path.isfile(src_path):
                continue

            with open(src_path, "r", encoding="utf-8", errors="surrogateescape") as src_file:
                content = src_file.read()

            dst_path = os.path.join(target_dir, name)
            with open(dst_path, "w", encoding="utf-8", errors="surrogateescape") as dst_file:
                dst_file.write(content)

            copied.add(name)

    return sorted(copied)


def main():
    parser = argparse.ArgumentParser(description="Refresh the final archive from all dated beifen snapshots, keeping the newest file version for each article.")
    parser.add_argument("--archive-root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), help="Directory containing beifen* snapshots.")
    parser.add_argument("--target-dir", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), help="Directory receiving the merged snapshot data.")
    args = parser.parse_args()

    archive_root = os.path.abspath(args.archive_root)
    target_dir = os.path.abspath(args.target_dir)

    snapshot_dirs = find_snapshot_dirs(archive_root)
    copied = merge_snapshots(snapshot_dirs, target_dir)

    print(f"Scanned {len(snapshot_dirs)} snapshot folders")
    print(f"Merged {len(copied)} article files into {target_dir}")
    for name in copied:
        print(f"  - {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

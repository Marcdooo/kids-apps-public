#!/usr/bin/env python3
"""Clone this project into a new app.

    python3 tools/new_app.py DEST_DIR --name sea_coloring

Copies the template, renames the Dart package, and prints the next steps.
The new app then only needs its own pictures (or other content), its text in
assets/i18n/, and an icon. Does not copy platform folders (android/, ios/),
because `flutter create` generates those with the new app's package id.
"""
import argparse
import os
import re
import shutil
import sys

SKIP_DIRS = {"build", ".dart_tool", "android", "ios", "web", "linux", "macos",
             "windows", ".idea", ".git", "__pycache__"}
SKIP_FILES = {"pubspec.lock", ".metadata", ".flutter-plugins",
              ".flutter-plugins-dependencies", ".packages"}


def current_package_name(project_dir):
    """The Dart package name of the project being cloned, from its pubspec."""
    with open(os.path.join(project_dir, "pubspec.yaml"), encoding="utf-8") as f:
        match = re.search(r"^name:\s*(\S+)", f.read(), re.MULTILINE)
    if not match:
        sys.exit("could not find 'name:' in pubspec.yaml")
    return match.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dest")
    ap.add_argument("--name", required=True,
                    help="new Dart package name: lowercase letters, digits, underscores")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.name):
        sys.exit("--name must be lowercase letters, digits and underscores, starting with a letter")
    src = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dest = os.path.abspath(args.dest)
    old_name = current_package_name(src)
    if os.path.exists(dest) and os.listdir(dest):
        sys.exit(f"{dest} already exists and is not empty")

    for folder, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(folder, src)
        target = dest if rel == "." else os.path.join(dest, rel)
        os.makedirs(target, exist_ok=True)
        for name in files:
            if name in SKIP_FILES or name.endswith(".pyc"):
                continue
            from_path = os.path.join(folder, name)
            to_path = os.path.join(target, name)
            if name.endswith((".dart", ".yaml", ".md")):
                text = open(from_path, encoding="utf-8").read().replace(old_name, args.name)
                with open(to_path, "w", encoding="utf-8") as f:
                    f.write(text)
            else:
                shutil.copy2(from_path, to_path)

    print(f"Created {dest}\n")
    print("Next steps:")
    print(f"  cd {dest}")
    print(f"  flutter create --org com.YOURNAME --project-name {args.name} .")
    print("  flutter pub get")
    print("  # edit assets/i18n/*.json (app_title + picture names), replace pictures,")
    print("  # then: python3 tools/validate_content.py && flutter test")


if __name__ == "__main__":
    main()

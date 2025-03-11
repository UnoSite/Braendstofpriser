"""Update the manifest file."""

import json
import os
import sys

def update_manifest():
    """Update the manifest file."""
    version = "0.0.0"
    manifest_path = None
    dorequirements = False

    # Parse arguments
    for index, value in enumerate(sys.argv):
        if value in ["--version", "-V"]:
            version = str(sys.argv[index + 1]).replace("v", "")
        if value in ["--path", "-P"]:
            manifest_path = str(sys.argv[index + 1])
        if value in ["--requirements", "-R"]:
            dorequirements = True

    if not manifest_path:
        sys.exit("Error: Missing path to manifest file")

    # Resolve correct file path
    repo_root = os.path.dirname(os.path.abspath(__file__))
    manifest_file = os.path.join(repo_root, manifest_path, "manifest.json")

    if not os.path.exists(manifest_file):
        sys.exit(f"Error: manifest.json not found at {manifest_file}")

    # Read manifest file
    with open(manifest_file, encoding="UTF-8") as manifestfile:
        manifest = json.load(manifestfile)

    # Update version
    manifest["version"] = version

    # Update requirements if requested
    if dorequirements:
        req_file = os.path.join(repo_root, "requirements.txt")
        if os.path.exists(req_file):
            with open(req_file, encoding="UTF-8") as file:
                new_requirements = [line.strip() for line in file if line.strip()]
            # Merge and remove duplicates
            manifest["requirements"] = list(set(manifest.get("requirements", []) + new_requirements))

    # Write back to manifest file
    with open(manifest_file, "w", encoding="UTF-8") as manifestfile:
        json.dump(manifest, manifestfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_manifest()

#!/bin/bash
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred. Exiting..."
    exit 1
}

trap handle_error ERR

# Get the current version
current_version=$(grep -o "__version__ = version = '[0-9.]*'" src/text2doc/_version.py | grep -o "[0-9.]*")
echo "Current version: $current_version"

# Increment the patch version
IFS='.' read -r major minor patch <<< "$current_version"
new_patch=$((patch + 1))
new_version="$major.$minor.$new_patch"

# Check if tag already exists, if so increment again
while git rev-parse "v$new_version" >/dev/null 2>&1; do
    echo "Tag v$new_version already exists, incrementing..."
    new_patch=$((new_patch + 1))
    new_version="$major.$minor.$new_patch"
done

echo "New version: $new_version"


# Update version in _version.py
./increment_version.py
./increment_setup.py

# Commit changes
echo "Publishing new version to GitHub..."
echo "Found version: $new_version"
echo ""
echo "Changes to be published:"
echo ""
git add .
git commit -m "Release version $new_version"
git tag "v$new_version"

# Push changes
echo "Pushing changes and tags to GitHub..."
git push origin main
git push origin "v$new_version"
echo "Successfully published version $new_version"

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ src/text2doc.egg-info/

# Upgrade build tools
echo "Upgrading build tools..."
python -m pip install --upgrade pip build twine setuptools wheel

# Build the package
echo "Building package..."
python setup.py sdist bdist_wheel

# Check the package
echo "Checking package..."
python -m twine check dist/*

# Publish to PyPI
echo "Publishing to PyPI..."
python -m twine upload dist/*

echo "Version $new_version has been released and published!"

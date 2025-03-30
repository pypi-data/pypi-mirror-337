rm -rf dist
uv build
twine upload dist/*
git add .
git commit -m "$1"
git push
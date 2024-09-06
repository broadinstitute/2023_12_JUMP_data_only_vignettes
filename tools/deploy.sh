#/usr/bin/env bash
jupytext --sync scripts/*.py &&
git config --global user.email quarto-github-actions-publish@example.com &&
git config --global user.name  Quarto_GHA_Runner &&
export QUARTO_PYTHON=$(which python) &&
quarto publish gh-pages &&
echo "Generating collab files" &&
git restore --source gh-pages -- "howto/*.ipynb" &&
python tools/insert_colab_cell.py &&
git add colab && git commit -m 'add colab files' && git push --force origin main:colab

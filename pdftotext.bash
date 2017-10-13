find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && find -name '*.pdf' -print0 | xargs -0 -n1 pdftotext -raw && pwd" \;

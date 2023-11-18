#!/usr/bin/bash

files=$(ls json_files)

for f in $files; do
    echo "$f: "
    # jq ".violations | length" "json_files/$f"
    # jq ".violations[].nodes[0].impact" "json_files/$f"

    # Check for all non-minor violations, and print the corresponding problematic HTML, a message, and the CSS target
    jq '.violations[] | select (.impact != "minor") | .nodes[] | .html, .none[].message, .any[].message, .all[].message, .target[]' "json_files/$f"
    echo -e "\n---\n"
done

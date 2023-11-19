#!/usr/bin/bash

files=$(ls json_files)

for f in $files; do
    #    echo "$f: "
    # jq ".violations | length" "json_files/$f"
    # jq ".violations[].nodes[0].impact" "json_files/$f"

    # Check for all non-minor violations, and print the corresponding problematic HTML, a message, and the CSS target
    #    jq '.violations[] | select (.impact != "minor") | .nodes[] | .html, .none[].message, .any[].message, .all[].message, .target[]' "json_files/$f"
    #    jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f
    echo -n "Number of elements in $f with sufficient colour contrast: "
    jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has sufficient" | wc -l
    echo -n "Number of elements in $f with insufficient colour contrast: "
    jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has insufficient" | wc -l
    echo -e "\n---\n"
done

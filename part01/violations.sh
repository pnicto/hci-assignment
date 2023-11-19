#!/usr/bin/bash

files=$(ls json_files)

jq '.passes[], .violations[] | .description' json_files/* | sort | uniq

for f in $files; do
    #    echo "$f: "
    # jq ".violations | length" "json_files/$f"
    # jq ".violations[].nodes[0].impact" "json_files/$f"

    # Check for all non-minor violations, and print the corresponding problematic HTML, a message, and the CSS target
    #    jq '.violations[] | select (.impact != "minor") | .nodes[] | .html, .none[].message, .any[].message, .all[].message, .target[]' "json_files/$f"
    #    jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f
    echo -n "Number of elements in $f with sufficient colour contrast: "
    suff=`jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has sufficient" | wc -l`
    echo $suff
    echo -n "Number of elements in $f with insufficient colour contrast: "
    insuff=`jq -r '.passes[], .violations[], .incomplete[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has insufficient" | wc -l`
    echo $insuff
    echo -n "The percentage of elements with sufficient colour contrast is "
    echo -e "$suff\t$insuff" | awk '{print 100 * $1/($1 + $2) "%"}'
    jq '.passes[] | .description, .id' json_files/$f | grep -q "document-title"
    if [[ $? -eq 0 ]]; then
        echo "The website has a title description."
    else
        echo "The website does not have a title description."
    fi
    echo -e "\n---\n"
done

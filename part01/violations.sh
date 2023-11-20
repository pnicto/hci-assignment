#!/usr/bin/bash

files=$(ls json_files)

# A list of all relevant tests performed by axe
jq '.passes[], .violations[] | .description' json_files/* | sort | uniq > text_files/tests.txt

for f in $files; do
    #    echo "$f: "

    # Checking colour contrast
    echo -n "Number of elements in $f with sufficient colour contrast: "
    suff=`jq -r '.passes[], .violations[]| .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has sufficient" | wc -l`
    echo $suff
    echo -n "Number of elements in $f with insufficient colour contrast: "
    insuff=`jq -r '.passes[], .violations[] | .nodes[] | select (.any[].id == "color-contrast") | select (.any[].message | match("sufficient")?) | .html, .target[], .any[].message' json_files/$f | grep "has insufficient" | wc -l`
    echo $insuff
    echo -n "The percentage of elements with sufficient colour contrast is "
    echo -e "$suff\t$insuff" | awk '{print 100 * $1/($1 + $2) "%"}'

    # Checking for title descriptions
    jq -e '.passes[] | select (.id == "document-title")' json_files/$f > /dev/null
    if [[ $? -eq 0 ]]; then
        echo "The website has a title description."
    else
        echo "The website does not have a title description."
    fi

    # Checking for restricted zooming
    jq -e '.passes[] | select (.id == "meta-viewport")' json_files/$f > /dev/null
    if [[ $? -eq 0 ]]; then
        echo "The website does not limit text scaling and zooming."
    else
        echo "The website limits text scaling and zooming."
    fi
    echo -e "\n---\n"
done

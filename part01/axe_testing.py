import os
import glob
import json
from selenium import webdriver
from axe_selenium_python import Axe


def test_accessibility(urls):
    # Create a directory for JSON files
    os.makedirs("json_files", exist_ok=True)

    # Instantiate the Chrome WebDriver
    with webdriver.Chrome() as driver:
        for url in urls:
            try:
                # Open the webpage
                driver.get(url)

                # Instantiate the Axe class
                axe = Axe(driver)

                # Inject axe-core javascript into page.
                axe.inject()

                # Run axe accessibility checks.
                results = axe.run()

                # Write results to file
                if len(results["violations"]) > 0:
                    axe.write_results(
                        results,
                        os.path.join(
                            "json_files",
                            f"accessibility_violations_{url.replace('://', '_').replace('/', '_')}.json",
                        ),
                    )
            except Exception as e:
                print(f"An error occurred while processing {url}: {str(e)}")


def write_violations_to_file():
    # Create a directory for text files
    os.makedirs("text_files", exist_ok=True)

    # Get all JSON files in the current directory
    json_files = glob.glob("json_files/*.json")

    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)

        # Extract the violations
        violations = data.get("violations", [])

        # Prepare the text to be written to the file
        text = ""
        for violation in violations:
            text += f"Violation ID: {violation['id']}\n"
            text += f"Description: {violation['description']}\n"
            text += f"Help: {violation['help']}\n"
            text += f"Help URL: {violation['helpUrl']}\n"
            text += f"Impact: {violation['impact']}\n"
            text += f"Tags: {', '.join(violation['tags'])}\n"
            text += "---\n"

        # Write the violations to a text file
        with open(
            os.path.join(
                "text_files",
                f"{os.path.splitext(os.path.basename(json_file))[0]}_violations.txt",
            ),
            "w",
        ) as f:
            f.write(text)


urls = [
    "https://www.usa.gov/",
    "https://www.usa.gov/es/",
    "https://www.isro.gov.in/",
    "https://www.isro.gov.in/ISRO_HINDI/",
    "https://medium.com/",
    "https://www.education.gov.in/",
    "https://www.education.gov.in/hi",  # "https://www.education.gov.in/en" is broken
    "https://nrega.nic.in/MGNREGA_new/Nrega_home.aspx",
    "https://nrega.nic.in/MGNREGA_new/NREGA_home_hi.aspx",  # "https://nrega.nic.in/Nregahome/MGNREGA_new/Nrega_home.aspx" is broken
    "https://www.bits-pilani.ac.in/",
]
test_accessibility(urls)
write_violations_to_file()

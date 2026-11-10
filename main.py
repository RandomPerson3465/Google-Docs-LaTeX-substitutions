import argparse
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from browser_profile import get_driver

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("import", "export", "clear"), help="The action (import, export, clear)")
    parser.add_argument("browser", type=str, help="The browser (chrome, firefox, or edge)")
    parser.add_argument("-p", "--profile", type=str, help="The profile to open (the FOLDER name)")
    parser.add_argument("-f", "--file", type=str, help="The file path to import from/export to")
    parser.add_argument("-u", "--user", type=int, help="The user number (0 for main account, 1 for first alt, etc.)")
    parser.add_argument("-d", "--ignore-duplicates", help="ignore duplicates", action="store_true")

    args = parser.parse_args()
    if (args.action in ["import", "export"] and args.file is None):
        print("file not specified")
        exit(1)

    if (args.file is not None):
        try:
            with open(args.file, "r", newline="", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            print("file not found")
            exit(1)

    print("Starting (this may take a few seconds...)")
    driver = get_driver(args.browser, args.profile)
    if driver is None:
        exit(1)

    driver.get(f"https://docs.google.com?authuser={0 if args.user is None else args.user}")

    wait = WebDriverWait(driver, 120)
    newdoc = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".docs-homescreen-templates-templateview.docs-homescreen-templates-templateview-showcase")))
    newdoc.click()

    wait = WebDriverWait(driver, 2)
    tools = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#docs-tools-menu")))
    tools.click()

    wait = WebDriverWait(driver, 2)
    prefs = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label=\"Preferences p\"]")))
    prefs.click()

    wait = WebDriverWait(driver, 2)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".javascriptMaterialdesignGm3WizTabsPrimary-tab")))
    prefs = driver.find_elements(By.CSS_SELECTOR, ".javascriptMaterialdesignGm3WizTabsPrimary-tab")[1]
    prefs.click()

    boxes = driver.find_elements(By.CSS_SELECTOR, "[jsname=vhZMvf]")
    box_iter = iter(boxes)
    if args.action == 'import':

        current_set = set()

        if args.ignore_duplicates:
            for i, box in enumerate(boxes[::2]):
                if i == 0: continue
                current_set.add(box.find_element(By.TAG_NAME, "input").get_attribute("value"))

        original_input = boxes[0]
        original_input_input = original_input.find_element(By.TAG_NAME, "input")
        replace_input = boxes[1]
        replace_input_input = replace_input.find_element(By.TAG_NAME, "input")

        try:
            with open(args.file, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                
                for entry in reader:
                    if (len(entry) != 2): raise ValueError("All rows must have 2 columns")
                    if (entry[0].strip() == "" or entry[1].strip() == ""): continue
                    if (args.ignore_duplicates and entry[0] in current_set): continue
                    current_set.add(entry[0])
                    original_input.click()
                    original_input_input.send_keys(entry[0].strip())
                    replace_input.click()
                    replace_input_input.send_keys(entry[1].strip())

                original_input.click()

                finish_button = driver.find_elements(By.CSS_SELECTOR, ".mdc-touch-target-wrapper")[1]
                finish_button.click()
        except FileNotFoundError:
            print("file not found")

    elif args.action == 'export':
        results = []
        for i, box1, box2 in enumerate(zip(box_iter, box_iter)):
            if i == 0: continue
            val1 = box1.find_element(By.TAG_NAME, "input").get_attribute("value")
            val2 = box2.find_element(By.TAG_NAME, "input").get_attribute("value")
            results.append([val1, val2])
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)

if __name__ == "__main__":
    main()
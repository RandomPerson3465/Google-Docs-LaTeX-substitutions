import argparse
import csv
import os
import sys
from dotenv import load_dotenv
from seleniumbase import sb_cdp

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("import", "export", "delete"), help="The action (import, export, clear)")
    parser.add_argument("-f", "--file", type=str, help="The file path to import from/export to")
    parser.add_argument("-d", "--ignore-duplicates", help="ignore duplicates", action="store_true")

    args = parser.parse_args()
    if (args.action in ["import", "export"] and args.file is None):
        print("file not specified")
        exit(1)

    if (args.file is not None and args.action in ["import", "delete"]):
        try:
            with open(args.file, "r", newline="", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            print("file not found")
            exit(1)

    sys.argv.append("--fast")
    driver = sb_cdp.Chrome(fast=True)
    print("Starting...")

    driver.goto("https://docs.google.com")
    if "email" in os.environ:
        driver.send_keys("[jsname=YPqjbf]", os.environ["email"] + "\n")

    if "password" in os.environ:
        driver.wait_for_element_visible("input[type=password]", timeout=60)
        driver.send_keys("input[type=password]", os.environ["password"] + "\n")

    driver.wait_for_element_visible(".docs-homescreen-templates-templateview.docs-homescreen-templates-templateview-showcase", timeout=10)
    driver.click(".docs-homescreen-templates-templateview.docs-homescreen-templates-templateview-showcase", timeout=5)
    driver.click("#docs-tools-menu")
    driver.wait_for_element_visible("[aria-label=\"Preferences p\"]", timeout=5)
    driver.click("[aria-label=\"Preferences p\"]")
    driver.wait_for_element_visible(".javascriptMaterialdesignGm3WizTabsPrimary-tab", timeout=5)
    driver.click_nth_visible_element(".javascriptMaterialdesignGm3WizTabsPrimary-tab", 2)

    boxes = driver.find_elements("[jsname=vhZMvf] input")
    box_iter = iter(boxes)
    if args.action == 'export':
        results = []
        for i, (box1, box2) in enumerate(zip(box_iter, box_iter)):
            if i == 0: continue
            val1 = box1.get_attribute("value")
            val2 = box2.get_attribute("value")
            results.append([val1, val2])
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)
    elif args.action == 'import':
        current_set = set()
        if args.ignore_duplicates:
            for i, box in enumerate(boxes[::2]):
                if i == 0: continue
                current_set.add(box.get_attribute("value"))
        try:
            with open(args.file, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for entry in reader:
                    if (len(entry) < 2): raise ValueError("All rows must have 2 columns")
                    if (entry[0].strip() == "" or entry[1].strip() == ""): continue
                    if (args.ignore_duplicates and entry[0] in current_set): continue
                    current_set.add(entry[0])
                    try:
                        boxes[0].send_keys(entry[0].strip(), fast=True)
                    except TypeError:
                        print(f"the string contains an incompatible unicode character: {entry[0]}")
                    try:
                        boxes[1].send_keys(entry[1].strip(), fast=True)
                    except TypeError:
                        print(f"the string contains an incompatible unicode character: {entry[1]}")
                driver.click(":nth-child(1 of .docsPreferencesDialogLabelAndTextField) input")
                driver.click_nth_visible_element(".mdc-touch-target-wrapper",2)
        except FileNotFoundError:
            print("file not found")
    elif args.action == 'delete':
        crosses = driver.find_elements("[jsname=nUV0Pd]")
        items_to_remove = set()
        try:
            with open(args.file, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for entry in reader:
                    if (len(entry) < 1): raise ValueError("All rows must have 1 column")
                    if (entry[0].strip() == ""): continue
                    items_to_remove.add(entry[0])
        except FileNotFoundError:
            print("file not found")
            exit(1)
        for box, cross in zip(boxes[-2:1:-2], crosses[::-1]):
            if (len(items_to_remove) == 0 or box.get_attribute("value") in items_to_remove):
                cross.click()
        driver.click_nth_visible_element(".mdc-touch-target-wrapper",2)

    input("Press Enter to close the window:")

if __name__ == '__main__':
    main()
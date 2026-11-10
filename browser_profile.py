import os
import platform
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException, SessionNotCreatedException
from selenium.webdriver.remote.webdriver import WebDriver

def get_driver(browser, profile_name="Default") -> WebDriver:
    try:
        browser = browser.lower()
        system = platform.system()
        home = Path.home()

        if system == "Windows":
            paths = {
                "chrome": Path(os.environ["LOCALAPPDATA"]) / "Google/Chrome/User Data",
                "edge": Path(os.environ["LOCALAPPDATA"]) / "Microsoft/Edge/User Data",
                "firefox": Path(os.environ["APPDATA"]) / "Mozilla/Firefox/Profiles"
            }

        elif system == "Darwin":
            paths = {
                "chrome": home / "Library/Application Support/Google/Chrome",
                "edge": home / "Library/Application Support/Microsoft Edge",
                "firefox": home / "Library/Application Support/Firefox"
            }

        elif system == "Linux":
            paths = {
                "chrome": home / ".config/google-chrome",
                "edge": home / ".config/microsoft-edge",
                "firefox": home / ".mozilla/firefox"
            }

        else:
            raise OSError(f"Unsupported operating system: {system}")

        if browser not in paths:
            raise ValueError("Browser must be chrome, edge, or firefox")

        profile_path = paths[browser]

        # Launch browser
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={profile_path}")
            options.add_argument(f"--profile-directory={profile_name}")
            return webdriver.Chrome(options=options)

        elif browser == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--start-maximized")
            options.add_argument(f"--user-data-dir={profile_path}")
            options.add_argument(f"--profile-directory={profile_name}")
            return webdriver.Edge(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.profile = profile_path / profile_name
            # options.add_argument("-profile")
            # options.add_argument(f"--user-data-dir={profile_path}")
            # options.add_argument(f"--profile-directory={profile_name}")
            return webdriver.Firefox(options=options)
    except (OSError,ValueError,FileNotFoundError) as e:
        print(e)
        return None
    except NoSuchDriverException:
        print("browser not installed")
        return None
    except SessionNotCreatedException:
        print("failed to start browser")
        return None
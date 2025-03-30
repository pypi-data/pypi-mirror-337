import warnings
import json
import urllib.request
from packaging import version

warnings.simplefilter("ignore")

__version__ = "1.1.2"  # Your package version

def check_for_update():
    try:
        # Query PyPI for the package data
        with urllib.request.urlopen("https://pypi.org/pypi/purdue-connect/json") as response:
            data = json.load(response)
        latest_version = data["info"]["version"]

        if version.parse(latest_version) > version.parse(__version__):
            red_bold = "\033[1;31m"
            reset = "\033[0m"
            print(
                f"\n{red_bold}New version available: {latest_version}. "
                "Please consider upgrading by running: pip install --upgrade purdue-connect"
                f"{reset}\n"
            )
    except Exception:
        # You might want to log the error in real-world use
        pass

# Run the update check when the package is imported
check_for_update()

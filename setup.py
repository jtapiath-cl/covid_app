import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--force", "-f", help = "Force full setup execution.", action = "store_true")
args = parser.parse_args()

from src import setup

if args.force:
    setup.main_function(True)
else:
    setup.main_function()
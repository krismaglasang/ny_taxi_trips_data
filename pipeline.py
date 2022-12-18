import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Just testing a list argument")
parser.add_argument('--url', nargs='+')
args = parser.parse_args()

print(args.url)
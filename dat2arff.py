import argparse
import os

SCRIPT_NAME = os.path.basename(__file__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="specify output file", metavar="file")
    parser.add_argument("dat_file", help="path to raw data file to convert to arff")
    args = parser.parse_args()

    file = args.dat_file
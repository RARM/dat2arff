import argparse
import os

SCRIPT_NAME = os.path.basename(__file__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="specify output file", metavar="file")
    parser.add_argument("-c", "--config", required=True, help="configuration file for the data", metavar="config_file")
    parser.add_argument("dat_file", help="path to raw data file to convert to arff")
    args = parser.parse_args()

    dat_filename = args.dat_file

def checkfile(filename):
    pass

def parse_conf(filename):
    pass
import argparse
import os

SCRIPT_NAME = os.path.basename(__file__)

def getyorn() -> bool:
    """Get a yes or not

    This function will read from stdin to check if the user gave a positive
    response (y or Y) or not (n or N). It will keep asking the user until they give
    a valid response.

    Returns
    -------
    bool
        It is True if the user gave a positive response and False if not.
    """
    ans = input()
    while (ans.lower() != 'y' or ans.lower() != 'n'):
        ans = input("Please, type 'y' or 'n':")

    return True if ans == 'y' else False

def tokenize(filename: str) -> list:
    """Get all the tokens from a file.

    Parameters
    ----------
    filename : str
        Path of the file to get tokens from.
    
    Returns
    -------
    list
        The array of tokens.
    """
    tokens = []

    with open(filename, 'r') as file:
        for line in file:
            for word in line.split():
                tokens.append(word)
            tokens.append("\n")
    
    return tokens


def parse_conf(filename: str):
    pass

class ConfParser:
    def __init__(self):
        pass
    
    def get_repr(self):
        pass

class ConfRepr:
    def __init__(self):
        pass

if __name__ == "__main__":
    # Set up and parse the program argument.
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="specify output file", metavar="file")
    parser.add_argument("-c", "--config", required=True, help="configuration file for the data", metavar="config_file")
    parser.add_argument("dat_file", help="path to raw data file to convert to arff")
    args = parser.parse_args()

    # Perform secondary argument checking.
    dat_filename = args.dat_file
    conf_filename = args.config
    output_filename = args.output if args.output else dat_filename + '.arff'
    checked = False

    if not os.path.exists(dat_filename):
        print('Error: The data file', dat_filename, 'does not exists.')
    elif not os.path.exists(conf_filename):
        print('Error: The config file', conf_filename, 'does not exists.')
    else:
        checked = True
    
    if (checked and os.path.exists(output_filename)):
        print('Warning: The output file exists. Do you want to replace it? [y/n]', end=' ')
        if not getyorn():
            print('ARFF file generation stopped. Provide a valid output file.')
            checked = False

    # Read configuration and data files.
    if checked:
        dat_tokens = tokenize(dat_filename)
        conf_tokens = tokenize(conf_filename)

    # Generate ARFF file.
import argparse
import os
import re

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
    while (ans.lower() != 'y' and ans.lower() != 'n'):
        ans = input("Please, type 'y' or 'n': ")

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

def parse_conf(tokens: list, output_file) -> list:
    """Parse config tokens, get attributes types, and writes ARFF header section.

    Parameters
    ----------
    tokens : list
        The list of tokens to parse.
    output_file : TextIOWrapper
        The opened output file.
        
    Returns
    -------
    list
        An array of strings with the attribute types per entries to expect.
    """
    parser = ConfParser(tokens, output_file)
    while parser.has_more_commands():
        parser.next()
    output_file.write("\n") # End of ARFF header section.
    return parser.get_repr()

class ConfParser:
    """Class used to parse the config file.

    Attributes
    ----------
    tokens : list
        The list of tokens to parse.
    i : int
        The index of the token currently reading.
    line : int
        The line number currently reading.
    output_file : TextIOWrapper
        The opened output file.
    error : bool
        State if there is an error reading tokens.
    repr : list
        Array of attribute types.

    Methods
    -------
    next() : None
        Read the next line.
    has_more_commands() : bool
        Check whether there are more commands to read.
    get_repr() : list
        Get an array of types expected in the dataset for all entries.

    """
    def __init__(self, tokens, output_file):
        """Initialize the configuration parser.

        tokens : list
            The list of tokens to parse.
        output_file : TextIOWrapper
            The opened output file.

        """
        self.tokens = tokens
        self.i = 0
        self.line = 0
        self.out = output_file
        self.error = False
        self.repr = []

    def has_more_commands(self):
        """Checks whether there are more commands to read."""
        return self.i < len(self.tokens) and not self.error

    def next(self):
        """Read the next line in the configuration parser."""
        token = self.tokens[self.i]
        if (self.i == 0):
            self.out.write('@relation ' + token + "\n\n")
            if self.tokens[1] != "\n":
                self.error = True
                print("Error: There was an unexpected token during the relation declaration (config file, line 1).")
        elif (token == "\n"):
            self.line += 1
        else: # Reading attributes.
            if (token == "numeric" and self.tokens[self.i + 1] != "\n"):
                self.repr.append(token)
                attr_type = token
                self.i += 1
                token = self.tokens[self.i]
                self.out.write('@attribute ' + token + ' ' + attr_type + "\n")
            else:
                self.error = True
                print("Error: Invalid attribute declaration in config file. Line", self.line + 1)
        self.i += 1
    
    def get_repr(self):
        """Get the attributes representation object."""
        return self.repr

class DataParser:
    """Module to parser the data using the given configuration.

    Attributes
    ----------
    tokens : list
        The list of tokens to parse.
    i : int
        The index of the token currently reading.
    line : int
        The line number currently reading.
    output_file : TextIOWrapper
        The opened output file.
    error : bool
        State if there is an error reading tokens.
    data : list
        Array of data entries.

    Methods
    -------
    has_more_data() : bool
        Check if there are more tokens to read and there is no error.
    next() : None
        Read the next entry.
    write_out() : None
        Write data to ARFF file.
    """
    def __init__(self, tokens: list, repr: list, output_file):
        """Initialize the data parser.

        Arguments
        ---------
        tokens : list
            Tokens to read.
        repr :  list
            Expected data types to read in entries.
        output_file : TextIOWrapper
            Opened file to write data in ARFF format.
        
        """
        self.tokens = tokens
        self.i = 0
        self.line = 0
        self.error = False
        self.repr = repr
        self.data = []
    
    def has_more_data(self):
        """Checks whether there are more commands to read."""
        return self.i < len(self.tokens) and not self.error
    
    def next(self):
        entry = []
        for dtype in self.repr:
            token = self.tokens[self.i]
            if (dtype == "numeric" and re.match(r"^-?\d+(\.\d+)?$", token)):
                entry.append(token)
            else:
                self.error = True
                print("Error: Invalid entry in the data file (line " + str(self.line + 1) + ").")
                break
            self.i += 1
        
        if (not self.error and self.tokens[self.i] != "\n"):
            self.error = True
            print("Error: Unexpected token in data file (line " + str(self.line + 1) + ").")
        
        if not self.error:
            self.data.append(entry)
            self.i += 1
            self.line += 1

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
        conf_tokens = tokenize(conf_filename)
        dat_tokens = tokenize(dat_filename)

    # Generate ARFF file.
    if checked:
        with open(output_filename, 'w') as output_file:
            data_repr = parse_conf(conf_tokens, output_file)
            data_parser = DataParser(dat_tokens, data_repr, output_file)
            while (data_parser.has_more_data()):
                data_parser.next()
            print("Data:", data_parser.data)
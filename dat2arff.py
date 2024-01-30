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
    return parser.get_repr(), parser.error

class ConfParser:
    """Class used to parse the config file.

    Attributes
    ----------
    tokens : list
        The list of tokens to parse.
    i : int
        The index of the token currently reading.
    current : string
        String represeting the current token.
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
    has_more_commands() : bool
        Check whether there are more commands to read.
    next() : None
        Read the next line.
    get_attr_vis(token: str) : str
        Get a string represting the visibility command of attribute.
    get_attr_type() : str
        Returns string representing the ARFF attribute type.
    get_next_token() : bool
        Updates current token (and index) checking it is not a new line.
    end_line() : bool
        Update current token to the first one of next line. Expect new line.
    get_create_expr() : dict
        Get the transformation condition.
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
        self.i = -1 # First call to get_next_token() will set it to 0.
        self.current = ''
        self.line = 0
        self.out = output_file
        self.error = False
        self.repr = []

    def has_more_commands(self):
        """Checks whether there are more commands to read."""
        return self.i + 1 < len(self.tokens) and not self.error

    def next(self):
        """Read the next line in the configuration file."""
        self.line += 1
        self.get_next_token()
        if (self.line == 1):
            self.out.write('@relation ' + self.current + "\n\n")
        else: # Reading attributes.
            attr_vis = self.get_attr_vis(self.current)
            attr_name = self.current if attr_vis == "keep" else self.current[1:]
            
            self.get_next_token()
            if self.error : return
            attr_type = self.get_attr_type()

            extra = ""
            if attr_vis == "create":
                self.get_next_token()
                extra = self.get_create_expr()
                if self.error: return
            elif attr_type == "nominal":
                self.get_next_token()
                extra = self.get_nominals()
                if self.error: return
            
            attr_repr = AttrRepr(attr_name, attr_vis, attr_type, extra)
            self.repr.append(attr_repr)
            
            self.out.write('@attribute ' + attr_name + ' ' + attr_type + "\n")
        self.end_line()

    def get_attr_vis(self, token: str):
        cmd = "keep"
        if (token[0] == "+"): cmd = "create"
        elif (token[0] == "-"): cmd = "hide"
        return cmd

    def get_attr_type(self):
        token = self.current.lower()
        if token != "numeric" and token != "nominals":
            self.error = True
            print("Error: Unknown attribute type in configuration file (line " + str(self.line) + ").")
            token = ""
        return token

    def get_next_token(self) -> None:
        if self.tokens[self.i + 1] == "\n":
            print("Error: Unexpected end of line in configuration file (line " + str(self.line) + ").")
            self.error = True
        else:
            self.i += 1
            self.current = self.tokens[self.i]

    def end_line(self) -> None:
        if self.tokens[self.i + 1] != "\n":
            print("Error: Unexpected token in configuration file (line " + str(self.line) + ")")
            self.error = True
        else:
            self.i += 1
            self.current = self.tokens[self.i]
    
    def get_create_expr(self) -> dict:
        token = self.current
        create_expr = {}

        # Getting tokens when transforming number to nominal.
        if re.match(r"^[a-zA-Z_]\w*([<>=]|<=|>=)[0-9]+(\.[0-9]+)?\?[a-zA-Z_]\w*:[a-zA-Z_]\w*$", token):
            end_of_comp_pos = re.search(r"\?", expr).start(0)
            
            comparison = expr[:end_of_comp_pos]
            results = expr[end_of_comp_pos + 1:]

            comp_op_reg = re.search(r"([<>=]|<=|>=)", comparison)
            comp_op = comp_op_reg.group(0)
            comp_op_pos = comp_op_reg.start(0)
            attr_name = comparison[:comp_op_pos]
            comp_to = comparison[comp_op_pos + 1:]

            res_sep_pos = re.search(r":", results).start(0)
            rit = results[:res_sep_pos]
            rif = results[res_sep_pos + 1:]

            create_expr = {
                "attr_name": attr_name,
                "comp_op": comp_op,
                "comp_to": comp_to,
                "if_true": rit,
                "if_false": rif
            }
        else:
            self.error = true
            print("Error: Invalid transformation expression in the configuration file (line " + str(self.line) + ").")
        return create_expr

    def get_nominals(self) -> list:
        nominals = []
        
        if re.match(r"^{[a-zA-Z_]\w*(,[a-zA-Z_]\w*)*}$", expr):
            nominals = expr[1:-1].split(',')
        else:
            self.error = True
            print("Error: Invalid declaration of nominals in configuration file (line " + str(self.line) + ").")
        return nominals

    def get_repr(self):
        """Get the attributes representation object."""
        return self.repr

class AttrRepr:
    def __init__(self, name: str, visibility: str, attr_type: str, extra: str):
        self.name = name
        self.visibility = visibility
        self.attr_type = attr_type
        self.extra = extra

class DataParser:
    """Module to parser the data using the given configuration.

    Attributes
    ----------
    tokens : list
        The list of tokens to parse.
    i : int
        The index of the token currently reading.
    current : str
        String representing the current token.
    line : int
        The line number currently reading.
    output_file : TextIOWrapper
        The opened output file.
    error : bool
        State if there is an error reading tokens.
    data : list
        Array of parsed data entries.

    Methods
    -------
    has_more_data() : bool
        Check if there are more tokens to read and there is no error.
    next() : None
        Read the next entry.
    get_next_token() : bool
        Updates current token (and index) checking it is not a new line.
    end_line() : bool
        Update current token to the first one of next line. Expect new line.
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
        self.i = -1
        self.current = ""
        self.line = 0
        self.error = False
        self.output_file = output_file
        self.repr = repr
        self.data = []
    
    def has_more_data(self):
        """Checks whether there are more commands to read."""
        return self.i + 1 < len(self.tokens) and not self.error
    
    def next(self):
        self.line +=1
        entry = []

        col = 0
        for attr_repr in self.repr:
            self.get_next_token()
            col += 1
            if attr_repr.visibility == 'create': continue
            elif attr_repr.attr_type == 'numeric': entry.append(self.get_num(col, attr_repr.name))
            elif attr_repr.attr_type == 'nominals': entry.append(self.get_nominal(attr_repr.extra, col, attr_repr.name))
        
        if not self.error:
            self.data.append(entry)
            self.end_line()

    def get_nominal(self, valid_nominals: list, col: int, attr_name: str):
        nominal = ''
        if self.current in valid_nominals: nominal = self.current
        else:
            self.error = True
            print("Error: Invalid nominal value '" + attr_name + "' in data file (line " + str(self.line) + "; element " + str(col) + ").")

    def get_num(self, col: int, attr_name: str):
        if re.match(r"^-?\d+$", self.current): return int(self.current)
        elif re.match(r"^-?\d+(?:\.\d+)?$", self.current): return float(self.current)
        else:
            self.error = True
            print("Error: Value '" + attr_name + "' in data file (line " + str(self.line) + ")")

    def get_next_token(self) -> None:
        if self.tokens[self.i + 1] == "\n":
            print("Error: Unexpected end of line in data file (line " + str(self.line) + ").")
            self.error = True
        else:
            self.i += 1
            self.current = self.tokens[self.i]

    def end_line(self) -> None:
        if self.tokens[self.i + 1] != "\n":
            print("Error: Unexpected token in data file (line " + str(self.line) + ")")
            self.error = True
        else:
            self.i += 1
            self.current = self.tokens[self.i]

    def write_out(self):
        print("Entries parsed:")
        print(self.data)

        # FIXME: Rewrite this section.
        # self.output_file.write("@data\n")
        # self.output_file.write("%\n% " + str(self.line) + " instances\n%\n")
        # for entry in self.data:
        #     self.output_file.write(', '.join(entry) + "\n")

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
            data_repr,err = parse_conf(conf_tokens, output_file)
            if not err:
                data_parser = DataParser(dat_tokens, data_repr, output_file)
                while (data_parser.has_more_data()):
                    data_parser.next()
                if not data_parser.error:
                    data_parser.write_out()
                print("ARFF file generated.")
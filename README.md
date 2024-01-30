# DAT2ARFF
The `dat2arff` Python script is a tool to convert raw data to the ARFF format
that the Weka tool can accept. This tool is under development and has limited
functionalities in preparing the ARFF format. Please read below for detailed
information on how to use it.

## Usage
Running the help flag (`-h` or `--help`) shows the most accurate and up-to-date
information on how to use this tool. You will find more details on using this
tool below.

```
$ python3 dat2arff.py -h
usage: dat2arff.py [-h] [-o file] -c config_file dat_file

positional arguments:
  dat_file              path to raw data file to convert to arff

optional arguments:
  -h, --help            show this help message and exit
  -o file, --output file
                        specify output file
  -c config_file, --config config_file
                        configuration file for the data
```

### Raw Data File `dat_file`
The purpose of this tool is to create files that conform to the [ARFF format](https://www.cs.waikato.ac.nz/~ml/weka/arff.html)
as specified in its documentation by the University of Waikato. This program
receives the raw data from a text file (the main required argument), where
values have blank spaces between columns and new lines between entries (rows).
For example, let's assume that some data has three entries where each record
holds four numbers. The raw data file would look like this:

```text
10 113 3 55 1700
13 102 2 37 1253
7  119 5 66 1963
```

The spaces between the columns can be one or more white spaces or tabs. However,
the program would recognize a new line as a new entry, expecting data in every
line. The program also checks that every entry has the proper number of values
(e.g., it will throw an error if one of the lines in the example file above has
more or less than five numbers).

### Configuration File `-c,--config config_file`
This prototype can only check for numbers and classes (not strings and dates
yet). However, the program needs a configuration file to know the types and
number of attributes. The configuration file is a text file where the first
line is the relation name, and the rest are the attribute declarations.

```text
relation_name
numeric val1
numeric val2
numeric val3
numeric val4
numeric val5
```

Like data files, the program doesn't care about extra spaces or tabs in
configuration files but expects a new command after every new line. And it
expects only attribute declarations after the relation name (the first line).
Every attribute declaration must first have the type declaration (`numeric` or
`class`).

#### Numeric
[Description.]

#### Class
[Description.]

## Features Roadmap
- [ ] Checks attribute types.
  - [x] Numeric.
  - [ ] Nominals.
  - [ ] Strings.
  - [ ] Dates.
  - [ ] Accepts unknown value (?).
- [ ] Perform data transformations.
  - [ ]  Basic Attributes manipulation.
    - [ ] Hide attributes.
    - [ ] Create attributes.
  - [ ] Conditional number-to-class transformation.
    - [ ] Simple two classes transformation.
  - [ ] Conditional class-to-number transformation.
    - [ ] Simple single class to two numbers transformation. (E.g., `nom>5?true:false`)
- [ ] Performs conditional basic type conversion.
  - [ ] Number to two classes.
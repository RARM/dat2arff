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
usage: dat2arff.py [-h] [-o file] dat_file

positional arguments:
  dat_file              path to raw data file to convert to arff

optional arguments:
  -h, --help            show this help message and exit
  -o file, --output file
                        specify output file
```

The purpose of this tool is to create files that conform to the [ARFF format](https://www.cs.waikato.ac.nz/~ml/weka/arff.html)
as specified in its documentation by the University of Waikato.
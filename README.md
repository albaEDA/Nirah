<img src="https://github.com/AaronKel/Nirah/raw/master/nirah.png" alt="Nirah" width="150" align="right">
<h1 align="center">
  Nirah
</h1>

<h4 align="center">Nirah is a project aimed at automatically wrapping verilator C++ models in python in order for high level, extendable control and verification of verilog systems.</h4>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/AaronKel/Nirah.svg)](https://github.com/AaronKel/Nirah/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
GCC 5+ (or 4+ with stdc++ libs linked)
Python 3.0+
Swig
Verilator
Nirah
```

### Installing

Currently Nirah is a standalone script but in future it will be a utility called from a command line. To get up and running the repository should act as a workspace to work as a testbed.

```
git clone https://github.com/AaronKel/Nirah.git
cd Nirah
python nirah.py RTL/sha256_rtl/sha256.v -O3 --verilator="-IRTL/sha256_rtl"
```
This will generate a wrapped libary that you can perform tests on. You will need to move the generated python file from obj_dir to TESTBENCH/sha256_tb aswell as the shared _sha256.o. An example of this is shown in the following:

```
mv obj_dir/sha256.py TESTBENCH/sha256_tb/
mv TESTBENCH/_sha256.so TESTBENCH/sha256_tb/
python TESTBENCH/sha256_tb/sha256_tb.py
```
view sha256_tb.py for VCD dumping code.


## Example
<img src="https://github.com/AaronKel/Nirah/raw/e4189df154ed1a72a64ef0d4a1f652b2dbac26af/nirah_autocomplete.gif" alt="Nirah" align="left">
<br>

The following GIF shows the heirachy autocompletion within Visual Code.
The ports are exposed as variables an can be written to the DUT as integers, however other forms of data can be handled natively by Python such as hex and binary values.

Nirah provides minimal support for arrays.

The project is in it's intial stages and can synthesize large designs, however there are bugs with tracing on some larger designs with work arounds already implimented
<br>
<br>
<br>
<br>
## Features
- [x] Trace dumping (VCD)

- [x] Coverage

- [x] Multi-dimensional Array

- [x] Command line args

  Use with --swig="...", --gcc="...", etc

- [x] Complex examples

  Added SHA256 example

- [ ] Multi-threaded. (Compiles but is slower than single threaded)

- [ ] Nirah library for verilog helper features

- [ ] Documentation

## Authors

* **Aaron Kelly** - *Initial work* - [AaronKel](https://github.com/AaronKel)

See also the list of [contributors](https://github.com/AaronKel/nirah/contributors) who participated in this project.

## Acknowledgments

* Inspiration from sin00b with [VerilatorGen.rb](https://github.com/sin00b/VerilatorGen.rb) a ruby wrapper for Verilator

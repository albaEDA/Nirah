&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/AaronKel/Nirah.svg)](https://github.com/AaronKel/Nirah/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

# Nirah
Nirah is a project aimed at automatically wrapping verilator C++ models in python in order for high level, extendable control and verification of verilog systems.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
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
python3 nirah.py up_counter.v
```
This will generate a wrapped libary that you can perform tests on an example of this is shown in the following:

```
python3 up_counter_tb.py
```

## Authors

* **Aaron Kelly** - *Initial work* - [AaronKel](https://github.com/AaronKel)

See also the list of [contributors](https://github.com/AaronKel/nirah/contributors) who participated in this project.

## Acknowledgments

* Inspiration from sin00b with [VerilatorGen.rb](https://github.com/sin00b/VerilatorGen.rb) a ruby wrapper for Verilator

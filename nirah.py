import os
import sys
import subprocess

import argparse

parser = argparse.ArgumentParser(
    description='Nirah is a project aimed at automatically wrapping \
                verilator C++ models in python in order for high level,\
                extendable control and verification of verilog systems.')
group = parser.add_mutually_exclusive_group()

parser.add_argument(
    'files',
    metavar='F',
    type=str,
    nargs='+',
    help='list of files to compile')

group.add_argument('-O0', action='store_true', help="No optimisations")
group.add_argument('-O1', action='store_true', help="Low optimisations")
group.add_argument('-O2', action='store_true', help="Medium optimisations")
group.add_argument('-O3', action='store_true', help="High optimisations")

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help="Enables verbrose/debugging to be printed")

parser.add_argument(
    '--verilator',
    type=str,
    help="Passes arguments to Verilator")

parser.add_argument(
    '--swig',
    type=str,
    default=1,
    help="Passes arguments to Swig")

parser.add_argument(
    '--gcc',
    type=str,
    default=1,
    help="Passes arguments to GCC")

args = parser.parse_args()

if args.O0:
    nirah_opt = " -O0"
elif args.O1:
    nirah_opt = " -O1"
elif args.O2:
    nirah_opt = " -O2"
elif args.O3:
    nirah_opt = " -O3"
else:
    nirah_opt = " -O0"

OBJ_DIR = "./obj_dir"
ORG_PATH = os.getcwd()

verilator_root = str(subprocess.check_output("verilator -V  \
| grep VERILATOR_ROOT", shell=True), 'utf-8').rstrip("\n").split("\n")

verilator_root_default = verilator_root[0].split(" = ")[1]
verilator_root_enviroment = verilator_root[1].split(" = ")[1]

if verilator_root_enviroment == "":
    verilator_root = verilator_root_default
else:
    verilator_root = verilator_root_enviroment

verilator_files = " ".join(args.files)
verilator_args = args.verilator
verilator_args += nirah_opt

cmd = "verilator -Wno-fatal --cc {VERILATOR_FILES} {VERILATOR_ARGS}".format(
    VERILATOR_FILES=verilator_files, VERILATOR_ARGS=verilator_args)

if args.debug:
    print(cmd)

os.system(cmd)
for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "mk":
            if not files.endswith("_classes.mk"):
                vmkfile = files
    except BaseException:
        pass

top_mod = vmkfile.lstrip("V").rstrip(".mk")
WRAP_CPP = "{}.cpp".format(top_mod)

os.chdir(OBJ_DIR)
os.system(
    'CPPFLAGS=\"-fPIC {NIRAH_OPT}\" make -f {MAKEFILE}'.format(
        NIRAH_OPT=nirah_opt,
        MAKEFILE=vmkfile))
os.chdir(ORG_PATH)

vincs_basename = ""
vincs_relative = ""

for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "h":
            if files.endswith("unit.h") is False:
                vincs_basename += "#include \"{}\"\n".format(files)
                vincs_relative += "%include \"./obj_dir/{}\"\n".format(files)
    except BaseException:
        pass

submodule_tracing = ""
for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "h":
            if "_" in files and "__" not in files:
                submodule_tracing += "%ignore " + \
                    files.split(".")[0] + "::" + "trace;\n"
                submodule_tracing += "%ignore " + \
                    files.split(".")[0] + "::" + "traceInit;\n"
                submodule_tracing += "%ignore " + \
                    files.split(".")[0] + "::" + "traceFull;\n"
                submodule_tracing += "%ignore " + \
                    files.split(".")[0] + "::" + "traceChg;\n"
    except BaseException:
        pass

swig_src = """%module {}

%include stdint.i
%include "carrays.i"
%include "cpointer.i"
%pointer_functions(uint_fast16_t, pointer)

%inline %{{
static void set_array(uint_fast16_t *ary, int index, unsigned long value) {{
    ary[index] = value;
}}
%}}

%inline %{{
static unsigned long get_array(uint_fast16_t *ary, int index) {{
    return ary[index];
}}
%}}

%{{
#define SWIG_FILE_WITH_INIT 1
#include "verilatedos.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include "verilated_cov.h"
{}
%}}

%ignore _Vbit;
%ignore _VERILATEDOS_H_;
%ignore _VERILATED_H_;
%ignore _VERILATED_VCD_C_H_;
%ignore _VERILATED_COV_H_;
%ignore Verilated::getCommandArgs();
%ignore Verilated::commandArgsPlusMatch;
%ignore Verilated::commandArgsAdd;
%ignore Verilated::commandArgs;
%ignore sc_time_stamp();
{}

%define __restrict %enddef

%include "verilatedos.h"
%include "verilated.h"
%include "verilated_vcd_c.h"
%include "verilated_cov.h"
{}""".format(top_mod,
             vincs_basename,
             submodule_tracing,
             vincs_relative)

fp = open("{}.i".format(top_mod), "w")
fp.write(swig_src)
fp.close()

incdir_opt = " -I{}/include -I{}/include/vltstd -I{}".format(verilator_root,
                                                             verilator_root,
                                                             OBJ_DIR)

PYTHON_LD = str(
    subprocess.check_output(
        "python3-config --cflags",
        shell=True),
    'utf-8').split()[0].lstrip("-I")

swig_cmd = "swig -python -c++ {} -I{} -I{} -o {}/{} -w509 -w451 {}.i".format(
    incdir_opt, PYTHON_LD, verilator_root, OBJ_DIR, WRAP_CPP, top_mod)

if args.debug:
    print(swig_cmd)

os.system(swig_cmd)
if not os.path.exists("TESTBENCH"):
    os.mkdir("TESTBENCH")

objs = ["{}/include/verilated.cpp".format(verilator_root),
        "{}/{}.cpp".format(OBJ_DIR, top_mod),
        "{}/V{}__ALL.a".format(OBJ_DIR, top_mod),
        "{}/include/verilated_vcd_c.cpp".format(verilator_root),
        "{}/include/verilated_cov.cpp".format(verilator_root)]

gcc_cmd = """
gcc -shared -std=c++11 -o TESTBENCH/_{TOP_MOD}.so \
{OBJ_0} \
{OBJ_1} \
{OBJ_2} \
{OBJ_3} \
{OBJ_4} \
-L. \
-L/usr/lib/x86_64-linux-gnu \
-Wl,-Bsymbolic-functions -fPIC \
-I{VERILATOR_ROOT}/include \
-I{VERILATOR_ROOT}/include/vltstd \
-I{OBJ_DIR} \
-I{PYTHON_LD} \
-l:{OBJ_2} \
-lstdc++ -lgmp -ldl -lcrypt -lm -lc
""".format(TOP_MOD=top_mod,
           OBJ_0=objs[0],
           OBJ_1=objs[1],
           OBJ_2=objs[2],
           OBJ_3=objs[3],
           OBJ_4=objs[4],
           VERILATOR_ROOT=verilator_root,
           OBJ_DIR=OBJ_DIR,
           PYTHON_LD=PYTHON_LD)

if args.debug:
    print(gcc_cmd)

os.system(gcc_cmd)

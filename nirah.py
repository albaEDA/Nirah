import os
import sys
import subprocess

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

cmd = "verilator -Wno-fatal --trace --cc {} -I./RTL".format(sys.argv[1])
os.system(cmd)
for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "mk":
            if not files.endswith("_classes.mk"):
                vmkfile = files
    except:
        pass

top_mod = vmkfile.lstrip("V").rstrip(".mk")
WRAP_CPP = "{}.cpp".format(top_mod)

os.chdir(OBJ_DIR)
os.system('CPPFLAGS=\"-fPIC\" make -f {}'.format(vmkfile))
os.chdir(ORG_PATH)

vincs_basename = ""
vincs_relative = ""

for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "h":
            if files.endswith("unit.h") == False:
                vincs_basename += "#include \"{}\"\n".format(files)
                vincs_relative += "%include \"./obj_dir/{}\"\n".format(files)
    except:
        pass

submodule_tracing = ""
for files in os.listdir(OBJ_DIR):
    try:
        if files.split(".")[1] == "h":
            if "_" in files and "__" not in files:
                submodule_tracing += "%ignore " + files.split(".")[0] + "::" + "trace;\n"
                submodule_tracing += "%ignore " + files.split(".")[0] + "::" + "traceInit;\n"
                submodule_tracing += "%ignore " + files.split(".")[0] + "::" + "traceFull;\n"
                submodule_tracing += "%ignore " + files.split(".")[0] + "::" + "traceChg;\n"
    except:
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

PYTHON_LD = str(subprocess.check_output("python3-config --cflags", shell=True), 'utf-8').split()[0].lstrip("-I")

swig_cmd = "swig -python -c++ {} -I{} -I{} -o {}/{} -w509 -w451 {}.i".format(incdir_opt,
                                                                             PYTHON_LD,
                                                                             verilator_root,
                                                                             OBJ_DIR,
                                                                             WRAP_CPP,
                                                                             top_mod)

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
gcc -shared -std=c++11 -o TESTBENCH/_{}.so \
{} \
{} \
{} \
{} \
{} \
-L. \
-L/usr/lib/x86_64-linux-gnu \
-Wl,-Bsymbolic-functions -fPIC \
-I{}/include \
-I{}/include/vltstd \
-I{} \
-I{} \
-l:{} \
-lstdc++ -lgmp -ldl -lcrypt -lm -lc
""".format(top_mod,
           objs[0],
           objs[1],
           objs[2],
           objs[3],
           objs[4],
           verilator_root,
           verilator_root,
           OBJ_DIR,
           PYTHON_LD,
           objs[2])

print(gcc_cmd)
os.system(gcc_cmd)
os.system("cp obj_dir/{}.py TESTBENCH/".format(top_mod))

import counter

top = counter.Vcounter()

main_time = 0
counter.Verilated_traceEverOn(True)

VCD = counter.VerilatedVcdC()
top.trace(VCD, 99)
VCD.open("counter_dump.vcd")


def clk_toggle(n=1):
    for _ in range(n):
        top.clk = 0
        top.eval()
        top.clk = 1
        top.eval()


top.enable = 1

for i in range(100):
    clk_toggle()
    print(top.out)

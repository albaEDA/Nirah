import counter

top = counter.Vcounter()

main_time = 0
counter.Verilated_traceEverOn(True)

VCD = counter.VerilatedVcdC()
top.trace(VCD, 99)
VCD.open("counter_dump.vcd")


def clk_toggle(n=1):
    global main_time
    for _ in range(n):
        top.clk = 0
        top.eval()
        main_time += 1
        VCD.dump(main_time)
        top.clk = 1
        top.eval()
        main_time += 1
        VCD.dump(main_time)


top.enable = 1

for i in range(100):
    clk_toggle()
    print(top.out)

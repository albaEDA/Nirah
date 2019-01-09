import counter

top = counter.Vcounter()


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

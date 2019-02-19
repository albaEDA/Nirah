import sha256

sha256_top = sha256.Vsha256()

#main_time = 0
#sha256.Verilated_traceEverOn(True)

#sha256_VCD = sha256.VerilatedVcdC()
#sha256_top.trace(sha256_VCD, 99)
#sha256_VCD.open("sha256_dump.vcd")

def clk_toggle(n=1):
    global main_time
    for i in range(n):
        sha256_top.clk = 0
        sha256_top.eval()
        #main_time += 1
        #sha256_VCD.dump(main_time)
        sha256_top.clk = 1
        sha256_top.eval()
        #main_time += 1
        #sha256_VCD.dump(main_time)


def data_chunker(data, width, chunk):
    data_bin = bin(data)[2:].zfill(512)
    data_chunk = data_bin[width*chunk:width*(chunk+1)]
    return int(data_chunk, 2)


def init_sim():
    sha256_top.clk = 0
    sha256_top.reset_n = 0
    sha256_top.cs = 0
    sha256_top.we = 0
    sha256_top.address = 0
    sha256_top.write_data = 0


def reset_dut():
    sha256_top.reset_n = 0
    clk_toggle(4)
    sha256_top.reset_n = 1


def write_word(address, word):
    #print("Writing {} to {}".format(hex(word), hex(address)))
    sha256_top.address = address
    sha256_top.write_data = word
    sha256_top.cs = 1
    sha256_top.we = 1
    clk_toggle(1)
    sha256_top.cs = 0
    sha256_top.we = 0


def write_block(block_data):
    for i in range(0, 16):
        write_word(16+i, data_chunker(block_data, 32, i))


def read_word(address):
    sha256_top.address = address
    sha256_top.cs = 1
    sha256_top.we = 0
    clk_toggle(1)
    data = sha256_top.read_data
    sha256_top.cs = 0
    #print("Read {} from {}".format(hex(data), hex(address)))
    return data


def read_digest():
    read_word(int('20', 16))
    read_word(int('21', 16))
    read_word(int('22', 16))
    read_word(int('23', 16))
    read_word(int('24', 16))
    read_word(int('25', 16))
    read_word(int('26', 16))
    read_word(int('27', 16))


def wait_ready():
    while read_word(int('9', 16)) != 3:
        clk_toggle()


def single_block_test(block_data):

    write_block(block_data)

    write_word(int('8', 16), (int('5', 16)))

    wait_ready()
    read_digest()


block_data = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018

init_sim()
reset_dut()

for i in range(10000):
    single_block_test(block_data)

#sha256.VerilatedCov.write("sha256.dat")

module up_counter (
  input         enable, 
  input         clk,
  input         reset,
  output [7:0]  out
);

  logic [7:0]   out;

  always @(posedge clk)
  if (reset) begin
    out <= 8'b0 ;
  end else if (enable) begin
    out <= out + 1;
  end

endmodule 
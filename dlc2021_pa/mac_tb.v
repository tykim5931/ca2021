`timescale 1ns/1ns

module mac_tb ;
  
  reg clk,reset;
  
  always begin
    clk = 0; #25;
    clk = 1; #25;
  end

  always @ (negedge clk) begin
    if(reset ==1)
      reset = 0;	#100
    else
      reset = 1;	#100;
  end
  
  // for testing 4-bit mac 
  reg [3:0] in4, w4;
  reg ds_in4, ds_w4;
  wire [7:0] mac4_out;
  
  // submodule 4 mac 
  mac MAC4 (
    .K(4)
    .mac_out(mac4_out),
    .in(in4),
    .w(w4),
    .data_strobe_in(ds_in4),
    .data_strobe_w(ds_w4),
    .clk(clk),
    .reset(reset)
  ) ;
  
  initial begin
    in4=4'b0001; w4=4'b0001; ds_in4=0; ds_w4=0; #50;
    in4=4'b0010; w4=4'b0001; ds_in4=0; ds_w4=1; #50;
	in4=4'b0011; w4=4'b0001; ds_in4=1; ds_w4=0; #50;
    in4=4'b0100; w4=4'b0001; ds_in4=0; ds_w4=1; #50;
    
    in4=4'b0101; w4=4'b0010; ds_in4=1; ds_w4=1; #50;
    in4=4'b0110; w4=4'b0010; ds_in4=1; ds_w4=1; #50;
	in4=4'b0100; w4=4'b0010; ds_in4=1; ds_w4=0; #50;
    in4=4'b1000; w4=4'b0010; ds_in4=0; ds_w4=0; #50;
  end
  
  
  // for testing 8-bit mac 
  reg [7:0] in8, w8;
  reg ds_in8, ds_w8;
  wire [15:0] mac8_out;
  
  // submodule 8 mac 
  mac MAC8(
    .K(8)
    .mac_out(mac8_out),
    .in(in8),
    .w(w8),
    .data_strobe_in(ds_in8),
    .data_strobe_w(ds_w8),
    .clk(clk),
    .reset(reset)
  );

  initial begin
    in8=8'b0001; w8=8'b0001; ds_in8=0; ds_w8=0; #50;
    in8=8'b0010; w8=8'b0001; ds_in8=0; ds_w8=1; #50;
	in8=8'b0011; w8=8'b0001; ds_in8=1; ds_w8=0; #50;
    in8=8'b0100; w8=8'b0001; ds_in8=0; ds_w8=1; #50;
    
    in8=8'b0101; w8=8'b0010; ds_in8=1; ds_w8=1; #50;
    in8=8'b0110; w8=8'b0010; ds_in8=1; ds_w8=1; #50;
	in8=8'b0100; w8=8'b0010; ds_in8=1; ds_w8=0; #50;
    in8=8'b1000; w8=8'b0010; ds_in8=0; ds_w8=0; #50;
    
    in8=8'b1011; w8=8'b0001; ds_in8=0; ds_w8=0; #50;
    in8=8'b1010; w8=8'b0001; ds_in8=0; ds_w8=1; #50;
	in8=8'b1111; w8=8'b0001; ds_in8=1; ds_w8=0; #50;
    in8=8'b0100; w8=8'b0001; ds_in8=0; ds_w8=1; #50;
    
    in8=8'b0101; w8=8'b0010; ds_in8=1; ds_w8=1; #50;
    in8=8'b1110; w8=8'b0010; ds_in8=1; ds_w8=1; #50;
	in8=8'b1100; w8=8'b0010; ds_in8=1; ds_w8=0; #50;
    in8=8'b1100; w8=8'b0010; ds_in8=0; ds_w8=0; #50;
  end
  
  
  // for testing 32-bit mac 
  reg [31:0] in32, w32;
  reg ds_in32, ds_w32;
  wire [63:0] mac32_out;
  
  // submodule 32 mac 
  mac MAC32(
    .K(32)
    .mac_out(mac32_out),
    .in(in32),
    .w(w32),
    .data_strobe_in(ds_in32),
    .data_strobe_w(ds_w32),
    .clk(clk),
    .reset(reset)
  );

  initial begin
    integer i;
    for(i=0; i<64/4; i =i + 1) begin
    	in32=32'b0101; w32=32'b0101; ds_in32=0; ds_w32=0; #50;
    	in32=32'b0101; w32=32'b0101; ds_in32=0; ds_w32=1; #50;
      	in32=32'b0101; w32=32'b0101; ds_in32=1; ds_w32=0;#50;
      	in32=32'b0101; w32=32'b0101; ds_in32=1; ds_in32=1; #50;
    end
  end
        
        
  initial begin
   $dumpfile("mac.vcd");
   $dumpvars;
  end
  
endmodule
  


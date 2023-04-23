module mac(in, w, data_strobe_in, data_strobe_w, clk, 
			reset, mac_out);
  
  // parameters
  parameter K 			= 4 ;
  parameter IDLE  		= 2'b000 ;
  parameter WAIT_IN	 	= 2'b001 ;
  parameter WAIT_W 		= 2'b010 ;
  parameter MAC  		= 2'b011 ;
  
  parameter BUSY		= 1 ;
  parameter NOT_BUSY	= 0 ;
  
  // input output declartion			
  input 	[K-1:0]	 	in, w;
  input 				data_strobe_in, data_strobe_w;
  input					clk, reset;	// for setting sequential
  output reg [2K-1:0] 	mac_out;  
  
  reg					counter ;	// for counting added layer
  reg					busy_flag ;	// busy flag
  reg 		 [1:0] 		state_Next, state ;	// for setting flag
  reg signed [K-1:0]	reg_in, reg_w ;
  reg signed [2K-1:0] 	reg_mul, reg_out;
  
  // Count till threshold
  always @ (negedge clk) begin
    if (reset)
		counter <= K ;
    else if (counter == K)
      if (data_strobe_in & data_strobe_w)
        	counter <= 1 ;
    	else
			counter <= 0 ;
    else if (state == MAC)
          counter <= counter + 1 ;
  end
  
  always@(posedge clk )	// update state every positive edge of clock.
    begin
      if(reset)
          state <= IDLE ;
      else
          state <= state_Next ;
    end
    
  // Always update state 
  always @ (*) begin
    if(state == MAC)
      busy_flag = BUSY;
    else
      busy_flag = NOT_BUSY;
  end
    
  always @ (*) begin
    case(state)
      IDLE : if (data_strobe_in & data_strobe_w) begin
				state_Next = MAC ;
      		 end
      		 // If Input is ready but not weight, then wait.
      		 else if (data_strobe_in) 
                state_Next = WAIT_W ; 
      		 // If weight is ready but not input, then wait.
      		 else if (data_strobe_w) 
			   state_Next = WAIT_IN ; 
      		 // If both of inputs are not ready, then stay in IDLE
      		 else begin   
               state_Next = IDLE ;
		
        WAIT_IN : if(data_strobe_in) begin
                    // if waited input is ready, then start mac.
                    state_Next = MAC ;
      			  end
                  else begin// Input is not ready yet, then stick with wait.
                    state_Next = WAIT_IN ;
                  end
				 
        WAIT_W : if(data_strobe_w) begin
          			// if waited input is ready, then start mac.
		          	state_Next = MAC ;
        		 end
				 else begin// Input is not ready
                   	state_Next = WAIT_W ;
                 end
		
        MAC : if(data_strobe_in & data_strobe_w) 
				 state_Next = MAC ; 
				 else if(data_strobe_in)
					state_Next = WAIT_IN ;
				 else if(data_strobe_w)
					state_Next = WAIT_W ;
				 else 
                   	state_Next = IDLE ;
		default : 
          state_Next = IDLE ;
      endcase
  end
  
  //===============1st Sequential Circuit for feeding input=========================
      
  always @(posedge clk) begin	// if input is ready, put it to input register
    if(data_strobe_in)
		reg_in <= in ;
  end
  
  always @(posedge clk) begin	// if input is ready, put it to input register
    if(data_strobe_w)
      reg_w <= w ;
  end
  
  always @(negedge clk)	// This holds multiplied result.
    begin
      if(reset)
        reg_mult <= 0 ;
      else if(counter == K)	
		if(data_strobe_in & data_strobe_w)
		reg_mult <= reg_in * reg_w ;
		else
		reg_mult <= 0 ;
      else if(state == MAC)	// If the unit is in MAC state, do adding to prev output
		reg_mult <= reg_mult + (reg_a*reg_b) ;
    end
  
  //================================================================================
      
      
  //=================2nd Sequential circuit for pushing output.=====================
  always@(posedge clk)	// in positive edge of clock, update output!!
     begin
       if(counter >= 1 && counter <= K)
         reg_out <= reg_mult ;
     end

  always@(posedge clk)	// If adding is done, then open output port
    begin
      if(counter == K)
        out_sig <= 1 ;
      else
		out_sig <= 0 ;
    end
  
  always@(posedge clk)	  // output port
    begin
      if(out_sig)
        mac_out <= reg_out ;
    end
   //===============================================================================
      
endmodule
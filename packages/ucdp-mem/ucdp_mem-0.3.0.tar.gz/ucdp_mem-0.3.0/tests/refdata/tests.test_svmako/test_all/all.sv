// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
//
//  MIT License
//
//  Copyright (c) 2024-2025 nbiotcloud
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
// =============================================================================
//
// Module:     tests.all
// Data Model: tests.test_svmako.AllMod
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all();



  // ------------------------------------------------------
  //  tests.all_otp0: u_otp0
  // ------------------------------------------------------
  all_otp0 u_otp0 (
    .main_clk_i     (1'b0               ), // TODO - Clock
    .main_rst_an_i  (1'b0               ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0               ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(99) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0               ), // TODO - Memory Write Enable
    .io_main_wdata_i(8'h00              ), // TODO - Memory Write Data
    .io_main_rdata_o(                   )  // TODO - Memory Read Data
  );


  // ------------------------------------------------------
  //  tests.all_otp1: u_otp1
  // ------------------------------------------------------
  all_otp1 u_otp1 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(1023) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_main_wdata_i(64'h0000000000000000 ), // TODO - Memory Write Data
    .io_main_rdata_o(                     )  // TODO - Memory Read Data
  );


  // ------------------------------------------------------
  //  tests.all_rom0: u_rom0
  // ------------------------------------------------------
  all_rom0 u_rom0 (
    .main_clk_i     (1'b0               ), // TODO - Clock
    .main_rst_an_i  (1'b0               ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0               ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(99) {1'b0}}), // TODO - Memory Address
    .io_main_rdata_o(                   ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0               )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_rom1: u_rom1
  // ------------------------------------------------------
  all_rom1 u_rom1 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(1023) {1'b0}}), // TODO - Memory Address
    .io_main_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_rom2: u_rom2
  // ------------------------------------------------------
  all_rom2 u_rom2 (
    .main_clk_i    (1'b0                 ), // TODO - Clock
    .main_rst_an_i (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_one_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_one_addr_i ({$clog2(1023) {1'b0}}), // TODO - Memory Address
    .io_one_rdata_o(                     ), // TODO - Memory Read Data
    .io_two_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_two_addr_i ({$clog2(3071) {1'b0}}), // TODO - Memory Address
    .io_two_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_main_pwr_i(1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_rom3: u_rom3
  // ------------------------------------------------------
  all_rom3 u_rom3 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(4095) {1'b0}}), // TODO - Memory Address
    .io_main_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_one_pwr_i  (1'b0                 ), // TODO - Enable
    .pwr_two_pwr_i  (1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_rom4: u_rom4
  // ------------------------------------------------------
  all_rom4 u_rom4 (
    .main_clk_i    (1'b0                  ), // TODO - Clock
    .main_rst_an_i (1'b0                  ), // TODO - Async Reset (Low-Active)
    .io_one_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_one_addr_i ({$clog2(4095) {1'b0}} ), // TODO - Memory Address
    .io_one_rdata_o(                      ), // TODO - Memory Read Data
    .io_two_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_two_addr_i ({$clog2(16383) {1'b0}}), // TODO - Memory Address
    .io_two_rdata_o(                      ), // TODO - Memory Read Data
    .pwr_one_pwr_i (1'b0                  ), // TODO - Enable
    .pwr_two_pwr_i (1'b0                  )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_rom5: u_rom5
  // ------------------------------------------------------
  all_rom5 u_rom5 (
    .main_clk_i     (1'b0                  ), // TODO - Clock
    .main_rst_an_i  (1'b0                  ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(10239) {1'b0}}), // TODO - Memory Address
    .io_main_rdata_o(                      ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0                  )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram0: u_ram0
  // ------------------------------------------------------
  all_ram0 u_ram0 (
    .main_clk_i     (1'b0               ), // TODO - Clock
    .main_rst_an_i  (1'b0               ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0               ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(99) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0               ), // TODO - Memory Write Enable
    .io_main_wdata_i(8'h00              ), // TODO - Memory Write Data
    .io_main_rdata_o(                   ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0               )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram1: u_ram1
  // ------------------------------------------------------
  all_ram1 u_ram1 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(1023) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_main_wdata_i(64'h0000000000000000 ), // TODO - Memory Write Data
    .io_main_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram2: u_ram2
  // ------------------------------------------------------
  all_ram2 u_ram2 (
    .main_clk_i    (1'b0                 ), // TODO - Clock
    .main_rst_an_i (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_one_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_one_addr_i ({$clog2(1023) {1'b0}}), // TODO - Memory Address
    .io_one_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_one_wdata_i(64'h0000000000000000 ), // TODO - Memory Write Data
    .io_one_rdata_o(                     ), // TODO - Memory Read Data
    .io_two_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_two_addr_i ({$clog2(3071) {1'b0}}), // TODO - Memory Address
    .io_two_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_two_wdata_i(64'h0000000000000000 ), // TODO - Memory Write Data
    .io_two_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_main_pwr_i(1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram3: u_ram3
  // ------------------------------------------------------
  all_ram3 u_ram3 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(4095) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_main_wdata_i(16'h0000             ), // TODO - Memory Write Data
    .io_main_rdata_o(                     ), // TODO - Memory Read Data
    .pwr_one_pwr_i  (1'b0                 ), // TODO - Enable
    .pwr_two_pwr_i  (1'b0                 )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram4: u_ram4
  // ------------------------------------------------------
  all_ram4 u_ram4 (
    .main_clk_i    (1'b0                  ), // TODO - Clock
    .main_rst_an_i (1'b0                  ), // TODO - Async Reset (Low-Active)
    .io_one_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_one_addr_i ({$clog2(4095) {1'b0}} ), // TODO - Memory Address
    .io_one_wena_i (1'b0                  ), // TODO - Memory Write Enable
    .io_one_wdata_i(16'h0000              ), // TODO - Memory Write Data
    .io_one_rdata_o(                      ), // TODO - Memory Read Data
    .io_two_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_two_addr_i ({$clog2(16383) {1'b0}}), // TODO - Memory Address
    .io_two_wena_i (1'b0                  ), // TODO - Memory Write Enable
    .io_two_wdata_i(16'h0000              ), // TODO - Memory Write Data
    .io_two_rdata_o(                      ), // TODO - Memory Read Data
    .pwr_one_pwr_i (1'b0                  ), // TODO - Enable
    .pwr_two_pwr_i (1'b0                  )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram5: u_ram5
  // ------------------------------------------------------
  all_ram5 u_ram5 (
    .main_clk_i     (1'b0                  ), // TODO - Clock
    .main_rst_an_i  (1'b0                  ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                  ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(10239) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0                  ), // TODO - Memory Write Enable
    .io_main_wdata_i(18'h00000             ), // TODO - Memory Write Data
    .io_main_rdata_o(                      ), // TODO - Memory Read Data
    .pwr_main_pwr_i (1'b0                  )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram7: u_ram7
  // ------------------------------------------------------
  all_ram7 u_ram7 (
    .main_clk_i     (1'b0                ), // TODO - Clock
    .main_rst_an_i  (1'b0                ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(127) {1'b0}}), // TODO - Memory Address
    .io_main_wena_i (1'b0                ), // TODO - Memory Write Enable
    .io_main_wdata_i(64'h0000000000000000), // TODO - Memory Write Data
    .io_main_rdata_o(                    ), // TODO - Memory Read Data
    .io_main_sel_i  (8'h00               ), // TODO - Slice Selects
    .pwr_main_pwr_i (1'b0                )  // TODO - Enable
  );


  // ------------------------------------------------------
  //  tests.all_ram8: u_ram8
  // ------------------------------------------------------
  all_ram8 u_ram8 (
    .main_clk_i     (1'b0                 ), // TODO - Clock
    .main_rst_an_i  (1'b0                 ), // TODO - Async Reset (Low-Active)
    .io_main_ena_i  (1'b0                 ), // TODO - Memory Access Enable
    .io_main_addr_i ({$clog2(119) {1'b0}} ), // TODO - Memory Address
    .io_main_wena_i (1'b0                 ), // TODO - Memory Write Enable
    .io_main_wdata_i(68'h00000000000000000), // TODO - Memory Write Data
    .io_main_rdata_o(                     ), // TODO - Memory Read Data
    .io_main_sel_i  (17'h00000            ), // TODO - Slice Selects
    .pwr_main_pwr_i (1'b0                 )  // TODO - Enable
  );

endmodule // all

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

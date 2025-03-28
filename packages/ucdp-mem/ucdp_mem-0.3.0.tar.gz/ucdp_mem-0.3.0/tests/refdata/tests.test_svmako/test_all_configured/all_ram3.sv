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
// Module:     tests.all_ram3
// Data Model: tests.test_svmako.RamMod
//
//
// Org:         4096x16 (8 KB)
// Wordmasks:   0xFFFF
// Accesslanes: -
// Powerlanes:  one='4 KB', two='4 KB'
// Constraints: MemTechConstraints(max_depth=2048, max_width=32, depth_inc=32, width_inc=4)
// Segmentation:
//     y/x         0
//      0  2048x16/1,pwr=one
//      1  2048x16/1,pwr=two
//     Total: 4096x16/1(8 KB)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram3 ( // tests.test_svmako.RamMod
  // main_i: Clock and Reset
  input  wire                     main_clk_i,      // Clock
  input  wire                     main_rst_an_i,   // Async Reset (Low-Active)
  // io_i
  //   io_main_i
  input  wire                     io_main_ena_i,   // Memory Access Enable
  input  wire  [$clog2(4095)-1:0] io_main_addr_i,  // Memory Address
  input  wire                     io_main_wena_i,  // Memory Write Enable
  input  wire  [15:0]             io_main_wdata_i, // Memory Write Data
  output logic [15:0]             io_main_rdata_o, // Memory Read Data
  // pwr_i
  //   pwr_one_i
  input  wire                     pwr_one_pwr_i,   // Enable
  //   pwr_two_i
  input  wire                     pwr_two_pwr_i    // Enable
  // tech_i
);



  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  // mem_s
  //   mem_y0_x0_s
  logic                    mem_y0_x0_ena_s;   // Memory Access Enable
  logic [$clog2(2047)-1:0] mem_y0_x0_addr_s;  // Memory Address
  logic                    mem_y0_x0_wena_s;  // Memory Write Enable
  logic [15:0]             mem_y0_x0_wdata_s; // Memory Write Data
  logic [15:0]             mem_y0_x0_rdata_s; // Memory Read Data
  //   mem_y1_x0_s
  logic                    mem_y1_x0_ena_s;   // Memory Access Enable
  logic [$clog2(2047)-1:0] mem_y1_x0_addr_s;  // Memory Address
  logic                    mem_y1_x0_wena_s;  // Memory Write Enable
  logic [15:0]             mem_y1_x0_wdata_s; // Memory Write Data
  logic [15:0]             mem_y1_x0_rdata_s; // Memory Read Data


  // ------------------------------------------------------
  //  tests.all_ram3_mux: u_mux
  // ------------------------------------------------------
  all_ram3_mux u_mux (
    .in_main_ena_i    (io_main_ena_i    ), // Memory Access Enable
    .in_main_addr_i   (io_main_addr_i   ), // Memory Address
    .in_main_wena_i   (io_main_wena_i   ), // Memory Write Enable
    .in_main_wdata_i  (io_main_wdata_i  ), // Memory Write Data
    .in_main_rdata_o  (io_main_rdata_o  ), // Memory Read Data
    .out_y0_x0_ena_o  (mem_y0_x0_ena_s  ), // Memory Access Enable
    .out_y0_x0_addr_o (mem_y0_x0_addr_s ), // Memory Address
    .out_y0_x0_wena_o (mem_y0_x0_wena_s ), // Memory Write Enable
    .out_y0_x0_wdata_o(mem_y0_x0_wdata_s), // Memory Write Data
    .out_y0_x0_rdata_i(mem_y0_x0_rdata_s), // Memory Read Data
    .out_y1_x0_ena_o  (mem_y1_x0_ena_s  ), // Memory Access Enable
    .out_y1_x0_addr_o (mem_y1_x0_addr_s ), // Memory Address
    .out_y1_x0_wena_o (mem_y1_x0_wena_s ), // Memory Write Enable
    .out_y1_x0_wdata_o(mem_y1_x0_wdata_s), // Memory Write Data
    .out_y1_x0_rdata_i(mem_y1_x0_rdata_s)  // Memory Read Data
  );

endmodule // all_ram3

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

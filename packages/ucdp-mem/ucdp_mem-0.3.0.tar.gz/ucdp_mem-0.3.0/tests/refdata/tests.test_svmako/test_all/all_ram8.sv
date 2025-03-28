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
// Module:     tests.all_ram8
// Data Model: tests.test_svmako.RamMod
//
//
// Org:         120x68 (1020 bytes)
// Wordmasks:   0x1FFFF, 0x1FFFF, 0x1FFFF, 0x1FFFF
// Accesslanes: -
// Powerlanes:  -
// Constraints: -
// Segmentation:
//     y/x    0
//      0  120x68/1
//     Total: 120x68/17(1020 bytes)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram8 ( // tests.test_svmako.RamMod
  // main_i: Clock and Reset
  input  wire                    main_clk_i,      // Clock
  input  wire                    main_rst_an_i,   // Async Reset (Low-Active)
  // io_i
  //   io_main_i
  input  wire                    io_main_ena_i,   // Memory Access Enable
  input  wire  [$clog2(119)-1:0] io_main_addr_i,  // Memory Address
  input  wire                    io_main_wena_i,  // Memory Write Enable
  input  wire  [67:0]            io_main_wdata_i, // Memory Write Data
  output logic [67:0]            io_main_rdata_o, // Memory Read Data
  input  wire  [16:0]            io_main_sel_i,   // Slice Selects
  // pwr_i
  //   pwr_main_i
  input  wire                    pwr_main_pwr_i   // Enable
  // tech_i
);



  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  // mem_s
  //   mem_main_s
  logic                   mem_main_ena_s;   // Memory Access Enable
  logic [$clog2(119)-1:0] mem_main_addr_s;  // Memory Address
  logic                   mem_main_wena_s;  // Memory Write Enable
  logic [67:0]            mem_main_wdata_s; // Memory Write Data
  logic [67:0]            mem_main_rdata_s; // Memory Read Data
  logic [16:0]            mem_main_sel_s;   // Slice Selects

  // ------------------------------------------------------
  //  Assigns
  // ------------------------------------------------------
  assign mem_main_ena_s   = io_main_ena_i;
  assign mem_main_addr_s  = io_main_addr_i;
  assign mem_main_wena_s  = io_main_wena_i;
  assign mem_main_wdata_s = io_main_wdata_i;
  assign io_main_rdata_o  = mem_main_rdata_s;
  assign mem_main_sel_s   = io_main_sel_i;

endmodule // all_ram8

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

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
// Module:     tests.all_ram2_mux
// Data Model: tests.test_svmako.SegMuxMod
//
//
// y/x         0
//  0  1024x64/1,acc=one
//  1  1024x64/1,acc=two
//  2  2048x64/1,acc=two
// Total: 4096x64/1(32 KB)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_ram2_mux ( // tests.test_svmako.SegMuxMod
  // in_i
  //   in_one_i
  input  wire                     in_one_ena_i,      // Memory Access Enable
  input  wire  [$clog2(1023)-1:0] in_one_addr_i,     // Memory Address
  input  wire                     in_one_wena_i,     // Memory Write Enable
  input  wire  [63:0]             in_one_wdata_i,    // Memory Write Data
  output logic [63:0]             in_one_rdata_o,    // Memory Read Data
  //   in_two_i
  input  wire                     in_two_ena_i,      // Memory Access Enable
  input  wire  [$clog2(3071)-1:0] in_two_addr_i,     // Memory Address
  input  wire                     in_two_wena_i,     // Memory Write Enable
  input  wire  [63:0]             in_two_wdata_i,    // Memory Write Data
  output logic [63:0]             in_two_rdata_o,    // Memory Read Data
  // out_o
  //   out_y0_x0_o
  output logic                    out_y0_x0_ena_o,   // Memory Access Enable
  output logic [$clog2(1023)-1:0] out_y0_x0_addr_o,  // Memory Address
  output logic                    out_y0_x0_wena_o,  // Memory Write Enable
  output logic [63:0]             out_y0_x0_wdata_o, // Memory Write Data
  input  wire  [63:0]             out_y0_x0_rdata_i, // Memory Read Data
  //   out_y1_x0_o
  output logic                    out_y1_x0_ena_o,   // Memory Access Enable
  output logic [$clog2(1023)-1:0] out_y1_x0_addr_o,  // Memory Address
  output logic                    out_y1_x0_wena_o,  // Memory Write Enable
  output logic [63:0]             out_y1_x0_wdata_o, // Memory Write Data
  input  wire  [63:0]             out_y1_x0_rdata_i, // Memory Read Data
  //   out_y2_x0_o
  output logic                    out_y2_x0_ena_o,   // Memory Access Enable
  output logic [$clog2(2047)-1:0] out_y2_x0_addr_o,  // Memory Address
  output logic                    out_y2_x0_wena_o,  // Memory Write Enable
  output logic [63:0]             out_y2_x0_wdata_o, // Memory Write Data
  input  wire  [63:0]             out_y2_x0_rdata_i  // Memory Read Data
);

// TODO

endmodule // all_ram2_mux

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

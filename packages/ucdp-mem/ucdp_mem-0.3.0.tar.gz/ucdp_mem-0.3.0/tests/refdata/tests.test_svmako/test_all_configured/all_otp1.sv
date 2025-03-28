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
// Module:     tests.all_otp1
// Data Model: tests.test_svmako.OtpMod
//
//
// Org:         1024x64 (8 KB)
// Wordmasks:   0xFFFFFFFF, 0xFFFFFFFF
// Accesslanes: -
// Powerlanes:  -
// Constraints: -
// Segmentation:
//     y/x     0
//      0  1024x64/1
//     Total: 1024x64/1(8 KB)
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module all_otp1 ( // tests.test_svmako.OtpMod
  // main_i: Clock and Reset
  input  wire                     main_clk_i,      // Clock
  input  wire                     main_rst_an_i,   // Async Reset (Low-Active)
  // io_i
  //   io_main_i
  input  wire                     io_main_ena_i,   // Memory Access Enable
  input  wire  [$clog2(1023)-1:0] io_main_addr_i,  // Memory Address
  input  wire                     io_main_wena_i,  // Memory Write Enable
  input  wire  [63:0]             io_main_wdata_i, // Memory Write Data
  output logic [63:0]             io_main_rdata_o  // Memory Read Data
  // pwr_i
  //   pwr_main_i
  // tech_i
);


endmodule // all_otp1

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

SDET Coding Challenge - QA Report
1. Executive Summary
This report documents the findings of the testing phase for the LoanPro Calculator CLI. While the application handles basic arithmetic and input validation correctly, several critical precision bugs were identified. These issues directly contradict the technical requirements specified in the documentation (Section 5.3), specifically regarding the 16-digit precision guarantee.

2. Bug Findings
BUG-01: Precision Loss in Addition (Requirement Regression)
Command: docker run --rm public.ecr.aws/l4q9w4c5/loanpro-calculator-cli add 1.000000000000001 1.000000000000001

Expected Result: 2.000000000000002

Reasoning: Section 5.3 of the documentation explicitly states that this specific operation should yield this exact result to guarantee 16-digit precision.

Actual Result: Result: 2

Probably Root Cause: The application seems to be using an integer-based parser or a rounding strategy that ignores the 15th and 16th decimal places, treating the input as a whole number when the decimal part is sufficiently small.

BUG-02: Division Result Truncation
Command: docker run --rm [image] divide 5 2.9999999999999999999999998

Expected Result: 1.6666666666666667

Reasoning: To comply with the 16-digit precision rule, the division should return at least 16 significant digits.

Actual Result: Result: 1.66666667

Probably Root Cause: The output formatter or the data type used for the divide operation appears to be limited to a fixed 8-decimal precision, which violates the project's 16-digit standard.

BUG-03: Floating Point Precision "Negative Zero"
Command: docker run --rm [image] subtract -1.000000001 -1.00000000000001

Expected Result: -0.00000000099999

Reasoning: A subtraction of two distinct negative values should result in the exact mathematical difference, maintaining the sign and decimal integrity.

Actual Result: Result: -0

Probably Root Cause: This is an IEEE 754 floating-point artifact. The result is so close to zero that the system rounds the value but preserves the sign bit. This confirms the engine cannot handle the required decimal depth.

BUG-04: Integer Overflow/Precision in Large Multiplications
Command: docker run --rm [image] multiply -99999999999999 -9999999999999999

Expected Result: 999999999999989900000000000000 (Approx)

Reasoning: Mathematical multiplication of large integers should maintain significant digits before falling into scientific notation or rounding.

Actual Result: Result: 999999999999990000000000000000

Probably Root Cause: The internal calculation is likely casting large integers to a standard float64 (double precision) type prematurely, causing a loss of the least significant digits during the mantissa calculation.

3. Full Test Execution Log
ID: TC-01
Operation: Multiplication
Command: multiply -5 -5
Expected Result: Result: 25
Current Result: Result: 25
Pass / Fail: Pass

ID: TC-02
Operation: Multiplication
Command: multiply -5 5
Expected Result: Result: -25
Current Result: Result: -25
Pass / Fail: Pass

ID: TC-03
Operation: Multiplication
Command: multiply -99999999999999 -9999999999999999
Expected Result: 9.999999999999899e+27
Current Result: Result: 999999999999990000000000000000
Pass / Fail: Fail

ID: TC-04
Operation: Division
Command: divide 5 0
Expected Result: Error: Cannot divide by zero
Current Result: Error: Cannot divide by zero
Pass / Fail: Pass (Known Issue)

ID: TC-05
Operation: Division
Command: divide 5 1
Expected Result: Result: 5
Current Result: Result: 5
Pass / Fail: Pass

ID: TC-06
Operation: Division
Command: divide 5 2
Expected Result: Result: 2.5
Current Result: Result: 2.5
Pass / Fail: Pass

ID: TC-07
Operation: Division
Command: divide 5 2.00000000000000000000000000000001
Expected Result: Result: 2.4999999999999999
Current Result: Result: 2.5
Pass / Fail: Fail

ID: TC-08
Operation: Division
Command: divide 5 2.9999999999999999999999998
Expected Result: Result: 1.6666666666666667
Current Result: Result: 1.66666667
Pass / Fail: Fail

ID: TC-09
Operation: Validation
Command: divide 5 2.e
Expected Result: Error: Invalid argument. Must be a numeric value.
Current Result: Error: Invalid argument. Must be a numeric value.
Pass / Fail: Pass

ID: TC-10
Operation: Validation
Command: divide 5 e
Expected Result: Error: Invalid argument. Must be a numeric value.
Current Result: Error: Invalid argument. Must be a numeric value.
Pass / Fail: Pass

ID: TC-11
Operation: Division
Command: divide 5 5
Expected Result: Result: 1
Current Result: Result: 1
Pass / Fail: Pass

ID: TC-12
Operation: Addition
Command: add 0.0000000000000001 0.0000000000000001
Expected Result: Result: 0.0000000000000002
Current Result: Result: 0
Pass / Fail: Fail

ID: TC-13
Operation: Addition
Command: add 1.0000000000000001 1.0000000000000001
Expected Result: Result: 2.0000000000000002
Current Result: Result: 2
Pass / Fail: Fail

ID: TC-14
Operation: Addition
Command: add 1.1111111111111111 1.1111111111111111
Expected Result: Result: 2.2222222222222222
Current Result: Result: 2.22222222
Pass / Fail: Fail

ID: TC-15
Operation: Addition
Command: add 999999999999999999 999999999999999999
Expected Result: Result: 1999999999999999998
Current Result: Result: 2000000000000000000
Pass / Fail: Fail

ID: TC-16
Operation: Addition
Command: add 9 9
Expected Result: Result: 18
Current Result: Result: 18
Pass / Fail: Pass

ID: TC-17
Operation: Validation
Command: add a b
Expected Result: Error: Invalid argument. Must be a numeric value.
Current Result: Error: Invalid argument. Must be a numeric value.
Pass / Fail: Pass

ID: TC-18
Operation: Validation
Command: add % 5
Expected Result: Error: Invalid argument. Must be a numeric value.
Current Result: Error: Invalid argument. Must be a numeric value.
Pass / Fail: Pass

ID: TC-19
Operation: Subtraction
Command: subtract 0 0
Expected Result: Result: 0
Current Result: Result: 0
Pass / Fail: Pass

ID: TC-20
Operation: Subtraction
Command: subtract -0 -0
Expected Result: Result: 0
Current Result: Result: 0
Pass / Fail: Pass

ID: TC-21
Operation: Subtraction
Command: subtract -1 -1
Expected Result: Result: 0
Current Result: Result: 0
Pass / Fail: Pass

ID: TC-22
Operation: Subtraction
Command: subtract -1.000000001 -1.00000000000001
Expected Result: Result: -0.00000000099999
Current Result: Result: -0
Pass / Fail: Fail

ID: TC-23
Operation: Subtraction
Command: subtract 999999999 9999999999999
Expected Result: Result: -9999000000000
Current Result: Result: -9999000000000
Pass / Fail: Pass

ID: TC-24
Operation: Validation
Command: subtract 1 e
Expected Result: Error: Invalid argument. Must be a numeric value.
Current Result: Error: Invalid argument. Must be a numeric value.
Pass / Fail: Pass

ID: TC-25
Operation: Subtraction
Command: subtract 1 -111111111111111
Expected Result: Result: 111111111111112
Current Result: Result: 111111111111112
Pass / Fail: Pass
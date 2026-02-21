import subprocess
import pytest

def run_calc(op, arg1, arg2):
    cmd = f"docker run --rm public.ecr.aws/l4q9w4c5/loanpro-calculator-cli {op} {arg1} {arg2}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else result.stderr.strip()

@pytest.mark.parametrize("test_id, op, a1, a2, expected", [
    ("TC-01", "multiply", "-5", "-5", "Result: 25"),
    ("TC-02", "multiply", "-5", "5", "Result: -25"),
    ("TC-03", "multiply", "-99999999999999", "-9999999999999999", "999999999999990000000000000000"),
    ("TC-04", "divide", "5", "0", "Error: Cannot divide by zero"),
    ("TC-05", "divide", "5", "1", "Result: 5"),
    ("TC-06", "divide", "5", "2", "Result: 2.5"),
    ("TC-07", "divide", "5", "2.00000000000000000000000000000001", "Result: 2.4999999999999999"),
    ("TC-08", "divide", "5", "2.9999999999999999999999998", "Result: 1.6666666666666667"),
    ("TC-09", "divide", "5", "2.e", "Error: Invalid argument"),
    ("TC-10", "divide", "5", "e", "Error: Invalid argument"),
    ("TC-11", "divide", "5", "5", "Result: 1"),
    ("TC-12", "add", "0.0000000000000001", "0.0000000000000001", "Result: 0.0000000000000002"),
    ("TC-13", "add", "1.0000000000000001", "1.0000000000000001", "Result: 2.0000000000000002"),
    ("TC-14", "add", "1.1111111111111111", "1.1111111111111111", "Result: 2.2222222222222222"),
    ("TC-15", "add", "999999999999999999", "999999999999999999", "Result: 1999999999999999998"),
    ("TC-16", "add", "9", "9", "Result: 18"),
    ("TC-17", "add", "a", "b", "Error: Invalid argument"),
    ("TC-18", "add", "%", "5", "Error: Invalid argument"),
    ("TC-19", "subtract", "0", "0", "Result: 0"),
    ("TC-20", "subtract", "-0", "-0", "Result: 0"),
    ("TC-21", "subtract", "-1", "-1", "Result: 0"),
    ("TC-22", "subtract", "-1.000000001", "-1.00000000000001", "Result: -0.00000000099999"),
    ("TC-23", "subtract", "999999999", "9999999999999", "Result: -9999000000000"),
    ("TC-24", "subtract", "1", "e", "Error: Invalid argument"),
    ("TC-25", "subtract", "1", "-111111111111111", "Result: 111111111111112")
])
def test_calculator_logic(test_id, op, a1, a2, expected):
    actual = run_calc(op, a1, a2)
    assert expected in actual, f"Falla en {test_id}: Esperaba {expected} pero se obtuvo {actual}"
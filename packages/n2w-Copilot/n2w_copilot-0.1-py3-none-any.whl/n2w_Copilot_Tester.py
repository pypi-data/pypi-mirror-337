# n2w_Copilot_Tester.py
import sys
import argparse
from n2w_Copilot_3 import num2words

def test():
    with open('n2w_Test_Numeri_Input.txt', 'r') as f:
        values = f.read().split()
    print("Values read from file:", values)
    
    results = []
    for val in values:
        try:
            result = "{0} = {1}".format(val, num2words(val))
            print(result)
            results.append(result)
        except KeyError:            
            error_message = "Error: argument contains non-digits"
            print(error_message)
            results.append(error_message)
    
    with open('n2w_test_result.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')

def main():
    parser = argparse.ArgumentParser(description="Test the num2words function")
    parser.add_argument("num", nargs='*', help="Numbers to convert to words")
    parser.add_argument("-t", "--test", dest="test", action='store_true', default=False, help="Test mode: reads from file")
    args = parser.parse_args()
    
    if args.test:
        test()
    else:
        results = []
        for num in args.num:
            try:
                result = num2words(num)
                output = "For {0}, say: {1}".format(num, result)
                print(output)
                results.append(output)
            except KeyError:
                error_message = f"Error: argument '{num}' contains non-digits"
                print(error_message)
                results.append(error_message)
        
        with open('n2w_test_result.txt', 'w') as f:
            for line in results:
                f.write(line + '\n')

if __name__ == '__main__':
    main()

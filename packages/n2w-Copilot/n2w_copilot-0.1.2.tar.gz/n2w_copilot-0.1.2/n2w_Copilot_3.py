# n2w_Copilot_3.py
import sys, string, argparse

_1to9dict = {'0': '', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
             '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}

_10to19dict = {'0': 'ten', '1': 'eleven', '2': 'twelve',
               '3': 'thirteen', '4': 'fourteen', '5': 'fifteen',
               '6': 'sixteen', '7': 'seventeen', '8': 'eighteen', '9': 'nineteen'}

_20to90dict = {'2': 'twenty', '3': 'thirty', '4': 'forty', '5': 'fifty',
               '6': 'sixty', '7': 'seventy', '8': 'eighty', '9': 'ninety'}

_magnitude_list = [(0, ''), (3, ' thousand '), (6, ' million '), (9, ' billion '), (12, ' trillion '), (15, '')]

def num2words(num_string):
    if num_string == '0':
        return 'zero'
    num_string = num_string.replace(",", "")
    num_length = len(num_string)
    max_digits = _magnitude_list[-1][0]
    if num_length > max_digits:
        return "Sorry, can't handle numbers with more than {0} digits".format(max_digits)
    num_string = '00' + num_string

    word_string = ''
    for mag, name in _magnitude_list:
        if mag >= num_length:
            return word_string
        else:
            hundreds, tens, ones = num_string[-mag-3], num_string[-mag-2], num_string[-mag-1]
            if not (hundreds == tens == ones == '0'):
                word_string = _handle1to999(hundreds, tens, ones) + name + word_string

def _handle1to999(hundreds, tens, ones):
    if hundreds == '0':
        return _handle1to99(tens, ones)
    else:
        return _1to9dict[hundreds] + ' hundred ' + _handle1to99(tens, ones)

def _handle1to99(tens, ones):
    if tens == '0':
        return _1to9dict[ones]
    elif tens == '1':
        return _10to19dict[ones]
    else:
        return _20to90dict[tens] + ' ' + _1to9dict[ones]

def test():
    print("Entering test mode ...")
    values = input("Enter numbers separated by spaces: ").split()
    print("Values read from stdin:", values)
    for val in values:
        try:
            print("{0} = {1}".format(val, num2words(val)))
        except KeyError:
            print("Error: argument contains non-digits")

def main():
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("num", nargs='*')
    parser.add_argument("-t", "--test", dest="test", action='store_true', default=False, help="Test mode: reads from stdin")
    args = parser.parse_args()
    
    if args.test:
        test()
    else:
        for num in args.num:
            try:
                result = num2words(num)
            except KeyError:
                print(f"Error: argument '{num}' contains non-digits")
            else:
                print("For {0}, say: {1}".format(num, result))

if __name__ == '__main__':
# Inizio simulazione di argomenti passati dalla riga di comando
#    sys.argv = ['n2w_Copilot_3.py', '123', 'abc', '456']
    main()
else:
    print("n2w loaded as a module")

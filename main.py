import re
import sys

def display_error_and_exit(error_msg):
  print(error_msg, file=sys.stderr)
  sys.exit(1)

def is_space(x):
  return x == ' '

def is_number(x):
  return x.isnumeric()

def is_sign(x):
  return x == '+' or x == '-'

def is_equal_sign(x):
  return x == '='

def is_exponent(input, pos):
  if len(input) - pos < 3:
    return False
  return input[pos: pos+3] == 'X^0' or input[pos: pos+3] == 'X^1' or input[pos: pos+3] == 'X^2'

def parse_input(input):
  i = 0
  while i < len(input):
    while i < len(input) and is_space(input[i]):
      i += 1
    if i < len(input) and is_sign(input[i]):
      i += 1
      while i < len(input) and is_space(input[i]):
        i+= 1
      if i < len(input) and not is_number(input[i]) and not is_exponent(input, i):
        return False
    if i < len(input) and is_number(input[i]):
      while i < len(input) and is_number(input[i]):
        i += 1
    if i < len(input) and is_equal_sign(input[i]):
      i += 1
      while i < len(input) and is_space(input[i]):
        i += 1
      if i < len(input) and not is_number(input[i]) and not is_exponent(input, i) and not is_sign(input[i]):
        return False
    i += 1
  return True
  
def get_equation_monomials(argv):
  equation_monomials = re.split('(?=[+\-])', sys.argv[1])
  if equation_monomials[0] == '': # escape the first '' element as result of spliting first monomial
      equation_monomials = equation_monomials[1:]
  return equation_monomials

def get_equal_sign_position(equation_monomials):
  for index, value in enumerate(equation_monomials):
    if not value:
      display_error_and_exit("SYNTAX ERROR: EQUATION MALFORMED")
    if value[-1] == "=":
      equation_monomials[index] = equation_monomials[index].strip(" =") 
      return index + 1
    if '=' in value:
      tmp_monomial = value.split("=")
      del equation_monomials[index]
      equation_monomials[index:index] = tmp_monomial
      return index + 1
  return -1

def append_plus_sign_first_monominal(equation_monomials):
  if equation_monomials[0][0] not in ['+', '-']:
      equation_monomials[0] = '+' + equation_monomials[0]

def check_sign_errors(equation_monomials):
  for i in range(len(equation_monomials)):
    if len(equation_monomials[i]) < 2:
      display_error_and_exit("SYNTAX ERROR: SIGN ERROR")
    equation_monomials[i] = equation_monomials[i].strip()

def switch_rhs_monomial_sign(equation_monomials, equal_sign_index):
  for i in range(equal_sign_index, len(equation_monomials)):
    if equation_monomials[i][0] not in ['+', '-']:
      equation_monomials[i] = '-' + equation_monomials[i]
    elif equation_monomials[i][0] == '+':
      equation_monomials[i] = '-' + equation_monomials[i][1:]
    else:
      equation_monomials[i] = '+' + equation_monomials[i][1:]

def check_coefficient(coefficient):
  list_chars = list(coefficient)
  if list_chars[0] not in ['+', '-']:
    display_error_and_exit("SYNTAX ERROR: COEFFICIENT ERROR")
  i = 2 if list_chars[1] == ' ' else 1
  for i in range(i, len(list_chars)): # exp: +5 2 *X^3
    if i != 1 and list_chars[i] == ' ':
      display_error_and_exit("SYNTAX ERROR: SYNTAX ERROR")
    if not list_chars[i].isnumeric():
      display_error_and_exit("SYNTAX ERROR: NON NUMERIC coefficient")


def handle_exponent(equation_dict, monomial):
  if len(monomial) < 2:
    display_error_and_exit("SYNTAX ERROR: WRONG SIGN") # exp: 2 * x^2 or 2 * X^4
  sign = 1 if monomial[0] == '+' else -1
  match monomial[1:].strip():
    case "X^0":
      equation_dict[0].append(sign * 1)
    case "X^1":
      equation_dict[1].append(sign * 1)
    case "X^2":
      equation_dict[2].append(sign * 1)
    case _:
      display_error_and_exit("SYNTAX ERROR: WRONG EXPONENT" + monomial) # exp: 2 * x^2 or 2 * X^4


def convert_equation_monomials_list_to_dict(equation_monomials):
  equation_dict = {}

  for i in range(3):
    equation_dict[i] = []
  for monomial in equation_monomials:
    if '*' in monomial:
      try:
        coefficient, exponent = map(str.strip, monomial.split('*'))
        check_coefficient(coefficient)
        if len(coefficient) < 2:
          display_error_and_exit("SYNTAX ERROR") # exp 3 - * X^2
        coefficient = coefficient.replace(' ', '') # remove white space from sign and coeff 
        match exponent:
          case "X^0":
            equation_dict[0].append(int(coefficient))
          case "X^1":
            equation_dict[1].append(int(coefficient))
          case "X^2":
            equation_dict[2].append(int(coefficient))
          case _:
            display_error_and_exit("SYNTAX ERROR: WRONG EXPONEN 7 T") # exp: 2 * x^2 or 2 * X^4 
      except:
        display_error_and_exit("SYNTAX ERROR: STRAY *")
    else:
      x = monomial[1:].strip()
      if x.isnumeric():
        equation_dict[0].append(int(monomial.replace(' ', '')))
      else:
        handle_exponent(equation_dict, monomial)

  return equation_dict

def main():
  if len(sys.argv) > 2:
    display_error_and_exit("WRONG NUMBER OF ARGUMENTS")
  if not parse_input(sys.argv[1]):
    display_error_and_exit("SYNTAX ERROR PARSER")    
  equation_monomials = get_equation_monomials(sys.argv)
  check_sign_errors(equation_monomials) #exp: +-+5
  append_plus_sign_first_monominal(equation_monomials)
  equal_sign_index = get_equal_sign_position(equation_monomials)
  if equal_sign_index < 1:
    display_error_and_exit("ERROR EQUAL SIGN")
  
  switch_rhs_monomial_sign(equation_monomials, equal_sign_index)
  equation_dict = convert_equation_monomials_list_to_dict(equation_monomials)
  print(equation_dict)
main()
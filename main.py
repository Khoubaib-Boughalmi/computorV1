from re import split, match
from typing import Optional
from math import sqrt
# Examples:
# 5 + 4 * X + X^2= X^2
# 5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^^3 = X^0 - 3
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^2 = X^0 - 3 - X

# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^^3 = X^0 - 3
# 8 * X^0 - 6 * X^1 + 0 * X^2.5 - 5.6 * X^3 = X^0 - 3
# `8 * X^0 - 6 * X1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3`
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3
# 8 * X^0 - 6 * XX^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3
# 8 * X^0 - 6 * CX^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3

"""

    parsing mechanism ==> * validate polynomial
                      ==> * exatract data into valid container
    steps:
        - split by `=` sign ==> 2 portion
        - split by `+` and `-` sign but keep the delimiter
        - convert the list into list of objects with metadata
"""

def split_equation(equation: str) -> list[str, str]:
    return equation.split("=")

def split_components(equation: str) -> list[str]:
    return split(r'(\+|-)', equation)

def strip_empty_elements(elements: list[str]) -> list[str]:
    newList = []
    left, right = 0, len(elements) - 1
    while elements[left] == "":
        left +=1
    while elements[right] == "":
        right -=1
    
    while left <= right:
        newList.append(elements[left])
        left += 1
    return newList

def merge_component_with_sign(elements: list[str]) -> list[str]:
    current = 1
    component_list = []

    if elements[0] != "+" and elements[0] != "-":
        component_list.append(elements[0])
    while current < len(elements):
        if elements[current - 1] == "+":
            component_list.append(f"+{elements[current]}")
        elif elements[current - 1] == "-":
            component_list.append(f"-{elements[current]}")
        current += 1
    return  component_list

def strip_element(element: str) -> str:
    result = ""
    for ch in element:
        if ch == " ":
            continue
        result += ch
    return result

def strip_components(elements: list[str]) -> list[str]:
    for key, value in enumerate(elements):
        elements[key] = strip_element(value)

def check_validity(elements: list[str]) -> bool:
    for element in elements:
        if not element or not element.strip() or element == "+" or element == "-":
            return False
    return True

def split_coefficient_and_variable(element: str) -> list[str, Optional[str]]:
    splitted_element = element.split("*")
    if  len(splitted_element) < 1 or len(splitted_element) > 2:
        raise Exception("Wrong syntax: problem with * sign")
    for item in splitted_element:
        if not item:
            raise Exception("Wrong syntax: problem with * sign")
    return splitted_element

def is_valid_coeff(element: str) -> bool:
    pattern = r'^[+-]?\d+(\.\d+)?$'
    return bool(match(pattern, element))

def is_valid_variable(element: str) -> bool:
    """
        valid variables: exp: X^2 or X
    """
    if element[0] == "+" or element[0] == "-":
        element = element [1:]
    if element == "X":
        return True
    
    # Must start with "X^" and have at least one digit after it
    if element.startswith("X^") and element[2:].isdecimal():
        return True
    
    return False

def get_exponent(variable: str) -> int:
    if variable[0] == "-" or variable[0] == "+" :
        variable = variable[1:]
        
    if variable == "X":
        return 1
    exponent = int(variable[2:])
    if exponent > 2:
        raise Exception("Only second degree polynomials are allowed")
    return exponent

def create_two_elements_obj(elements: list[str]) -> dict:
    # first element should be a coeff
    # second element should be a variable with optional exponent
    element_obj = {}
    if not is_valid_coeff(elements[0]):
        raise Exception("Wrong coefficient: ", elements[0])
    if not is_valid_variable(elements[1]):
        raise Exception("Wrong variable: ", elements[1])
    element_obj["coeff"] = float(elements[0])
    element_obj["exponent"] = get_exponent(elements[1])
    return element_obj

def create_single_element_obj(element: str):
    element_obj = {}
    if is_valid_coeff(element):
        element_obj["coeff"] = float(element)
        element_obj["exponent"] = 0
    elif is_valid_variable(element):
        element_obj["coeff"] = -1 if element[0] == "-" else 1
        element_obj["exponent"] = get_exponent(element)
    else:
        raise Exception("Wrong coeff or variable", element)
    return element_obj

#  8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3 - X
#  8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3 +X -X
#  8 * X^-1 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = X^0 - 3 +X -X
#  8 * X^1 - 6 * X^1 - 0 * X^2 - 5.6 * X^3 = X^0 - 3 +X -X
#  8 * X^1 - 6 * X^1 - 0 -X^2 - 5.6 * X^3 = X^0 - 3 + X
#  8 * X^1 - 6 * X^1 - 0 -X^2 - 5.6 * X^3 = X^0 - 3- + X
#  8 * X^1 - 6 * X^1 - 2.2 + 0 -X^2 - 5.6 * X^3 = X^0 - 3- X


def create_components_obj(elements: list[str]):
    components_dict_list = []
    # sign
    # coefficient
    # variable
    # exponent

    # it is okay if we have a coeff but not a variable: 5 ==> 5*X^0
    # it is okay if we have variable without a coeff: X^2 ==> 1*X^2
    # it is okay if we have variable without an exponent: X ==> X^1
    for element in elements:
        splitted_element = split_coefficient_and_variable(element) # if we have empty element then there is an extra * ==> err
        if len(splitted_element) == 2:
            # we have a coeff and variable(optionally exopnent)
            components_dict_list.append(create_two_elements_obj(splitted_element))
        elif len(splitted_element) == 1:
            # we have a coeff or variable(optionally exopnent)
            components_dict_list.append(create_single_element_obj(splitted_element[0]))
        else:
            raise Exception("Somthing went wrong")
    return components_dict_list

def parse_input(equation: str) -> list:
    try:
        lhs, rhs = list(map(lambda x: x.strip(), split_equation(equation)))
        lhs_components = strip_empty_elements(split_components(lhs))
        rhs_components = strip_empty_elements(split_components(rhs))
        lhs_signed_components = merge_component_with_sign(lhs_components)
        rhs_signed_components = merge_component_with_sign(rhs_components)
        strip_components(lhs_signed_components)
        strip_components(rhs_signed_components)
        if not check_validity(lhs_signed_components) or not check_validity(rhs_signed_components):
            raise Exception("Invalid signs in the equation")
        lhs_objs = create_components_obj(lhs_signed_components)
        rhs_objs = create_components_obj(rhs_signed_components)
        print([lhs_objs, rhs_objs])
        return [lhs_objs, rhs_objs]
    except Exception as e:
        raise Exception(str(e))

def reverse_sign_rhs(elements: list[dict]) -> list:
    for elem in elements:
        elem["coeff"] *= -1

def merge_components(elements: list[dict]) -> list:
    merged_components = {0:0, 1:0, 2:0}
    for component in elements:
        merged_components[component["exponent"]] += component["coeff"]
    return merged_components

def solve_second_deg_equation(components):
    print(components)
    delta = components[1]**2 - 4 * components[2] * components[0]
    print(delta)
    if delta < 0:
        print("No solutions")
    else:
        x_prime = (-components[1]+sqrt(delta)) / (2*components[2])
        if delta == 0:
            print(f"{x_prime:.6f}")
        else:
            x_second = (-components[1]-sqrt(delta)) / (2*components[2])
            print(f"{x_prime:.6f}")
            print(f"{x_second:.6f}")


def solve_first_deg_equation(components):
    if components[0] == 0:
        print("No solution")
    else:
        print(f"{-components[0]/components[1]:.6f}")

def main():
    equation = input()
    components_list = []
    try:
        components_list = parse_input(equation)
        reverse_sign_rhs(components_list[1])
        mergeded_components_list = merge_components([*components_list[0], *components_list[1]])
        if mergeded_components_list[2] != 0:
            solve_second_deg_equation(mergeded_components_list)
        elif mergeded_components_list[1] != 0:
            solve_first_deg_equation(mergeded_components_list)
        else:
            if mergeded_components_list[0] != 0:
                print("No solution")
            else:
                print("0")

            
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()
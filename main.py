from re import split
from typing import Optional

# 5 + 4 * X + X^2= X^2
# 5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0

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
    

def create_components_obj(elements: list[str]):
    components_dict = {}
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
            print("two_element", splitted_element)
            pass
        elif len(splitted_element) == 1:
            # we have a coeff or variable(optionally exopnent)
            print("single_element", splitted_element)
        else:
            # error
            print("wrong", splitted_element)

            raise Exception("Somthing went wrong")


def parse_input(equation: str) -> bool:
    try:
        lhs, rhs = list(map(lambda x: x.strip(), split_equation(equation)))
        lhs_components = strip_empty_elements(split_components(lhs))
        rhs_components = strip_empty_elements(split_components(rhs))
        lhs_signed_components = merge_component_with_sign(lhs_components)
        rhs_signed_components = merge_component_with_sign(rhs_components)
        strip_components(lhs_signed_components)
        strip_components(rhs_signed_components)
        if not check_validity(lhs_signed_components) or not check_validity(rhs_signed_components):
            raise Exception("unvalid signs")
        create_components_obj(lhs_signed_components)
        create_components_obj(rhs_signed_components)
        print(lhs_signed_components)
        print(rhs_signed_components)
    except Exception as e:
        print(e)
# 5 + 4 * X    +X^2= X ^   2 
def main():
    equation = input() 
    parse_input(equation)
    
if __name__ == "__main__":
    main()
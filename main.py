from re import split
# 5 + 4 * X + X^2= X^2
# 5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
# 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0


# parsing mechanism ==> * validate polynomial
#                   ==> * exatract data into valid container

"""
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

def parse_input(equation: str) -> None:
    lhs, rhs = list(map(lambda x: x.strip(), split_equation(equation)))
    lhs_components = strip_empty_elements(split_components(lhs))
    rhs_components = strip_empty_elements(split_components(rhs))
    lhs_signed_components = merge_component_with_sign(lhs_components)
    rhs_signed_components = merge_component_with_sign(rhs_components)
    strip_components(lhs_signed_components)
    strip_components(rhs_signed_components)
    if not check_validity(lhs_signed_components) or not check_validity(rhs_signed_components):
        print("not valid")
        return False

# --5 + 4 * X +  +  X^2= -   X ^   2  
def main():
    equation = input() 
    parse_input(equation)
    
if __name__ == "__main__":
    main()
"""
Find the area
Assignment 0
Semester 2, 2021
CSSE1001/CSSE7030
"""

# Replace these <strings> with your name, student number and email address.
__author__ = "Harold Shaw, 47020665"
__email__ = "s4702066@student.uq.edu.au"

def calculate_area(w:int, h:int) -> int:
    '''Calculate the area of a rectangle

    Parameters:
        w(int): width
        h(int): height

    Returns:
        int: Area of a rectangle

    '''
    return (w * h)

def main():
    '''Print area of a rectangle from height and width inputs

    Parameters:
        None

    Returns:
        None

    '''
    w = int(input('Please input the width of the rectangle: '))
    h = int(input('Please input the height of the rectangle: '))
    print('The area of the rectangle is', calculate_area(w, h))
    return None

if __name__ == "__main__":
    main()

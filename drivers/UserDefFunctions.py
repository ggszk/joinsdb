# User definition functions
# return value: tuple

class UserDefFunctions :
    # example: "select add('col1', 'col2') from r" return col1 + col2
    # example: "select add('col1', 3) from r" return col1 + 3
    def add(self, col1, col2) :
        return (col1 + col2,)

    # multiple constant to a one column
    # example: "select multiple('col1', 5) from r" return col1 * 5
    def multiple(self, col1, col2) :
        return (col1*col2,)
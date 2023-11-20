class TextParser:
    def __init__(self):
        self.classes = {}   # String name, ParserClass value

    def parse_lines(self, lines):
        # Note: we seperate definitions and attributes so they dont need to be in order.
        self.classes = {}
        for l in lines:
            self.parse_line_for_definitions(l)
        for l in lines:
            self.parse_line_for_attributes(l)

    def parse_line_for_definitions(self, line):
        line_string = line.get_string()
        if line.get_period_count() == 0 and line.get_equals_count() == 0 and line_string != "":
            # Class definition case, where we just take the first word (throw if spaces?) and add it as a new class
            if line_string.find(" ") == -1: self.classes[line_string] = ParserClass()

    def parse_line_for_attributes(self, line):
        line_string = line.get_string()
        if line.get_period_count() == 1 and line.get_equals_count() == 1:
            # Attribute definition case, where we add an attribute to a class
            class_name = line_string[:line_string.find(".")]
            attribute_name = line_string[line_string.find(".") + 1:line_string.find("=")]
            attribute_type = line_string[line_string.find("=") + 1:].replace(" ", "")

            # Makes sure both types are valid
            if class_name in self.classes.keys() and attribute_type in self.classes.keys():
                self.classes[class_name].add_attribute(attribute_name, attribute_type)
    
    def get_classes(self):
        return self.classes

class ParserClass:
    def __init__(self):
        self.attributes = {}    # String name, String value

    def add_attribute(self, attribute_name, attribute_type):
        self.attributes[attribute_name] = attribute_type
    
    def get_attributes(self):
        return self.attributes
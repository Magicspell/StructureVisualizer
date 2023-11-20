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

    # NOTE: For inheritance, order DOES matter. Parent must be defined before child.
    def parse_line_for_definitions(self, line):
        line_string = line.get_string()
        if line.get_period_count() == 0 and line.get_equals_count() == 0 and line_string != "":
            # Class definition case, where we just take the first word (throw if spaces?) and add it as a new class
            if line_string.find(" ") == -1:
                # Non-inheritance case
                self.classes[line_string] = ParserClass()
            else:
                # Inheritance case
                # Syntax: <ParentClass> <ChildClass>
                word_array = line_string.split(" ")
                if len(word_array) == 2:
                    parent_class = word_array[0]
                    child_class = word_array[1]
                    if parent_class in self.classes.keys():
                        self.classes[child_class] = ParserClass(self.classes[parent_class], parent_class)

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
    def __init__(self, parent_class = None, parent_class_name = None):
        self.attributes = {}                        # String name, String value
        self.parent_class = parent_class            # ParserClass obj
        self.parent_class_name = parent_class_name  # String
        # ^Dont really need both

    def add_attribute(self, attribute_name, attribute_type):
        self.attributes[attribute_name] = attribute_type
    
    def get_attributes(self):
        return self.attributes
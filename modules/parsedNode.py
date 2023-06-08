from nodes import BaseNode

#Class that takes a parsed node, containes information if node could have been parsed
class ParsedNode:
    def __init__(self, node: BaseNode, hasSyntaxError:bool ):
        self.node = node
        self.hasSyntaxError = hasSyntaxError
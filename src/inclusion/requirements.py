import tree_sitter_clarity as tsclarity
from tree_sitter import Language, Parser, Node, Tree


class RequirementError(Exception):
    pass


class SyntaxTreeSearcher:
    def __init__(self):
        self.language = Language(tsclarity.language())
        self.parser = Parser(self.language)

    def get_definitions_and_dependencies(
        self, symbols: list[str], file_content: str
    ) -> set[Node]:
        tree = self.parser.parse(bytes(file_content, "utf8"))
        nodes = set()
        for symbol in symbols:
            # Get top-level node where the symbol is defined
            symbol_node = self.get_symbol_node(symbol, tree)
            nodes.add(symbol_node)
            # Look for unresolved identifiers in the node (dependencies)
            dependencies = self.get_dependencies_in_text(symbol, symbol_node)
            # Get top-level node of each dependency
            for d in dependencies:
                nodes.update(self.get_symbol_and_dependencies(str(d, "utf8"), tree))

        # Sort nodes by start point row, so that they are copied keeping its relative order
        nodes = sorted(nodes, key=lambda x: x.start_point.row)
        # Return nodes
        return nodes

    def get_symbol_node(self, symbol: str, tree: Tree) -> Node:
        definition_node_types = [
            "trait_definition",
            # "trait_usage", # Don't see the case where this is needed
            "token_definition",
            "constant_definition",
            "variable_definition",
            "mapping_definition",
            "function_definition",
        ]

        cursor = tree.walk()
        # Get to nodes under the root
        assert cursor.goto_first_child()

        while True:
            if cursor.node.type not in definition_node_types:
                # Go to next node
                assert cursor.goto_next_sibling()
                continue

            root_type = cursor.node.type
            definition_node = cursor.node
            searching = True

            # Get into the node for the search
            assert cursor.goto_first_child()

            while searching:
                if cursor.node.type == "identifier":
                    # Check if it is the identifier we are looking for
                    if str(cursor.node.text, "utf8") == symbol:
                        return definition_node
                    else:
                        # Get out of this sub-tree and go to next node
                        # This assumes identifiers are always found first (left-to-right) when looking at its definition
                        # This else branch could be removed, but is more efficient while the assumption is true
                        while cursor.node.type != root_type:
                            assert cursor.goto_parent()
                        break
                # Try to go to first child
                if not cursor.goto_first_child():
                    # Otherwise go to next sibling
                    while not cursor.goto_next_sibling():
                        # If none, go back to parent til there is a sibling
                        cursor.goto_parent()
                        # If there isn't and we reach the root, stop searching the subtree and go to next
                        if cursor.node.type == root_type:
                            searching = False

            if not cursor.goto_next_sibling():
                raise RequirementError(f"Symbol '{symbol}' not found.")

    def get_dependencies_in_text(self, symbol: str, node: Node) -> set[str]:
        cursor = node.walk()
        dependencies = set()
        match node.type:
            case "trait_definition":
                # We only need to look at the parameters for more traits
                # Queries are simple to use here
                query = self.language.query(
                    """
                    (trait_type (identifier) @dependency)
                    """
                )
                captures = query.captures(node)
                for c in captures:
                    dependencies.add(c[0].text)
            # case "token_definition": # I don't think we would need this
            #     pass
            case "constant_definition":
                # We only need to look for identifiers in the object
                assert cursor.goto_last_child() and cursor.goto_previous_sibling()
                query = self.language.query("(identifier) @dependency")
                captures = query.captures(cursor.node)
                for c in captures:
                    dependencies.add(c[0].text)
            case "variable_definition":
                # We only need to look for identifiers in the object
                assert cursor.goto_last_child() and cursor.goto_previous_sibling()
                query = self.language.query("(identifier) @dependency")
                captures = query.captures(cursor.node)
                for c in captures:
                    dependencies.add(c[0].text)
            # case "mapping_definition": # I think this is not needed
            #     pass
            case "function_definition":
                # Get dependencies from signature
                local_bindings = set()
                query = self.language.query(
                    """
                    (parameter_type
                        (trait_type
                            (identifier) @dependency))                                       
                """
                )
                # We query identifiers in tuple keys for removing it later from the result
                captures = query.captures(cursor.node)
                query = self.language.query(
                    """
                    (tuple_lit
                        key: (identifier) @named_key)
                """
                )
                tuple_keys = set()
                for n, _ in query.captures(cursor.node):
                    tuple_keys.add(n.text)
                # Move to function body
                assert (
                    cursor.goto_first_child()
                    and cursor.goto_last_child()
                    and cursor.goto_previous_sibling()
                )
                # If this is a let expression, we need to consider local bindings
                if cursor.node.type == "let_expression":
                    # Move to where local bindings start
                    assert (
                        cursor.goto_first_child()
                        and cursor.goto_next_sibling()
                        and cursor.goto_next_sibling()
                        and cursor.goto_next_sibling()
                    )

                    # Iterate over local bindings
                    while cursor.node.type == "local_binding":
                        cursor.goto_first_child() and cursor.goto_next_sibling()
                        # Add local definitions to a set for removing them from final result
                        local_bindings.add(cursor.node.text)
                        cursor.goto_next_sibling()
                        # Get unresolved identifiers from bindings
                        query = self.language.query("(identifier) @dependency")
                        captures += query.captures(cursor.node)
                        # Go to the next binding, if any
                        cursor.goto_parent() and cursor.goto_next_sibling()

                # Get dependencies in the rest of the body
                # A loop might not be required here. Just once should be enough.
                while cursor.goto_next_sibling():
                    query = self.language.query("(identifier) @dependency")
                    captures += query.captures(cursor.node)

                ignore_identifiers = tuple_keys | local_bindings

                for c in captures:
                    # Remove tuple keys and local bindings
                    if c[0].text not in ignore_identifiers:
                        dependencies.add(c[0].text)

        return dependencies

import tree_sitter_clarity as tsclarity
from tree_sitter import Language, Parser

LANGUAGE = Language(tsclarity.language())

class RequirementError(Exception):
    pass

def require(symbol, file_content):
    parser = Parser(LANGUAGE)
    tree = parser.parse(bytes(file_content, "utf8"))
    return get_symbol_and_dependencies(symbol, tree)

def get_symbol_and_dependencies(symbol, tree):
    # find symbol
    symbol_node = get_symbol_node(symbol, tree)
    nodes = set([symbol_node])
    # get its dependencies
    dependencies = get_dependencies_in_text(symbol, symbol_node)
    # recursion
    for d in dependencies:
        nodes.update(get_symbol_and_dependencies(str(d, "utf8"), tree))
    # return nodes
    return nodes

def get_symbol_node(symbol, tree):
    cursor = tree.walk()
    assert cursor.goto_first_child()

    definition_node_types = [
        "trait_definition",
        # "trait_usage", # Don't see the case where this is needed
        "token_definition",
        "constant_definition",
        "variable_definition",
        "mapping_definition",
        "function_definition"
    ]

    while True:
        if cursor.node.type not in definition_node_types:
            cursor.goto_next_sibling()
            continue

        root_type = cursor.node.type
        definition_node = cursor.node
        searching = True
        assert cursor.goto_first_child()

        while searching:
            if cursor.node.type == "identifier":
                if str(cursor.node.text, "utf8") == symbol:
                    return definition_node
                else:
                    while cursor.node.type != root_type:
                        cursor.goto_parent()
                    break
            if not cursor.goto_first_child():
                while not cursor.goto_next_sibling():
                    cursor.goto_parent()
                    if cursor.node.type == root_type:
                        searching = False

        if not cursor.goto_next_sibling():
            raise RequirementError(f"Symbol '{symbol}' not found.")
                  

def get_dependencies_in_text(symbol, node):
    cursor = node.walk()
    dependencies = set()
    match node.type:
        case "trait_definition":
            # We only need to look at the parameters for more traits
            # Queries are simple to use here
            query = LANGUAGE.query(
                """
                (trait_type (identifier) @dependency)
                """
            )
            captures = query.captures(node)
            for c in captures:
                dependencies.add(c[0].text)
        # case "token_definition":
        #     pass
        case "constant_definition":
            assert cursor.goto_last_child() and cursor.goto_previous_sibling()
            query = LANGUAGE.query("(identifier) @dependency")
            captures = query.captures(cursor.node)
            for c in captures:
                dependencies.add(c[0].text)
        case "variable_definition":
            assert cursor.goto_last_child() and cursor.goto_previous_sibling()
            query = LANGUAGE.query("(identifier) @dependency")
            captures = query.captures(cursor.node)
            for c in captures:
                dependencies.add(c[0].text)
        # case "mapping_definition":
        #     pass
        case "function_definition":
            # Get dependencies from signature
            print(node)
            print()
            local_bindings = set()
            query = LANGUAGE.query(
            """
                (parameter_type
                    (trait_type
                        (identifier) @dependency))                                       
            """)
            captures = query.captures(cursor.node)
            query = LANGUAGE.query(
            """
                (tuple_lit
                    key: (identifier) @named_key)
            """)
            tuple_keys = set()
            for n, _ in  query.captures(cursor.node):
                tuple_keys.add(n.text)
            # Get dependencies in local bindings
            assert cursor.goto_first_child()
            assert cursor.goto_last_child() and cursor.goto_previous_sibling()
            if cursor.node.type == "let_expression":
                assert (cursor.goto_first_child() and
                cursor.goto_next_sibling() and
                cursor.goto_next_sibling() and
                cursor.goto_next_sibling())

                while cursor.node.type == "local_binding":
                    cursor.goto_first_child() and cursor.goto_next_sibling()
                    local_bindings.add(cursor.node.text)
                    cursor.goto_next_sibling()
                    query = LANGUAGE.query("(identifier) @dependency")
                    captures += query.captures(cursor.node)
                    cursor.goto_parent() and cursor.goto_next_sibling()

            while cursor.goto_next_sibling():
                query = LANGUAGE.query("(identifier) @dependency")
                captures += query.captures(cursor.node)

            # Get dependencies in the rest of the body
            ignore_identifiers = tuple_keys | local_bindings
            for c in captures:
                if not c[0].text in ignore_identifiers:
                    dependencies.add(c[0].text)
            
    return dependencies


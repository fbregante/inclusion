import tree_sitter_clarity as tsclarity
from tree_sitter import Language, Parser

class RequirementError(Exception):
    pass

def require(symbol, file_content):
    LANGUAGE = Language(tsclarity.language())
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
        nodes.union(get_symbol_and_dependencies(d, tree))
    # return nodes
    return nodes

def get_symbol_node(symbol, tree):
    cursor = tree.walk()
    assert cursor.goto_first_child()

    definition_node_types = [
        "trait_definition",
        "trait_usage",
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

        assert cursor.goto_next_sibling()
                  
    raise RequirementError(f"Symbol '{symbol}' not found.")

def get_dependencies_in_text(symbol, node):
    cursor = node.walk()
    return []
  

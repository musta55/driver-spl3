import ast
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse the Python code from a file
def parse_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return ast.parse(code)

# Step 2: Extract all function AST nodes from the parsed code
def extract_function_asts(ast_tree):
    function_asts = [node for node in ast.walk(ast_tree) if isinstance(node, ast.FunctionDef)]
    return function_asts

# Step 3: Generate Control Flow Graph (CFG) and Data Flow Graph (DFG) for each extracted function
def generate_cfg_and_dfg(ast_functions):
    graphs = []

    for ast_function in ast_functions:
        cfg = nx.DiGraph()
        dfg = nx.DiGraph()

        def traverse(node, parent_node=None, code="", assigned_vars=None):
            nonlocal cfg, dfg
            node_id = len(cfg.nodes)  # Generate unique IDs for nodes
            node_label = f"{type(node).__name__}\n{code[:50]}"  # Label for nodes
            cfg.add_node(node_id, label=node_label)

            if parent_node is not None:
                cfg.add_edge(parent_node, node_id)

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_var = target.id
                        assigned_vars.add(assigned_var)

            elif isinstance(node, ast.Name):
                var_name = node.id
                for assigned_var in assigned_vars:
                    dfg.add_edge(assigned_var, var_name)

            for child_node in ast.iter_child_nodes(node):
                if isinstance(child_node, ast.FunctionDef):
                    continue  # Skip nested functions for simplicity
                child_code = ast.unparse(child_node) if isinstance(child_node, ast.AST) else ""
                traverse(child_node, node_id, child_code, assigned_vars.copy())

        code = ast.unparse(ast_function)
        traverse(ast_function, code=code, assigned_vars=set())
        graphs.append((cfg, dfg))

    return graphs

# Step 4: Visualize the Graphs (both CFG and DFG)
def visualize_graphs(cfg, dfg, output_file, layout_algorithm=nx.kamada_kawai_layout):
    fig, ax = plt.subplots(figsize=(10, 10))

    node_size = 700
    font_size = 6

    # Draw CFG nodes and edges
    pos = layout_algorithm(cfg)
    labels = {node: data['label'] for node, data in cfg.nodes(data=True)}
    nx.draw(cfg, pos, labels=labels, with_labels=True, node_size=node_size, font_size=font_size, node_color='black', font_color='white', ax=ax)

    # Draw DFG nodes and edges
    pos_dfg = layout_algorithm(dfg)
    labels_dfg = {node: node for node in dfg.nodes}
    nx.draw(dfg, pos_dfg, labels=labels_dfg, with_labels=True, node_size=node_size, font_size=font_size, node_color='red', font_color='white', ax=ax)

    plt.savefig(output_file, format='png', bbox_inches='tight', dpi=200)
    plt.show()

# Main function
if __name__ == '__main__':
    python_file = 'Fibonacci.py'  # Replace with the path to your Python code file

    ast_tree = parse_file(python_file)
    function_asts = extract_function_asts(ast_tree)

    for i, (cfg, dfg) in enumerate(generate_cfg_and_dfg(function_asts)):
        output_file = f'cfg_and_dfg_function_{i}.png'
        visualize_graphs(cfg, dfg, output_file, layout_algorithm=nx.kamada_kawai_layout)

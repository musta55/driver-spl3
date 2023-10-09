import ast
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse the Python code from a file
def parse_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return ast.parse(code)

# Step 2: Generate Control Flow Graph (CFG)
def generate_cfg(ast_tree):
    cfg = nx.DiGraph()

    def traverse(node, parent_node=None):
        if isinstance(node, ast.FunctionDef):
            cfg.add_node(node.name, type="FunctionDef")
        elif isinstance(node, ast.While) or isinstance(node, ast.For):
            cfg.add_node(node, type=type(node).__name__)
        else:
            cfg.add_node(node, type=type(node).__name__)
            if parent_node is not None:
                cfg.add_edge(parent_node, node)

        for child_node in ast.iter_child_nodes(node):
            traverse(child_node, node)

    traverse(ast_tree)
    return cfg

# Step 3: Visualize the CFG
def visualize_cfg(cfg, output_file):
    pos = nx.spring_layout(cfg, seed=42)  # Adjust layout algorithm as needed

    plt.figure(figsize=(10, 10))
    labels = {node: node_type for node, node_type in nx.get_node_attributes(cfg, "type").items()}
    nx.draw(cfg, pos, labels=labels, with_labels=True, node_size=500, font_size=10, node_color='skyblue')
    plt.savefig(output_file, format='png', bbox_inches='tight')
    plt.show()

# Main function
if __name__ == '__main__':
    python_file = 'Fibonacci.py'  # Replace with the path to your Python code file
    output_file = 'cfg.png'  # Output image file name

    ast_tree = parse_file(python_file)
    cfg = generate_cfg(ast_tree)
    visualize_cfg(cfg, output_file)

import ast
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse the Python code
def parse_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return ast.parse(code)

# Step 2: Generate Control Flow Graph (CFG)
def generate_cfg(ast_tree):
    cfg = nx.DiGraph()

    def traverse(node, parent_node=None):
        nonlocal cfg
        cfg.add_node(node, type=type(node).__name__)

        if parent_node:
            cfg.add_edge(parent_node, node)

        for child_node in ast.iter_child_nodes(node):
            traverse(child_node, node)

    traverse(ast_tree)
    return cfg

# Step 3: Generate Data Flow Graph (DFG)
def generate_dfg(ast_tree):
    dfg = nx.DiGraph()

    def traverse(node):
        nonlocal dfg

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    dfg.add_edge(target.id, node, type='assignment')

        for child_node in ast.iter_child_nodes(node):
            traverse(child_node)

    traverse(ast_tree)
    return dfg

# Step 4: Combine Control Flow and Data Flow Graphs to create Program Flow Graph (PFG)
def generate_pfg(cfg, dfg):
    pfg = nx.compose(cfg, dfg)
    return pfg

# Step 5: Visualize the Graphs
def visualize_graph(graph, output_file, layout_algorithm=nx.spring_layout):
    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Customize node appearance
    node_size = 200
    font_size = 10

    # Draw the graph using the specified layout algorithm
    pos = layout_algorithm(graph)
    nx.draw(graph, pos, with_labels=True, node_size=node_size, font_size=font_size, node_color='skyblue', font_color='black', ax=ax)

    # Save or display the figure
    plt.savefig(output_file, format='png', bbox_inches='tight', dpi=300)
    plt.show()


# Main function
if __name__ == '__main__':
    python_file = 'Fibonacci.py'

    # Step 1: Parse Python code
    ast_tree = parse_file(python_file)

    # Step 2: Generate Control Flow Graph (CFG)
    cfg = generate_cfg(ast_tree)
    visualize_graph(cfg, 'cfg.png', layout_algorithm=nx.kamada_kawai_layout)

    # Step 3: Generate Data Flow Graph (DFG)
    dfg = generate_dfg(ast_tree)
    visualize_graph(dfg, 'dfg.png', layout_algorithm=nx.kamada_kawai_layout)

    # Step 4: Generate Program Flow Graph (PFG)
    pfg = generate_pfg(cfg, dfg)
    visualize_graph(pfg, 'pfg.png', layout_algorithm=nx.kamada_kawai_layout)

from anytree import Node, RenderTree

from .funcs_registry import (
    get_7_days_status,
    get_top_5_users,
    print_summary,
    predict_session_duration,
    save_to_txt,
    exit_program,
    enter_user_id,
    enter_period
)

FUNCTIONS_REGISTRY = {
    'Get top 5 users based on time spent gaming': get_top_5_users,
    'Get status for the past 7 days': get_7_days_status,
    'Print summary': print_summary,
    'Predict next session duration': predict_session_duration,
    'Save summary to txt': save_to_txt,
    'Exit program': exit_program,
    'Enter user id': enter_user_id,
    'Enter period (yyyy-mm-dd yyyy-mm-dd)': enter_period,
}


class InteractiveTerminal:
    def __init__(self):
        self._create_tree_structure()

    def _create_tree_structure(self):
        self.root = Node('Choose one operation from below', children=[
            Node('Get top 5 users based on time spent gaming')
        ])

        status = Node('Get status for the past 7 days', parent=self.root)
        summary = Node('Print user summary', parent=self.root)
        Node(
            'Predict user next session duration', parent=self.root,
            children=[Node('Enter user id', children=[Node('Predict next session duration')])]
        )
        exit_terminal = Node('Exit the program', parent=self.root)

        user_id = Node('Enter user id', parent=summary)
        period = Node('Enter period (yyyy-mm-dd yyyy-mm-dd)', parent=user_id)
        Node('Print summary', parent=period)

        status_exit = Node(status.name, parent=exit_terminal)
        Node('Save summary ?', parent=status_exit, children=[
            Node('Save summary to txt', children=[Node('Exit program')]), Node('Exit program')
        ])

    def print_terminal_options(self) -> None:
        for indent, _, node in RenderTree(self.root):
            print(f"{indent}{node.name}")

    @staticmethod
    def print_children_of_current_node(node):
        print(f'{node.name}:')
        for idx, child in enumerate(node.children):
            print(f'\t{idx}. {child.name}')

    def start_session(self) -> None:
        current_node = self.root

        while True:
            if current_node.is_root or len(current_node.children) > 1:
                self.print_children_of_current_node(current_node)
                option = int(input())
            else:
                option = 0

            if current_node.children[option].is_leaf:
                FUNCTIONS_REGISTRY[current_node.children[option].name]()
                current_node = self.root
            elif current_node.children[option].is_root:
                current_node = current_node.children[option]
                self.print_children_of_current_node(current_node)
            else:
                current_node = current_node.children[option]
                if FUNCTIONS_REGISTRY.get(current_node.name):
                    print(current_node.name)
                    FUNCTIONS_REGISTRY[current_node.name]()

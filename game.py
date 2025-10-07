import json
import time

class Node:
    def __init__(self, description: str=None, is_death: bool=None, is_end: bool=None, **kargs):
        self.description = description
        self.options = [] # value as decision desc and key as ref to node
        self.next = []
        self.is_death = is_death
        self.is_end = is_end

    def __repr__(self):
        pass

    def print_description(self, w_t=0.05, max_line_char_cnt=80):
        # divide words into small chunk with char size of 100
        line_char_cnt = 0
        for word in self.description.split(' '):
            # when curr line have n chars change line
            if line_char_cnt >= max_line_char_cnt:
                line_char_cnt = 0
                print()
            
            line_char_cnt += len(word) + 1
            print(word, end=' ', flush=True)
            time.sleep(w_t)
        
        print('\n')

    def print_options(self):
        for i, option in enumerate(self.options):
            print(f"{i}) {option}")
        
        print()

class Game:
    def __init__(self, st_node: Node):
        self.st_node = st_node
        self.curr_node = st_node
        self.rem_life = 3
        self.name = "Placeholder player"
    
    def _traverse_nodes(self):
        """Print all nodes."""
        def helper(node, visited):
            if node in visited:
                return
            visited.add(node)
            print(node.description)
            print("Decisions")
            print(f"\t{node.options}\n")

            for n in node.next:
                helper(n, visited)
        helper(self.st_node, set())
    
    @staticmethod
    def generate_tree(path: str):
        "Creat a tree with story at each level and return head node."
        with open(path, 'r') as f:
            graph = json.load(f)

        visited = {}
        def helper(key):
            if key in visited:
                return visited[key]
            
            node = Node(**graph[key])

            items = graph[key]['decision'].items()
            for key, value in items:
                node.options.append(value)
                node.next.append(helper(key))
            visited[key] = node
            return node

        return helper('start')
    
    @classmethod
    def from_file(cls, path: str):
        """Generate tree then return a Game object."""
        start_node = cls.generate_tree(path)
        return cls(start_node)
    
    # def next_node(self):
    #     pass
    
    def get_name(self):
        self.name = input("Enter your name: ").strip()
        print()

    def get_user_response(self) -> int:
        """
        Take stdin user repsonse and return next node.
        """
        invalid_option = True
        while invalid_option:
            option = input(f"Take decision, options 0 to {len(self.curr_node.options)-1}: ").strip()
            if option.isdigit() and 0 <= int(option) < len(self.curr_node.options):
                invalid_option = False
            else:
                print("Input valid option...")
        print()
        return int(option)
    
    def get_user_decision(self) -> Node:
        """
        - Take user input, 
        - Verify input,
        - Decrement life on death
        - return next node
        - if all life ends return None
        """
        is_life_decremented = True
        while is_life_decremented and self.rem_life:
            self.curr_node.print_options()

            option = self.get_user_response()
            next_node = self.curr_node.next[option]

            if next_node.is_death:
                next_node.print_description()
                self.decrement_life()
            else:
                is_life_decremented = False
                
        if self.rem_life == 0:
            return None   
            
        return next_node
    
    def decrement_life(self):
        """Decrement life of player by 1 and notify in STDIN."""
        self.rem_life -= 1
        print(f"Your remaining life: {self.rem_life}\n")

    def start(self):
        """
        Start game 
        """
        user_won = False
        while True:
            self.curr_node.print_description()
            
            # is user won
            if self.curr_node.is_end:
                user_won = True
                break

            next_node = self.get_user_decision()

            if not next_node:
                user_won = False
                break

            self.curr_node = next_node
        
        # verify verification
        if user_won:
            print(f"{self.name}, Congratulation.")
        else:
            print(f"{self.name}, Game Over")
        
        print()

    def play_new_game(self) -> bool:
        """
        Ask user for playing new game.
        """
        response = input("Do you want to play new game?(y/n): ").strip()

        return response.lower().startswith('y')



if __name__ == '__main__':
    new_game = True

    while new_game:
        story_path = "story/dragon.json"
        game = Game.from_file(story_path)
        game.get_name()
        game.start()

        new_game = game.play_new_game()

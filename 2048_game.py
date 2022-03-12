from typing import List, Tuple, Dict, Callable
import random
import itertools
import os
class Grid:
    pass
class Game:
    def __init__(self, size:int) -> None:
        self.size = size
        self.grid = self._generate_init_grid()
        self.controls = ["w", "a", "s", "d"]
        self._game_over = False
        self._ending_score = 2048
        
        
    
    def play(self) -> str:
        self.grid = self._generate_init_grid()
        self._init_two_values_in_ranodm_cells()
        while not (self._game_over):
            self._clear_interface()
            self._update_grid()
            direction = self._ask_for_direction()
            msg = self._logic(direction)
            
        
        if self._is_start_another_game():
            self._game_over = False
            self.play()
        
        return msg
        
            
        
    @property
    def gesture_with_movement_function(self) -> Dict[str, Callable]:
        return {
            "w":Movements.up, 
            "a":Movements.left,
            "s":Movements.down, 
            "d":Movements.right 
        }
        
    def _logic(self, direction:str) -> str:
        grid_copy = self.grid.copy()
        gesture_with_movement_function:Dict[str, Callable] = self.gesture_with_movement_function
        movement_func = gesture_with_movement_function[direction]
        
        result_grid = movement_func(grid_copy)
        # check four movements to check if there is still a way to move in the grid.
        if result_grid == self.grid:
            if not self._can_move_in_four_grids():
                self._game_over = True
                return "You Can Not Move, Lose"
            
        
        
        if result_grid != self.grid:
            self.grid = result_grid
            if self._is_greater_than_ending_score():
                self._game_over = True
                return "You Win"
        
        self._put_value_in_random_cell()
        
        
    

    def _generate_init_grid(self) -> List[List[int]]:
        grid = []
        for row in range(self.size):
            temp_row = []
            for col in range(self.size):
                temp_row.append(0)
            grid.append(temp_row)
        return grid
    
    def _init_two_values_in_ranodm_cells(self) -> None:
        self._put_value_in_random_cell()
        self._put_value_in_random_cell()
    
    
    def _put_value_in_random_cell(self) -> None:
        all_grid_coords = self._get_available_cells_coords()
        number = random.choice([4, 2] * 30)
        x, y = random.choice(all_grid_coords)
        self.grid[x][y] = number
    def _can_move_in_four_grids(self) -> bool:
        four_movement_funcs = list(self.gesture_with_movement_function.values())
        four_result_grids = [movement_func(self.grid) 
                      for movement_func in four_movement_funcs]
        
        for grid in four_result_grids:
            if grid != self.grid:
                return True
            
        
        return False
    
    def _update_grid(self) -> None:
        # clear the command line interface
        os.system("clear")
        print("-" * (self.size * 6))
        for row in self.grid:
            print(f'|{"|".join([str(col or " ").center(5) for col in row])}|')
        print("-" * (self.size * 6))
        
    def _clear_interface(self) -> None:
        # clear the command line interface
        os.system("clear")
    
    def _ask_for_direction(self) -> str:
        while (True):
            input_direction = input("Please Enter Direction (W / A / S / D): ").lower()
            if input_direction in self.controls:
                return input_direction
        
        
    
    def _is_start_another_game(self) -> bool:
        while (True):
            want_to_start_another_game = input("Start another game? [Y/N]").lower()
            if want_to_start_another_game in ["y", "n"]:
                return True if want_to_start_another_game == "y" else False
    
        
    def _is_greater_than_ending_score(self) -> bool:
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] >= self._ending_score:
                    return True
            
        return False
        
    
    def _get_available_cells_coords(self) -> List[Tuple]:
        return [
            (x, y) 
            for x in range(self.size) 
            for y in range(self.size)
            if self.grid[x][y] == 0 # if grid content is 0, it is available
        ]

class Movements:
    @classmethod
    def up(cls, grid:Grid) -> Grid:
        #transpose -> go left -> traspose
        return cls.transpose(cls.left(cls.transpose(grid))) 
    
    @classmethod
    def down(cls, grid:Grid) -> Grid:
        #transpose -> go rigt -> transpose
        return cls.transpose(cls.right(cls.transpose(grid))) 
        
    @classmethod
    def left(cls,grid:Grid) -> Grid:
        summed_grid = [cls.left_sum(row) for row in grid]
        return summed_grid
        
    @classmethod
    def right(cls, grid:Grid) -> Grid:
        summed_grid = [cls.right_sum(row) for row in grid]
        return summed_grid

    
    @classmethod
    def trim(cls, row:List[int], direction) -> List[int]:
        non_0_numbers = [number for number in row if number != 0]
        offset_elements = [0] * len(row)
        if direction == "a":
            row = (non_0_numbers + offset_elements)[:len(row)]
        if direction =="d":
            row = (offset_elements + non_0_numbers)[-len(row):]

        return row

    @classmethod
    def left_sum(cls,row:List[int]) -> List[int]:
        row = cls.trim(row,"a")
        left = 0
        while left < len(row)-1:
            right = left + 1
            two_are_equal = (row[left] == row[right])
            two_are_not_zero = (row[left] and row[right])
            if two_are_equal and two_are_not_zero:
                row[left] = row[left] + row[right]
                row[right] = 0
            left += 1


        return cls.trim(row, "a")
    @classmethod
    def right_sum(cls,row:List[int]) -> List[int]:
        row = cls.trim(row,"d")
        right = len(row) -1 
        while (right > 0):
            left = right - 1
            two_are_equal = (row[left] == row[right])
            two_are_not_zero = (row[left] and row[right])
            if two_are_equal and two_are_not_zero:
                row[right] = row[right] + row[right]
                row[left] = 0
            right -= 1

        return cls.trim(row, "d")
    @classmethod
    def transpose(cls,grid:Grid) -> Grid:
        return [[row[col] 
                for row in grid] 
                for col in range(len(grid))]


if __name__ == "__main__":
  game = Game(size = 3)
  game.play()
from typing import List, Tuple
from heapq import heappush, heappop, heapify, heappushpop

class RunningMedian:
    
    def __init__(self, window_size: int, initial_data: List[int]) -> None:
        assert len(initial_data) == window_size
        self.window_size = window_size
        self.current_index = window_size
        self.max_heap: List[Tuple[int,int]] = []
        self.min_heap: List[Tuple[int,int]] = []
        self.max_heap_size = 0
        self.min_heap_size = 0
        self.current_window = initial_data
        
        for idx, el in enumerate(initial_data):
            self.add_element(el, idx)
        
    def get(self) -> float:
        if self.max_heap_size > self.min_heap_size:
            return -self.max_heap[0][0]
        return (self.min_heap[0][0] - self.max_heap[0][0])/2
        
    def add(self, new_el: int) -> None:
        self.remove_old()
        self.current_window[self.current_index%self.window_size] = new_el
        self.add_element(new_el, self.current_index)
        self.pop_old_elements()
        self.current_index += 1

        
    def remove_old(self) -> None:
        el_to_remove = self.current_window[self.current_index%self.window_size]
        idx_to_remove = self.current_index - self.window_size
        if (el_to_remove, idx_to_remove) >= self.min_heap[0]:
            self.min_heap_size -= 1
        else:
            self.max_heap_size -= 1

        self.pop_old_elements()
        if self.max_heap_size < self.min_heap_size:
            el_to_move, idx_to_move = heappop(self.min_heap)
            heappush(self.max_heap, (-el_to_move, idx_to_move))
            self.min_heap_size -= 1
            self.max_heap_size += 1
        self.pop_old_elements()
        
    def add_element(self, new_el: int, index: int) -> None:
        assert new_el >= 0
        
        if self.max_heap_size == 0:
            heappush(self.max_heap, (-new_el, index))
            self.max_heap_size += 1
        elif self.max_heap_size == self.min_heap_size:
            self.max_heap_size += 1
            if  new_el < self.min_heap[0][0]:
                heappush(self.max_heap, (-new_el, index))
            else:
                el_to_move, idx_to_move = heappushpop(self.min_heap, (new_el, index))
                heappush(self.max_heap, (-el_to_move, idx_to_move))
        else:
            self.min_heap_size += 1
            if new_el > -self.max_heap[0][0]:
                heappush(self.min_heap, (new_el, index))
            else:
                el_to_move, idx_to_move = heappushpop(self.max_heap, (-new_el, index))
                heappush(self.min_heap, (-el_to_move, idx_to_move))
            
        
    def pop_old_elements(self):
        while self.max_heap and self.max_heap[0][1] <= self.current_index - self.window_size:
            heappop(self.max_heap)
        while self.min_heap and self.min_heap[0][1] <= self.current_index - self.window_size:
            heappop(self.min_heap)

from tkinter import Canvas, Tk
from copy import deepcopy
import time
import random
from algorithms import insertionSort

# Draw some rectangles of varying size based on the window, then start swapping

def rankify(array):
    # Get the ranks of the array in the same order they appear, starting at 0
    # [5, 3, 4, 100, 2]
    # [3, 1, 2, 4, 0]
    b = deepcopy(array)
    b.sort()
    result = []
    for i in array:
        x = b.index(i)
        result.append(x + 1)   # Need + 1 for the indexing in canvas.shape creation
    return result
    
    

class SortingCanvas(Canvas):
    def __init__(self, master = None, **kw):
        super().__init__(master, kw)
        self.array = []
        self.spawned = 0

    def spawn_rectangles(self, n):
        """ Draw a n rectangles from left to right, with increasing height. """
        self.update()
        starting_x = 0
        starting_y = self.winfo_height()
        rect_width = self.winfo_width() / n
        original_rect_height = self.winfo_height() / n
        rect_height = self.winfo_height() / n

        for i in range(n):
            self.array.append(self.create_rectangle(starting_x, starting_y, starting_x + rect_width, starting_y - rect_height))
            #print(self.coords(a))
            # rectangle keeps getting taller, so you gotta change its starting coords and its height
            rect_height += original_rect_height
            starting_x += rect_width
        
        self.spawned = n
    
    def draw_rectangle(self, numerator, denominator, n):
        """ Let numerator be the nth shortest rectangle that we want to make.
            Let denominator be the total number of rectangles that we want.
            We will draw this rectangle at the nth position relative to the left. """
        self.update()
        starting_y = self.winfo_height()
        rect_width = self.winfo_width() / denominator
        starting_x = n * rect_width
        rect_height = self.winfo_height() * (numerator / denominator)
        self.array.append(self.create_rectangle(starting_x, starting_y, starting_x + rect_width, starting_y - rect_height, fill = "white"))
        self.spawned += 1



    def swap_rectangles(self, rect_index1, rect_index2):
        """ Swap rectangles based on their order on the graph.
            swap_rectangles(0, 2) swaps the first and third rectangles.
         """
        
        # Get the actual rectangle indexes that were made by tkinter
        tk_rect1_index = self.array[rect_index1]
        tk_rect2_index = self.array[rect_index2]
        #print(tk_rect1_index, tk_rect2_index, "indexes")
        rect1_x1, rect1_y1, rect1_x2, rect1_y2 = self.coords(tk_rect1_index)
        rect2_x1, rect2_y1, rect2_x2, rect2_y2 = self.coords(tk_rect2_index)

        x_distance_to_move = rect2_x1 - rect1_x1

        # second rectangle was to the left of the first, move it right
        if x_distance_to_move < 0:
            self.move(tk_rect2_index, -x_distance_to_move, 0)
            self.move(tk_rect1_index, x_distance_to_move, 0)
        else:
            # second rectangle was to the right of the first, move it left
            self.move(tk_rect1_index, x_distance_to_move, 0)
            self.move(tk_rect2_index, -x_distance_to_move, 0)

        self.array[rect_index1], self.array[rect_index2] = self.array[rect_index2], self.array[rect_index1]

    def insert_rectangle(self, rect_index, destination_index):
        # Actually never ended up using this
        """ Take the rectangle at rect_index and put it at destination_index, moving every other
            rectangle to the right. rect_index and destination_index are zero-indexed. """

        self.swap_rectangles(rect_index, destination_index)
        for i in range(rect_index, destination_index + 1, -1):
            # Swap the just swapped guy all the way back down next to the new destination guy
            #print(i)
            self.swap_rectangles(i, i - 1)



    def scramble_rectangles(self, unsorted_array):
        """ Before the canvas runs the sorting algorithm, it's gotta put the rectangles
            in the same order as the unsorted array of stuffs. """
        ordering = rankify(unsorted_array)
        length = len(ordering)
        for i in range(length):
            # Draw the rectangles based on their height relative to how many there are
            self.draw_rectangle(ordering[i], length, i)

    def animate_swaps(self, swaps):
        """ Given a list of two-tuples [(index1, index2), ...]
            where each tuple contains a swap, do all said swaps to the rectangles. """
        for pair in swaps:
            self.swap_rectangles(pair[0], pair[1])
            self.update()

    def done_animation(self):
        """ Show that the sorting is done with a special animation. """
        for rect in self.array:
            self.itemconfig(rect, fill = "cyan")
            self.after(1)
            self.update()

    def clear_screen(self):
        """ Clear the screen of rectangles. """
        for rect in self.array:
            #print("deleting", rect)
            self.delete(rect)
        self.array = []





def demonstration(sorting_canvas, algorithm):
    """ Shows how the Canvas works with any particular algorithm. Runs infinitely till the
        window is closed. """
    while True:
        # Generate some random data
        array = [random.randint(1, 10000) for x in range(200)]

        # Plot the array on the graph in terms of rectangles
        sorting_canvas.scramble_rectangles(array)

        # Use one of the sorts to get the swaps
        swaps = algorithm(array)

        # Animate the swaps
        sorting_canvas.animate_swaps(swaps)
        sorting_canvas.done_animation()
        sorting_canvas.clear_screen()



def main():
    tk = Tk()
    tk.geometry("800x400")
    sc = SortingCanvas(master = tk, bg = "black")
    sc.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    demonstration(sc, insertionSort)
    #insertion_sort_demonstration(sc, quickSort_helper)

    tk.mainloop()

if __name__ == "__main__":
    main()
from tkinter import Canvas, Tk


class DraggableCanvas(Canvas):
    def __init__(self, master = None, **kw):
        super().__init__(master, kw)
        self.bind("<Motion>", self.draw_stuff)
        self.horizontal = 0
        self.vertical = 0
        self.text = 0
        # Keep on deleting the shapes drawn
    
    def draw_stuff(self, event):
        self.draw_cursor(event)
        self.draw_location(event)
        self.update()


    def draw_cursor(self, event):
        self.delete(self.horizontal)
        self.delete(self.vertical)
        self.horizontal = self.create_line(0, event.y, self.winfo_width(), event.y)
        self.vertical = self.create_line(event.x, 0, event.x, self.winfo_height())

    def draw_location(self, event):
        self.delete(self.text)
        text = "(%d, %d)" % (event.x, event.y)
        print(text)
        self.text = self.create_text(event.x + 30, event.y - 10, text = text)


def main():
    tk = Tk()
    c = DraggableCanvas(master = tk, bg = "white")
    c.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
    tk.mainloop()

if __name__ == "__main__":
    main()
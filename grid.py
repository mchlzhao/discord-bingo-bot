class Grid:
    def __init__(self, num_rows, num_cols, box_width, box_height, padding_horizontal=1, padding_vertical=1):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.box_width = box_width+2*padding_horizontal
        self.box_height = box_height+2*padding_vertical
        self.padding_vertical = padding_vertical
        self.padding_horizontal = padding_horizontal

        self.grid = []
        self.init_grid()

    def init_grid(self):
        row = [' '] * (self.box_width*self.num_cols + self.num_cols-1)
        row_sep = ['-'] * (self.box_width*self.num_cols + self.num_cols-1)
        for i in range(self.box_width, self.box_width*self.num_cols + self.num_cols-1, self.box_width+1):
            row[i] = '|'
            row_sep[i] = '+'

        for r in range(self.num_rows):
            for x in range(self.box_height):
                self.grid.append(list(row))
            if r != self.num_rows-1:
                self.grid.append(list(row_sep))

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))
        print()

    def write_word_to_coord(self, word, x, y):
        for c in word:
            self.grid[x][y] = c
            y += 1

    def write_to_box(self, text, row, col):
        words = text.split()
        cur_r = row * (self.box_height+1) + self.padding_vertical
        cur_c = col * (self.box_width+1) + self.padding_horizontal
        rem = self.box_width-2*self.padding_horizontal
        for word in words:
            if rem < len(word):
                cur_r += 1
                cur_c = col * (self.box_width+1) + self.padding_horizontal
                rem = self.box_width-2*self.padding_horizontal
            self.write_word_to_coord(word, cur_r, cur_c)
            cur_c += len(word)+1
            rem -= len(word)+1

    def get_grid(self):
        return [[x for x in row] for row in self.grid]
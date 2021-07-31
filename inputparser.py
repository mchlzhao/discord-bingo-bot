import numpy
import pandas

class InputParser:
    def __init__(self, csv_file):
        self.df = pandas.read_csv(csv_file)

        self.lines = self.df['lines'].to_list()
        # ??? does map work with pandas DFs
        self.probs = list(
            map(float, self.df['probs'].to_list())
        )
        self.did_occur = list(
            map(lambda x: x == 'y', self.df['did_occur'].to_list())
        )

    def print_lines(self):
        for line in self.lines:
            print(line)

    def print_probs(self):
        for line, prob in zip(self.lines, self.probs):
            print(prob, line)

    def print_did_occur(self):
        for line, did in zip(self.lines, self.did_occur):
            print('+' if did else '-', line)

    def print_df(self):
        print(self.df)

    def get_lines(self):
        return list(self.lines)

    def get_probs(self):
        return list(self.probs)

    def get_did_occur(self):
        return list(self.did_occur)

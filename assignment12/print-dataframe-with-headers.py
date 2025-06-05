# Task 5: Extending a Class
import pandas as pd

class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)

    def print_with_headers(self):
        n = len(self)
        for i in range(0, n, 10):
            print("\nColumn Headers:", list(self.columns))
            print(self.iloc[i:i+10])

if __name__ == "__main__":
    dfp = DFPlus.from_csv("../csv/products.csv")
    dfp.print_with_headers()
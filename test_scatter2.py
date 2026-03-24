import pandas as pd
try:
    books = pd.read_csv('dissertation/full_book_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    books = pd.read_csv('full_book_data_feb_25.csv', low_memory=False)
print("Books columns:", books.columns.tolist())

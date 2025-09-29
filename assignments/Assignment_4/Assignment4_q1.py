import sqlite3
import pandas as pd

# File paths
EXCEL_FILE = "Online Retail.xlsx"     # your Excel dataset file
DB_FILE = "online_retail.db"         # database file (SQLite)

# Read Excel file (first sheet by default)
df = pd.read_excel(EXCEL_FILE)

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# --- Step 1: Create tables ---
cur.execute("DROP TABLE IF EXISTS Countries")
cur.execute("DROP TABLE IF EXISTS Customers")
cur.execute("DROP TABLE IF EXISTS Products")
cur.execute("DROP TABLE IF EXISTS Invoices")
cur.execute("DROP TABLE IF EXISTS InvoiceLines")

cur.execute("""
CREATE TABLE Countries (
    CountryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CountryName TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY,
    CountryID INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
)
""")

cur.execute("""
CREATE TABLE Products (
    StockCode TEXT PRIMARY KEY,
    Description TEXT
)
""")

cur.execute("""
CREATE TABLE Invoices (
    InvoiceNo TEXT PRIMARY KEY,
    InvoiceDate TEXT,
    CustomerID INTEGER,
    InvoiceCancelled INTEGER,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
)
""")

cur.execute("""
CREATE TABLE InvoiceLines (
    InvoiceLineID INTEGER PRIMARY KEY AUTOINCREMENT,
    InvoiceNo TEXT,
    StockCode TEXT,
    Quantity INTEGER,
    UnitPrice REAL,
    FOREIGN KEY (InvoiceNo) REFERENCES Invoices(InvoiceNo),
    FOREIGN KEY (StockCode) REFERENCES Products(StockCode)
)
""")

conn.commit()

# --- Step 2: Insert first 1000 rows from Excel ---
count = 0
for _, row in df.iterrows():
    if count >= 1000:   # stop after 1000 rows
        break

    invoice_no = str(row["InvoiceNo"])
    stock_code = str(row["StockCode"])
    desc = str(row["Description"])
    qty = int(row["Quantity"])
    invoice_date = str(row["InvoiceDate"])
    price = float(row["UnitPrice"])
    cust_id = None if pd.isna(row["CustomerID"]) else int(row["CustomerID"])
    country = str(row["Country"])

    # Insert into Countries
    cur.execute("INSERT OR IGNORE INTO Countries (CountryName) VALUES (?)", (country,))
    cur.execute("SELECT CountryID FROM Countries WHERE CountryName=?", (country,))
    country_id = cur.fetchone()[0]

    # Insert into Customers
    if cust_id:
        cur.execute("INSERT OR IGNORE INTO Customers (CustomerID, CountryID) VALUES (?, ?)",
                    (cust_id, country_id))

    # Insert into Products
    cur.execute("INSERT OR IGNORE INTO Products (StockCode, Description) VALUES (?, ?)",
                (stock_code, desc))

    # Insert into Invoices
    cancelled = 1 if invoice_no.startswith("C") or qty < 0 else 0
    cur.execute("INSERT OR IGNORE INTO Invoices (InvoiceNo, InvoiceDate, CustomerID, InvoiceCancelled) VALUES (?, ?, ?, ?)",
                (invoice_no, invoice_date, cust_id, cancelled))

    # Insert into InvoiceLines
    cur.execute("INSERT INTO InvoiceLines (InvoiceNo, StockCode, Quantity, UnitPrice) VALUES (?, ?, ?, ?)",
                (invoice_no, stock_code, qty, price))

    count += 1

conn.commit()
conn.close()

print("✅ Done! Inserted", count, "rows into", DB_FILE)

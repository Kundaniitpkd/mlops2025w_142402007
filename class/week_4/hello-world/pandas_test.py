#import pandas as pd
import pandas as pd

# Create a toy dataset using a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'Score': [85.5, 92.0, 88.0, 76.5]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Show the DataFrame
print(df)


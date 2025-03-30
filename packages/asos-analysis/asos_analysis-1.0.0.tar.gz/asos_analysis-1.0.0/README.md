### **README.md**

# ASOS Analysis

ASOS Analysis is a Python library designed to streamline the sorting, cleaning, and analysis of ASOS (Automated Surface Observing System) weather data. It provides tools for sorting data by time, stations, and variables, detecting and standardizing date-time formats, and removing duplicate entries.

---

## Features

- **Sorting:**
  - Group and save data by time (hourly intervals).
  - Group and save data by station.
  - Extract data for specific variables and save them in individual files.

- **Cleaning:**
  - Remove duplicate entries from datasets.

- **Date-Time Management:**
  - Detect unique date-time formats used in data files.
  - Standardize all date-time values into a consistent format.

- **Flexible and Modular Design:**
  - Customizable options for handling ASOS datasets with ease.

---

## Installation

ASOS Analysis is available via both **pip** and **conda**.

### Using `pip`:
```bash
pip install asos_analysis
```

### Using `conda`:
```bash
conda install -c sauravshuvo asos_analysis
```

---

## Usage

Here's how to use ASOS Analysis for various tasks. Import the required functions and call them with your dataset paths.

### Sorting Data by Time
Sort data into hourly intervals and save each interval into a separate file:
```python
from asos_analysis.sorting import sort_by_time

input_file = "path/to/ND_feb12.csv"
output_dir = "path/to/Hourly_Files"

sort_by_time(input_file, output_dir)
```

### Sorting Data by Stations
Organize data by stations and save each station's data into a separate file:
```python
from asos_analysis.sorting import sort_by_station

input_file = "path/to/ND_feb12.csv"
output_dir = "path/to/Station_Files"

sort_by_station(input_file, output_dir)
```

### Sorting Data by Variables
Extract data for specific variables:
```python
from asos_analysis.sorting import sort_by_variable

input_file = "path/to/ND_feb12.csv"
variables = ['tmpf', 'dwpf', 'relh']
base_columns = ['station', 'valid', 'lon', 'lat', 'elevation']
output_dir = "path/to/Variables_Files"

sort_by_variable(input_file, variables, base_columns, output_dir)
```

### Removing Duplicate Entries
Clean your datasets by removing duplicate rows:
```python
from asos_analysis.cleaning import remove_duplicates

input_folder = "path/to/data_folder"
remove_duplicates(input_folder)
```

### Listing Unique Date-Time Formats
Analyze your datasets to find all unique date-time formats in the `valid` column:
```python
from asos_analysis.formats import list_unique_formats

input_folder = "path/to/data_folder"
unique_formats = list_unique_formats(input_folder)

print("Unique date-time formats detected:")
for fmt in unique_formats:
    print(fmt)
```

### Standardizing Date-Time Format
Ensure all date-time values in the `valid` column conform to a standard format:
```python
from asos_analysis.reformat import standardize_datetime

input_folder = "path/to/data_folder"
standardize_datetime(input_folder)
```

---

## Contributing

Contributions are welcome! Feel free to fork the repository, create a branch, and submit pull requests. You can also report issues or feature requests on the [GitHub repository](https://github.com/sauravshuvo/asos_analysis).

---

## License

This project is licensed under the MIT License. See the [LICENSE] file for more details.
```


import csv

# ==========================================================
# Function for reading a CSV file into a dictionary format
# ==========================================================


def read_variables_csv(csvfile):
    """
    Builds a Python dictionary object from an input CSV file.
    Helper function to read a CSV file on the disk, where user stores the limits/ranges of the process variables.
    Output of this function can be used directly with any DOE builder function
    The CSV file should be in the same directory
    """
    dict_key = {}
    try:
        with open(csvfile) as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            for field in fields:
                lst = []
                with open(csvfile) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        lst.append(float(row[field]))
                dict_key[field] = lst

        return dict_key
    except:
        print(
            "Error in reading the specified file from the disk. Please make sure it is in current directory."
        )
        return -1


# ===============================================================
# Function for writing the design matrix into an output CSV file
# ===============================================================


def write_csv(df, filename, rounding=2):
    """
    Writes a CSV file on to the disk from the computed design matrix
    filename: To be specified by the user. Just a name is fine. .CSV extension will be added automatically.
    rounding: Number up to which decimal the output will be rounded off. Often needed for practical DOE plans.
    """
    df_copy = round(df, rounding)
    try:
        if ".csv" not in filename:
            filename = filename + ".csv"
        f = df_copy.to_csv(filename, index=False)
        return f
    except:
        return -1

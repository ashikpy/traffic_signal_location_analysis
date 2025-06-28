from tkinter.filedialog import askopenfilename


def main():
    number_of_csvs = int(input("Enter the number of files to merge: "))
    file_paths = []
    for i in range(number_of_csvs):
        file_path = askopenfilename(
            title=f"Select CSV File {i + 1}",
            filetypes=[("CSV files", "*.csv")],
        )
        if file_path:
            file_paths.append(file_path)

    # check if all the csvs have the same columns
    if not file_paths:
        print("No files selected.")
        return
    first_file_columns = None
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            columns = f.readline().strip().split(',')
            if first_file_columns is None:
                first_file_columns = columns
            elif first_file_columns != columns:
                print(
                    f"File {file_path} has different columns than the first file.")
                return

    print("All files have the same columns.")
    print("Selected file paths:")
    for file_path in file_paths:
        print(file_path)

    # Merge the CSV files

    merged_data = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            header = f.readline().strip()
            if not merged_data:
                merged_data.append(header)
            for line in f:
                merged_data.append(line.strip())

    merged_file_path = "merged_data.csv"
    with open(merged_file_path, 'w') as f:
        for line in merged_data:
            f.write(line + '\n')

    print(f"Merged CSV file created at: {merged_file_path}")


if __name__ == "__main__":
    main()

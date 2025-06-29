import glob
import tabulate


def tabulate_files(dir_path, target_ext) -> tuple:
    # List all files with the given extension
    matched_files = glob.glob(f"{dir_path}/*.{target_ext}")

    # Prepare rows with index for tabulation
    table_rows = [[i, file] for i, file in enumerate(matched_files)]
    tabulated = tabulate.tabulate(
        table_rows, headers=["Index", "File Name"], tablefmt="grid")

    return matched_files, tabulated

import csv

"""
Takes a CSV voucher list from OPNsense and 
"""
def concat_credentials(input_path, output_path):
    with open(input_path, newline="") as f_in, open(output_path, "w", newline="") as f_out:
        writer = csv.writer(f_out)
        for row in csv.DictReader(f_in):
            writer.writerow([row["username"] + row["password"]])

if __name__ == "__main__":
    import sys
    concat_credentials(sys.argv[1], sys.argv[2])
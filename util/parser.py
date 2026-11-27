import csv


def concat_credentials(input_path):
    """
    Takes a CSV voucher list from OPNsense and combines the username & password columns, while deleting everything else

    :param input_path: relative path of the exported OPNsense voucher list
    :return: None
    """
    with open(input_path, newline="") as f_in, open("vouchers.csv", "w", newline="") as f_out:
        writer = csv.writer(f_out)
        for row in csv.DictReader(f_in):
            writer.writerow([row["username"] + row["password"]])

if __name__ == "__main__":
    import sys
    concat_credentials(sys.argv[1])
"""
  This could eventually be made more generic instead of assuming input structure.
  This code should be concerned with how* to store data, not the signature of that data.
"""
import csv as CSV


def csv(records: [], out_file: str, newline: str, delimiter: str) -> bool:
    with open(out_file, "w", newline=newline) as csvfile:
        writer = CSV.writer(csvfile, delimiter=delimiter, quoting=CSV.QUOTE_MINIMAL)

        for r in records:
            writer.writerow([r["post_id"], r["name"], r["post_date"], r["post_body"]])

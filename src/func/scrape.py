"""
  Designed to extract from known sources anonymously.
  Each execution is meant to be a *single unit of work*.
  This keeps the core process simple and pure.
  It is possible to chunk the work by handling N pages as well,
  but this is only desireable as a future optimization.
"""

import json
from lib import transform


def run(event, context) -> []:
    """
    test
    """

    # Steps 1 & 2 in the diagram
    # Identify target(s) from new Target-Manifest event
    # The (uncreated) scout process will handle discovery of viable pages
    # and create events that result in the following payload reaching this scrape process
    targets = json.loads(event["targets"])
    shape = event["transform"]
    protocol = event["extract"]

    records = []
    for target in targets:
        print(
            f"Target with shape {shape} will be gathered using protocol {protocol}: {target}"
        )

        print("Step 3:: scrape/extract from target")
        extract_func = getattr(context.extract, protocol)
        raw = extract_func(target)

        print("Step 4:: backup/snapshot")  # sprint N story abc

        print("Step 5:: parse")
        transform_func = getattr(transform, shape)
        records = records + transform_func(raw)

    print(f"Step 6:: saving {len(records)} records")

    if not context.var.get("skip_db"):
        prepare_func = getattr(transform, f"mysql_{shape}")
        insert_statement = context.var.insert_statement
        context.rds.executemany(insert_statement, prepare_func(records))

    if context.var.get("out_file") and context.var.get("serializer"):
        print(
            f"serializing results as {context.var.serializer}:: {context.var.out_file}"
        )
        serialize_func = getattr(context.serialize, context.var.serializer)
        serialize_func(
            records, context.var.out_file, context.var.newline, context.var.delimiter
        )

    print("done")
    return records

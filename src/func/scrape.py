'''
  Designed to extract from known anonymous sources.
'''

import csv
from lib import transform


def run(event, context):
  '''
    Business logic lives here.
  '''

  # Identify target from new Target-Manifest event
  target = event['target']
  shape = event['transform']
  protocol = event['extract']

  print(f'Target with shape {shape} will be gathered using protocol {protocol}: {target}')

  print('Step 3:: scrape/extract from target')
  extract_func = getattr(context.extract, protocol)
  raw = extract_func(target)

  print('Step 4:: backup/snapshot')

  print('Step 5:: parse')
  transform_func = getattr(transform, shape)
  records = transform_func(raw)

  print(f'Step 6:: saving {len(records)}')
  prepare_func = getattr(transform, f'mysql_{shape}')
  insert_statement = context.var.insert_statement
  context.rds.executemany(insert_statement, prepare_func(records))

  if context.var.get('out_file'):
    cereal_format = 'csv'
    print(f'serializing results as {cereal_format}:: {context.var.out_file}')
    with open(context.var.out_file, 'w', newline=context.var.newline) as csvfile:
      writer = csv.writer(
        csvfile,
        delimiter=context.var.delimiter,
        quoting=csv.QUOTE_MINIMAL
      )

      for r in records:
        writer.writerow([
          r['post_id'],
          r['name'],
          r['post_date'],
          r['post_body']
        ])

  print('done')
  return records

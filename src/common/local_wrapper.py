'''
  This wrapper script takes in real/fake values for prod/testing respectively.
'''
import traceback

import configargparse
from box import Box

from context import CustomContext
from func import run


def main(args):
  '''
    The entry point for local runs or container runs
  '''
  args = remove_blank_args(args)

  event = {
    'targets': args['targets'],
    'extract': args['target_protocol'],
    'transform': args['target_shape'],
  }

  with CustomContext(args) as custom_context:
    print(event)
    try:
      run(event, custom_context)
    except Exception as e:
      traceback.print_tb(e.__traceback__)

def remove_blank_args(args):
  '''
    We want the argument behaviour to emulate aws lambda and aws ECS.
    So if a value is unset, we want it to not exist as a key starting out.
    A downstream step will populate any missing values to sane default values.
  '''
  clean = {}
  for prop in args:
    if not args[prop] is None:
      clean[prop] = args[prop]
  return Box(clean)

if __name__ == '__main__':
  P = configargparse.ArgumentParser()

  P.add_argument('--region', type=str, env_var='AWS_DEFAULT_REGION', default='us-east-1')
  P.add_argument('--const_path', type=str, default='./const.yml')

  P.add_argument('--s3_endpoint', env_var='S3_ENDPOINT', type=str, default='http://localhost:4572')
  P.add_argument('--raw_bucket', env_var='S3_RAW_BUCKET', type=str, default='raw-data')

  P.add_argument('--skip_db', action='store_true')
  P.add_argument('--db_host', env_var='DB_HOST', type=str, default='localhost')
  P.add_argument('--db_port', env_var='DB_PORT', type=int, default=3306)
  P.add_argument('--db_name', env_var='DB_NAME', type=str, default='optimal')
  P.add_argument('--db_user', env_var='DB_USER', type=str, default='root')
  P.add_argument('--db_pass', env_var='DB_PASS', type=str, default='password')

  P.add_argument('--targets', type=str)
  P.add_argument('--target_shape', type=str)
  P.add_argument('--target_protocol', type=str)

  P.add_argument('--newline', type=str)
  P.add_argument('--delimiter', type=str)
  P.add_argument('--insert_statement', type=str)

  P.add_argument('--out_file', type=str)
  P.add_argument('--serializer', type=str, default='csv')

  main(P.parse_args(namespace=Box()))

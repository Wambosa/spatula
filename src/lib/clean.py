import re

'''
  Specifically cleans out junk found in post bodies.
  This strips out the signature at the moment.
'''
def php_bb_post(body):
  return re.sub(r'_________________(.|\s)*', '', body)

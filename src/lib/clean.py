import re

'''
  Specifically cleans out junk found in various text bodies
'''
def php_bb_post(body):
  return re.sub(r'_________________(.|\s)*', '', body)

'''
  Handles the retrieval of data.
'''
import requests


'''
  A simple anonymous http download.
'''
def html(url: str, client = requests) -> str:
  res = client.get(url)
  # todo: pretty error on bad res.status_code
  return res.text

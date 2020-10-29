"""
  Handles the transformation of some data into desireable format.
  NOTE: move into own repository and publish a lib with this logic.
"""
import re
import arrow
from bs4 import BeautifulSoup

from lib import clean

SERIALIZED_TIMESTAMP = "YYYY-MM-DD HH:mm:ss"

PHP_BB_BODY_DEPTH = 15
PHP_BB_ID = re.compile('.*name="(?P<post_id>\d{5,})".*')
PHP_BB_NAME = re.compile(".*\<b\>(?P<user_name>.*)\<\/b\>.*")
PHP_BB_DATE = re.compile(
    "^Posted:\s\w\w\w\s(?P<post_date>\w\w\w\s\d\d\,\s\d\d\d\d\s(\d|:){3,5}\s\wm)"
)
PHP_BB_DATE_PARSE = "MMM DD, YYYY H:mm A"

"""
  Understands a specific site shape and knows how to extract desired features.

  NOTE: B This strips out any quoted sections.
  We don't want to keep a quoted section in the users post.
  We should instead ammend the features we extract to include a quote_id which would reference another post_id.
  This can be a future part of sprint N story SPAT-556789.
"""


def php_bb(raw: str, encoding="utf-8", parser="html.parser") -> []:
    soup = BeautifulSoup(raw, parser, from_encoding=encoding)

    whos = [str(info) for info in soup.find_all("span", "name")]
    whos_length = len(whos)

    whens = [text.string for text in soup.find_all(string=PHP_BB_DATE)]
    whens_length = len(whens)

    # NOTE: B
    # this line causes the quoted section to be omitted
    is_original = lambda el: el.contents and len(list(el.parents)) == PHP_BB_BODY_DEPTH

    whats = [
        span.text for span in soup.find_all("span", "postbody") if is_original(span)
    ]
    whats = list(filter(lambda w: len(w), map(clean.php_bb_post, whats)))
    whats_length = len(whats)

    print(f"NAME: {whos_length}")
    print(f"DATE: {whens_length}")
    print(f"BODY: {whats_length}")

    all_equal = whos_length == whens_length and whos_length == whats_length

    if not all_equal:
        raise "transform.php_bb feature count mismatch, number of posts does not match post content."

    records = []
    for i in range(whos_length):
        post_id = PHP_BB_ID.match(whos[i]).group("post_id")
        name = PHP_BB_NAME.match(whos[i]).group("user_name")
        post_date = PHP_BB_DATE.match(whens[i]).group("post_date")
        timestamp = arrow.get(post_date, PHP_BB_DATE_PARSE).format(SERIALIZED_TIMESTAMP)
        post_body = whats[i]

        records.append(
            {
                "post_id": post_id,
                "name": name,
                "post_date": timestamp,
                "post_body": post_body,
                # quote_id: 'todo'
            }
        )

    return records


"""
  If the app is configured to save to optimal datastore mysql,
  then this transformation will make it compatible with parameterized queries.
"""


def mysql_php_bb(records: []) -> []:
    return [(r["post_id"], r["name"], r["post_date"], r["post_body"]) for r in records]

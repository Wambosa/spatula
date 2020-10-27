import sys
import unittest
sys.path.append('./tests')
sys.path.append('./src')
sys.path.append('./src/func')

from lib import transform

def test_GIVEN_known_php_bb_id_signature_WHEN_searching_for_post_id_THEN_expect_5_digit_number():
  text = '<span class="name"><a name="87120"></a><b>Vegeta</b></span>'
  assert transform.PHP_BB_ID.match(text).group('post_id') == '87120'


def test_GIVEN_known_php_bb_name_signature_WHEN_searching_for_username_THEN_expect_name_string():
  text = '<span class="name"><a name="99999"></a><b>deku</b></span>'
  assert transform.PHP_BB_NAME.match(text).group('user_name') == 'deku'


def test_GIVEN_known_php_bb_date_signature_WHEN_searching_for_post_date_THEN_expect_date_string():
  text = 'Posted: Mon Sep 24, 2012 4:53 pm    Post subject: Dangerous Jamboree'
  assert transform.PHP_BB_DATE.match(text).group('post_date') == 'Sep 24, 2012 4:53 pm'

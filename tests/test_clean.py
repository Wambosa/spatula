import sys
import unittest

sys.path.append("./tests")
sys.path.append("./src")
sys.path.append("./src/func")

from lib import clean


def test_GIVEN_consistent_php_bb_signature_pattern_WHEN_removing_signature_THEN_expect_plain_post_body():
    assert (
        clean.php_bb_post(
            "out of curiosity_________________Rick (OCC Admin) Various..."
        )
        == "out of curiosity"
    )

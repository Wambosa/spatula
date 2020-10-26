import sys
import unittest
sys.path.append('./tests')
sys.path.append('./src')
sys.path.append('./src/func')

from scrape import run
from context import UnitContext


class GIVEN_known_html_target(unittest.TestCase):
  def test_WHEN_executing_scrape_flow_THEN_expect_minimum_features_within_records(self):
    event = {
      'target': 'fake-target-for-unit',
      'extract': 'html',
      'transform': 'php_bb'
    }

    records = run(event, UnitContext())
    # todo: good use-case for snapshots
    self.assertSequenceEqual(records, [
      {
          "post_id": "87120",
          "name": "Rick",
          "post_date": "2012-09-24 16:53:00",
          "post_body": "Tonight, 8pm, might be worth a look...?\n\n\nRJ",
      },
      {
          "post_id": "87131",
          "name": "pigtin",
          "post_date": "2012-09-24 20:29:00",
          "post_body": "Oh dear! Just switched off... a couple of geezers on an ego trip, couldn't take any more when they picked up the shock absorber in the breakers yard. Would you want to sell a classic at a knockdown price to this guy?",
      },
      {
          "post_id": "87133",
          "name": "Riley Blue",
          "post_date": "2012-09-24 20:47:00",
          "post_body": "What a terrible programme. Why on earth did the production company choose that foul mouthed cockney bodger to front it? I'll watch this one until the bitter end out of curiousity but that's it for me, no more of this rubbish.",
      },
      {
          "post_id": "87135",
          "name": "47p2",
          "post_date": "2012-09-24 21:00:00",
          "post_body": "I've recorded it to watch later, I might give it a miss now  ",
      },
      {
          "post_id": "87136",
          "name": "Rick",
          "post_date": "2012-09-24 21:04:00",
          "post_body": 'Deary me, "restore" something and leave that awful glass pop-up sunroof in it, not to mention the junk they bought from the other fella. Good to hear that they repaired a piston, and cleaned out the cylinders though ... \n\n\n£30k?\n\n\nRJ\n\n\nI\'ll probably watch the next one though, out of curiosity',
      },
      {
          "post_id": "87139",
          "name": "welshrover",
          "post_date": "2012-09-24 21:09:00",
          "post_body": "what a load of rubbish .arthur daley would have done a better job . poxy modern sunroof ,nice pinky red paint then bangs it into an engine .would you buy a car from these two plonkers . ",
      },
      {
          "post_id": "87140",
          "name": "welshrover",
          "post_date": "2012-09-24 21:10:00",
          "post_body": "\n\ni wouldn't bother. ",
      },
      {
          "post_id": "87142",
          "name": "swampy",
          "post_date": "2012-09-24 22:02:00",
          "post_body": "One and half days to sort out the 'too much oil in the carb' issue just after he had boasted that he'd been doing this for thirty something years   I can truly say that I was awestruck ",
      },
      {
          "post_id": "87146",
          "name": "welshrover",
          "post_date": "2012-09-24 22:31:00",
          "post_body": "those diagprahms in the carbs looked new too.",
      },
      {
          "post_id": "87148",
          "name": "Penman",
          "post_date": "2012-09-25 00:34:00",
          "post_body": "Hi\n\nThe e type was the first car designed using a wind tunnel??\n\nI think not, Bristol Cars used Bristol Aeroplane's wind tunnel in the design stages of the 401 introduced in 1948.",
      },
      {
          "post_id": "87149",
          "name": "victor 101",
          "post_date": "2012-09-25 01:34:00",
          "post_body": "I turned off before it was half way through, about where he pulled some supposedly E type parts of the back of a pick up truck.",
      },
      {
          "post_id": "87151",
          "name": "Peter_L",
          "post_date": "2012-09-25 04:28:00",
          "post_body": '\n\n\nand as far back as 1934 Chrysler used the wind tunnel for their "Airflow" series.   \n\n\nI haven\'t seen the programme that is the subject of this thread, but poorly researched and gross presentations are quite common this side of the "pond"',
      },
      {
          "post_id": "87154",
          "name": "pigtin",
          "post_date": "2012-09-25 06:41:00",
          "post_body": "It was dumbed down to a point where I thought I'd switched on Eastenders by mistake. I believe there are a load of 'Toff' producers with a very strange idea about what many of us 'Plebs' like to watch. Surely they could have asked someone who knew about restorations to look it over.\n\nHaving switched off before halfway through I can only assume, from comments on here, the programme didn't redeem itself in the second half...",
      },
      {
          "post_id": "87156",
          "name": "Riley Blue",
          "post_date": "2012-09-25 07:21:00",
          "post_body": "Make your opinion known - I have-\n\n\ncustomerservices@channel5.com",
      },
      {
          "post_id": "87157",
          "name": "Rick",
          "post_date": "2012-09-25 07:41:00",
          "post_body": "Times like this I wish I had shares in Isopon \n\n\nRJ",
      },
    ])

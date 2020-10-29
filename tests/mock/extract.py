"""
  Some mock data extraction.
"""


def html(_, always_return="./tests/mock/target/classic_car.html"):
    with open(always_return, "rb") as file:
        return file.read()

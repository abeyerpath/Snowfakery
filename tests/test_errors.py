from io import StringIO
import unittest

from snowfakery.data_generator import generate
from snowfakery.data_gen_exceptions import (
    DataGenSyntaxError,
    DataGenNameError,
    DataGenError,
)

yaml1 = """                             #1
- object: A                             #2
  count: ${{abcd()}}                     #3
  fields:                               #4
    A: What a wonderful life            #5
    X: Y                                #6
    """

yaml2 = """- object: B                  #1
  count: ${{expr)>                       #2
  fields:                               #3
    A: What a wonderful life            #4
    X: Y                                #5
"""

yaml3 = """
- object: B                             #2
  count: 5                              #3
  fields:                               #4
    A: What a wonderful life            #5
    X:                                  #6
        xyzzy: abcde                    #7
"""


class TestErrors(unittest.TestCase):
    def test_name_error(self):
        with self.assertRaises(DataGenNameError) as e:
            generate(StringIO(yaml1), {}, None)
        assert str(e.exception)[-2:] == ":3"

    def test_syntax_error(self):
        with self.assertRaises(DataGenSyntaxError) as e:
            generate(StringIO(yaml2), {}, None)
        assert str(e.exception)[-2:] == ":2"

    def test_funcname_error(self):
        with self.assertRaises(DataGenError) as e:
            generate(StringIO(yaml3))
        assert "xyzzy" in str(e.exception)
        assert e.exception.line_num >= 5

    def test_conflicting_declarations_error(self):
        yaml = """
        - object: B                             #2
          macro: C                              #3
          fields:                               #4
            A: What a wonderful life            #5
            X:                                  #6
                xyzzy: abcde                    #7
        """
        with self.assertRaises(DataGenError) as e:
            generate(StringIO(yaml))
        assert 4 > e.exception.line_num >= 2

    def test_extra_keys(self):
        yaml = """
        - object: B                             #2
          velcro: C                             #3
          fields:                               #4
            A: What a wonderful life            #5
            X:                                  #6
                xyzzy: abcde                    #7
        """
        with self.assertRaises(DataGenError) as e:
            generate(StringIO(yaml))
        assert 4 > e.exception.line_num >= 2

    def test_missing_param(self):
        yaml = """
            - object: Person
              count: 5
              fields:
                gender: Male
                name:
                    fake:
        """
        with self.assertRaises(DataGenError) as e:
            generate(StringIO(yaml))
        assert "Cannot evaluate function" in str(e.exception)
        assert ":6" in str(e.exception)

    def test_yaml_error(self):
        yaml = """
        - object: B                             #2
            velcro: C                             #3
        """
        with self.assertRaises(DataGenSyntaxError) as e:
            generate(StringIO(yaml), {}, None)
        assert str(e.exception)[-2:] == ":2"

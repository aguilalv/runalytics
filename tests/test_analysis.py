import pytest
from unittest.mock import patch 
import pandas as pd
#import numpy as np

import tests.fixtures_analysis

import runalytics.analysis

class TestTrimp(object):
    """Tests for function trimp"""

    def test_xxx(self):
        with patch('runalytics.helpers.JustleticUser') as mock:
            instance = mock.return_value
            instance.activity.return_value = pd.DataFrame(tests.fixtures_analysis.ACTIVITY_ONE['data'])
            
            user = runalytics.helpers.JustleticUser(2)
            act = user.activity(0)

            assert runalytics.analysis.trimp(act,80,185) == tests.fixtures_analysis.ACTIVITY_ONE['trimp']       

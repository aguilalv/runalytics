import os
import pytest

import runalytics.helpers

#class TestGetUserTokens(object):
#    """Tests for get_user_tokens helper method"""

@pytest.fixture
def delete_admin_env_variable():
    del os.environ['JUSTLETIC_ADMIN_TOKEN']

def test_raise_exception_if_no_token_environment_variable(
    delete_admin_env_variable
):

    with pytest.raises(EnvironmentError) as exception_info:
        runalytics.helpers.get_user_tokens()
    assert 'JUSTLETIC_ADMIN_TOKEN not set' in str(exception_info.value)
#    print(os.environ.get('JUSTLETIC_ADMIN_TOKEN')) 
#    pytest.fail('Finish this test')

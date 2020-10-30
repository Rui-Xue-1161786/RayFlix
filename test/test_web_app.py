import pytest

from authentication.services import AuthenticationException

from authentication import services as auth_services
from datafilereaders.memory_repository import MemoryRepository
from watching.services import NonExistentArticleException


@pytest.fixture
def in_memory_repo():
    file_path = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
    repo = MemoryRepository(file_path)
    return repo

def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')




def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


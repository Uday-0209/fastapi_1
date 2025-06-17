import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    

def test_is_instance():
    assert isinstance('this is strin', str)
    assert not isinstance('10', int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hellow' == 'world') is False

def test_greater_or_less_than():
    assert 7 > 4
    assert 8 > 1

class Students:
    def __init__(self, first_name:str, last_name:str, major:str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Students('uday', 'Hiremath', 'Datascience', 3)

def test_person_initialization(default_employee):
    #p = Students('uday', 'Hiremath', 'Datascience', 3)
    assert default_employee.first_name == 'uday', 'first name should be Uday'
    assert default_employee.last_name == 'Hiremath'
    assert default_employee.major == 'Datascience'
    assert default_employee.years == 3
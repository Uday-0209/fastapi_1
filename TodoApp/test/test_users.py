from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithuk'
    assert response.json()['email'] == 'udayhiremath02@gmail.com'
    assert response.json()['first_name'] == 'Uday'
    assert response.json()['last_name'] == 'Hiremath'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '8310215305'

def test_change_the_password(test_user):
    response = client.put("/users/password", json = {'password':'testpassword',
                                                     'new_password':'newpassword'})
    assert response.status_code == status.HTTP_200_OK

def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/password", json = {
        'password': 'wrongpassword',
        'new_password':'newpassword'
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on password change'}

def test_change_phonenumber_success(test_user):
    response = client.put("/users/phone_number/464545455")
    assert response.status_code == status.HTTP_200_OK
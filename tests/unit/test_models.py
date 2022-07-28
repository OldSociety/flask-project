from yourspace.models import User

def test_create_user():
    user = User('username', 'email', 'password', 'posts')
    assert user.username == 'patkennedy'
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password != 'FlaskIsAwesome'
    assert user.posts == 'user'

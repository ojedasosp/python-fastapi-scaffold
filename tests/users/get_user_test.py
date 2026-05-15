from users import User

async def test_a_user_is_on_db(a_user_already_on_db, client):
    response = await client.get(f"/api/users/{1}")
    user = response.json()
    assert "name" in user
    assert "age" in user
    assert "email" in user

async def test_a_user_is_not_found(a_user_already_on_db, client):
    response = await client.get(f"/api/users/{2}")
    assert response.status_code == 404



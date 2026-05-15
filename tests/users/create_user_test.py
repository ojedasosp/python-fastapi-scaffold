from dtos.user_dto import CreateUserDTO

async def test_user_already_on_db(a_user_already_on_db, client):
    user = CreateUserDTO(name="Alice", age=30, email="alice@example.com", password="secret123").model_dump()
    response = await client.post("/api/users/", json=user)
    print(response.json())
    assert response.status_code == 409

async def test_create_a_user(client):
    user = CreateUserDTO(name="Alice", age=30, email="alice@example.com", password="secret123").model_dump()
    response = await client.post("/api/users/", json=user)
    created_user = response.json()
    print(created_user)
    assert response.status_code == 201
    assert "name" in created_user
    assert "age" in created_user
    assert "email" in created_user



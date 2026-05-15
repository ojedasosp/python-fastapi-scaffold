async def test_user_deleted(a_user_already_on_db, client):
    response = await client.delete("/api/users/", params = { 'id': 1 })
    assert response.status_code == 204 




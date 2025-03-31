from fastapi import FastAPI
from fastapi.testclient import TestClient
from litepolis_router_example import *

app = FastAPI()

app.include_router(
    router,
    prefix=f"/api/{prefix}"
)

client = TestClient(app)

def test_read_main():
    response = client.get(f"/api/{prefix}")
    assert response.status_code == 200
    assert response.json()["detail"] == "OK"

def test_read_user():
    response = client.get(f"/api/{prefix}/user")
    assert response.status_code == 200
    json_dict = response.json()
    assert json_dict["message"] == "User information"
    assert json_dict["detail"] == {
        "id": 0,
        "email": "user@example.com",
        "role": "user"
    }
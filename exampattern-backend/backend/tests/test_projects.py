import uuid

API = "/api/v1/projects"
PAYLOAD = {
    "title": "DSA End Sem",
    "course": "B.Tech CSE",
    "semester": "3",
    "duration_minutes": 180,
    "max_marks": 70,
    "institution": {"name": "Example Institute of Technology", "university_name": "Example University"},
    "subject_name": "Data Structures",
    "subject_code": "KCS301",
}


def test_requires_auth(client):
    assert client.get(API).status_code == 401
    assert client.post(API, json=PAYLOAD).status_code == 401


def test_create_get_list(client, auth_headers):
    r = client.post(API, json=PAYLOAD, headers=auth_headers)
    assert r.status_code == 201
    p = r.json()
    assert p["institution"]["name"] == "Example Institute of Technology"
    assert p["subject"]["name"] == "Data Structures" and p["subject"]["code"] == "KCS301"

    assert client.get(f"{API}/{p['id']}", headers=auth_headers).json()["id"] == p["id"]
    page = client.get(API, headers=auth_headers).json()
    assert page["total"] == 1 and page["items"][0]["id"] == p["id"]


def test_institution_and_subject_are_reused(client, auth_headers):
    a = client.post(API, json=PAYLOAD, headers=auth_headers).json()
    b = client.post(API, json={**PAYLOAD, "title": "Second"}, headers=auth_headers).json()
    assert a["institution"]["id"] == b["institution"]["id"] and a["subject"]["id"] == b["subject"]["id"]


def test_pagination(client, auth_headers):
    for i in range(3):
        client.post(API, json={"title": f"P{i}"}, headers=auth_headers)
    page = client.get(f"{API}?limit=2&offset=0", headers=auth_headers).json()
    assert page["total"] == 3 and len(page["items"]) == 2
    assert client.get(f"{API}?limit=0", headers=auth_headers).status_code == 422


def test_validation(client, auth_headers):
    assert client.post(API, json={}, headers=auth_headers).status_code == 422
    assert client.post(API, json={"title": "x", "max_marks": -5}, headers=auth_headers).status_code == 422


def test_patch_only_changes_sent_fields(client, auth_headers):
    p = client.post(API, json=PAYLOAD, headers=auth_headers).json()
    r = client.patch(f"{API}/{p['id']}", json={"max_marks": 100}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["max_marks"] == 100 and r.json()["title"] == PAYLOAD["title"]


def test_delete(client, auth_headers):
    p = client.post(API, json=PAYLOAD, headers=auth_headers).json()
    assert client.delete(f"{API}/{p['id']}", headers=auth_headers).status_code == 204
    assert client.get(f"{API}/{p['id']}", headers=auth_headers).status_code == 404


def test_other_users_projects_are_invisible(client, make_user):
    alice = make_user("alice@example.com")
    bob = make_user("bob@example.com")
    p = client.post(API, json=PAYLOAD, headers=alice).json()

    assert client.get(f"{API}/{p['id']}", headers=bob).status_code == 404
    assert client.patch(f"{API}/{p['id']}", json={"title": "hacked"}, headers=bob).status_code == 404
    assert client.delete(f"{API}/{p['id']}", headers=bob).status_code == 404
    assert client.get(API, headers=bob).json()["total"] == 0
    # untouched for the real owner
    assert client.get(f"{API}/{p['id']}", headers=alice).json()["title"] == PAYLOAD["title"]


def test_unknown_project_404_and_bad_uuid_422(client, auth_headers):
    assert client.get(f"{API}/{uuid.uuid4()}", headers=auth_headers).status_code == 404
    assert client.get(f"{API}/not-a-uuid", headers=auth_headers).status_code == 422

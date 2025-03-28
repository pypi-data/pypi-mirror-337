from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_profiles_table_populated_on_visit():
    datasette = Datasette(memory=True)
    await datasette.invoke_startup()

    actors1 = await datasette.actors_from_ids(("user1", "user2", "user3"))
    assert actors1 == {
        "user1": {"id": "user1"},
        "user2": {"id": "user2"},
        "user3": {"id": "user3"},
    }

    internal_db = datasette.get_internal_database()
    # Create empty users:
    for actor_id in ("user1", "user2", "user3"):
        await datasette.client.get(
            "/", cookies={"ds_actor": datasette.client.actor_cookie({"id": actor_id})}
        )
    assert (
        await internal_db.execute("select count(*) from profiles")
    ).single_value() == 3
    await internal_db.execute_write(
        "update profiles set name = 'User 1' where id = 'user1'"
    )
    await internal_db.execute_write(
        "update profiles set name = 'User 2' where id = 'user2'"
    )
    actors2 = await datasette.actors_from_ids(("user1", "user2", "user3"))
    assert actors2 == {
        "user1": {
            "id": "user1",
            "name": "User 1",
            "title": None,
            "email": None,
            "bio": None,
        },
        "user2": {
            "id": "user2",
            "name": "User 2",
            "title": None,
            "email": None,
            "bio": None,
        },
        "user3": {
            "id": "user3",
            "name": None,
            "title": None,
            "email": None,
            "bio": None,
        },
    }

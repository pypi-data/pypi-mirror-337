from datasette import hookimpl



@hookimpl
def actors_from_ids(datasette, actor_ids):
    db = datasette.get_internal_database()

    async def inner():
        sql = "select * from profiles where id in ({})".format(
            ", ".join("?" for _ in actor_ids)
        )
        actors = {}
        for row in (await db.execute(sql, actor_ids)).rows:
            actor = dict(row)
            actors[actor["id"]] = actor
        
        # Fill in any that are missing
        for actor_id in actor_ids:
            if actor_id not in actors:
                actors[actor_id] = {"id": actor_id}
        return actors

    return inner

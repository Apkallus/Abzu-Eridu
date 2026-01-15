







### Composite Conditions

So far, our `WHERE` conditions have been pretty simple.
This challenge complicates it somewhat by injection decoy data into your database.
Luckily, the flag tag is back.

You'll need to filter on _both_ the flag tag and the flag value.
Analogous to other programming languages, you can join together conditional expressions with boolean operators such as `AND` and `OR`.
Craft a powerful expression and filter the flag from the decoys!


### Reaching Your LIMITs

You've been able to rely on your `WHERE` clause to filter things down to exactly one result, but in this challenge, we've taken away the flag tags that you relied on to filter out decoy flags!
Luckily, simple SQL queries tend to return data in the order that it was inserted into the database, and the real flag was inserted before the decoy flags (but after some of the garbage data).
All you need is to `LIMIT` your query to just `1` result, and that result should be your flag!
The challenge links you to the `LIMIT` documentation if you need it!


### Querying Metadata

In actual security scenarios, there are times where the attacker lacks certain information, such as the names of tables that they want to query!
Luckily, every SQL engine has some way to query _metadata_ about tables (though, confusingly, every engine does this differently!).
SQLite uses a special `sqlite_master` table, in which it stores information about all other tables.
Can you figure out the name of the table that contains the flag, and query it?

var MIGRATION_ID = "0003_id_index";

var migration = db.migrations.findOne({
  migration: MIGRATION_ID
});

if (migration) {
  print("Migration " + MIGRATION_ID + " has already been applied.");
  quit(1);
}

db.tweets.createIndex(
  {
    id: 1
  },
  {
    name: "TweetId"
  }
);

db.migrations.insert({
  migration: MIGRATION_ID,
  created: new Date()
});

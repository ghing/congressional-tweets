var MIGRATION_ID = "0003_id_index";

var migration = db.migrations.findOne({
  migration: MIGRATION_ID
});

if (!migration) {
  print("Migration " + MIGRATION_ID + " has not been applied.");
  quit(1);
}

db.tweets.dropIndex("TweetId");

db.migrations.remove({
  migration: MIGRATION_ID
});

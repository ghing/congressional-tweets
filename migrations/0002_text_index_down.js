var MIGRATION_ID = "0002_text_index";

var migration = db.migrations.findOne({
  migration: MIGRATION_ID
});

if (!migration) {
  print("Migration " + MIGRATION_ID + " has not been applied.");
  quit(1);
}

db.tweets.dropIndex("TweetText");

db.migrations.remove({
  migration: MIGRATION_ID
});

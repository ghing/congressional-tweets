var MIGRATION_ID = "0002_text_index";

var migration = db.migrations.findOne({
  migration: MIGRATION_ID
});

if (migration) {
  print("Migration " + MIGRATION_ID + " has already been applied.");
  quit(1);
}

db.tweets.createIndex(
  {
    text: "text"
  },
  {
    name: "TweetText"
  }  
);

db.migrations.insertOne({
  migration: MIGRATION_ID,
  created: new Date()
});

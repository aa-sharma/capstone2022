const mongoose = require("mongoose");

const ExerciseLevelSchema = mongoose.Schema({
  exercise: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Exercise",
    required: [true, "`exercise` is required"],
  },
  level: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Level",
    required: [true, "`level` is required"],
  },
  dexterityDifficulty: {
    // value 1-10
    type: Number,
    required: true,
    min: [1, "minimum dexterity difficulty is 1"],
    max: [10, "maximum dexterity difficulty is 10"],
  },
  agilityDifficulty: {
    // value 1-10
    type: Number,
    required: true,
    min: [1, "minimum agility difficulty is 1"],
    max: [10, "maximum agility difficulty is 10"],
  },
});

const ExerciseLevel = mongoose.model("ExerciseLevel", ExerciseLevelSchema);

module.exports = { ExerciseLevel, ExerciseLevelSchema };

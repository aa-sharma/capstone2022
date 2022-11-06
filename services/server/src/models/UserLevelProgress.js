const mongoose = require("mongoose");
const { ExerciseLevelSchema } = require("./ExerciseLevel");

const UserLevelProgressSchema = mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: [true, "`user` is required"],
  },
  exerciseLevel: {
    type: ExerciseLevelSchema,
    default: () => ({}),
  },
  dexterityScore: {
    // relative to exerciseLevel dexterityDifficulty
    type: Number,
    required: [true, "`dexterityScore` is required"],
  },
  agilityScore: {
    // relative to exerciseLevel agilityDifficulty
    type: Number,
    required: [true, "`agilityScore` is required"],
  },
});

const UserLevelProgress = mongoose.model(
  "UserLevelProgress",
  UserLevelProgressSchema
);

module.exports = { UserLevelProgress, UserLevelProgressSchema };

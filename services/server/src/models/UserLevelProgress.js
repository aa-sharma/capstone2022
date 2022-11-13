const mongoose = require("mongoose");
const { ExerciseSchema } = require("./Exercise");

const modifiedExerciseSchema = mongoose.Schema(ExerciseSchema, {
  toJSON: {
    transform: function (doc, ret) {
      delete ret._id;
    },
  },
});

const UserLevelProgressSchema = mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: [true, "`user` is required"],
  },
  exercise: {
    type: modifiedExerciseSchema,
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
  date: {
    type: Date,
    default: Date.now,
  },
});

UserLevelProgressSchema.path("exercise").validate(function (exercise) {
  if (!exercise.position) {
    return false;
  } else if (exercise.position.length != 2) {
    return false;
  }
  return true;
}, "`exercise.position` must be of length 2, where the first index is the starting position and second index is the ending position");

const UserLevelProgress = mongoose.model(
  "UserLevelProgress",
  UserLevelProgressSchema
);

module.exports = { UserLevelProgress, UserLevelProgressSchema };

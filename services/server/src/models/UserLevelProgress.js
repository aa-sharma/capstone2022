const mongoose = require("mongoose");
const { ExerciseSchema } = require("./Exercise");
const logger = require("../utils/logger");

const modifiedExerciseSchema = mongoose.Schema(ExerciseSchema, {
  toJSON: {
    transform: function (doc, ret) {
      delete ret._id;
    },
  },
});

const SchemaTypes = mongoose.Schema.Types;
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
    type: SchemaTypes.Decimal128,
    required: [true, "`dexterityScore` is required"],
  },
  agilityScore: {
    // relative to exerciseLevel agilityDifficulty
    type: SchemaTypes.Decimal128,
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

UserLevelProgressSchema.path("agilityScore").validate(function (agilityScore) {
  if (
    parseFloat(agilityScore) > parseFloat(String(10)) ||
    parseFloat(agilityScore) < parseFloat(String(0))
  ) {
    return false;
  }
  return true;
}, "`agilityScore` must be between 0 and 10");

UserLevelProgressSchema.path("dexterityScore").validate(function (
  dexterityScore
) {
  if (
    parseFloat(dexterityScore) > parseFloat(String(10)) ||
    parseFloat(dexterityScore) < parseFloat(String(0))
  ) {
    return false;
  }
  return true;
},
"`dexterityScore` must be between 0 and 10");

const UserLevelProgress = mongoose.model(
  "UserLevelProgress",
  UserLevelProgressSchema
);

module.exports = { UserLevelProgress, UserLevelProgressSchema };

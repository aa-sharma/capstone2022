const mongoose = require("mongoose");
const { PositionSchema } = require("./Position");

const ExerciseSchema = mongoose.Schema({
  position: [
    {
      type: PositionSchema,
      default: () => ({}),
    },
  ],
  level: {
    type: Number,
    required: [true, "`level` is required"],
  },
  dexterityDifficulty: {
    // value 1-10
    type: Number,
    required: [true, "`dexterityDifficulty` is required"],
    min: [1, "minimum dexterity difficulty is 1"],
    max: [10, "maximum dexterity difficulty is 10"],
  },
  agilityDifficulty: {
    // value 1-10
    type: Number,
    required: [true, "`agilityDifficulty` is required"],
    min: [1, "minimum agility difficulty is 1"],
    max: [10, "maximum agility difficulty is 10"],
  },
});

ExerciseSchema.path("position").validate(function (position) {
  if (!position) {
    return false;
  } else if (position.length != 2) {
    return false;
  }
  return true;
}, "`position` must be of length 2, where the first index is the starting position and second index is the ending position");

const Exercise = mongoose.model("Exercise", ExerciseSchema);

module.exports = { Exercise, ExerciseSchema };

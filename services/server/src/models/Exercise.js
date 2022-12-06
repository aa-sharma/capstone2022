const mongoose = require("mongoose");
const { PositionSchema } = require("./Position");

const ExerciseSchema = mongoose.Schema({
  position: [
    {
      type: PositionSchema,
      default: () => ({}),
    },
  ],
  description: {
    type: String,
    required: [true, "`description` is required"],
  },
  level: {
    type: Number,
    required: [true, "`level` is required"],
  },
  exerciseNumber: {
    type: Number,
    required: [true, "`exerciseNumber` is required"],
  },
  image: {
    type: String,
    required: [true, "`image` is required"],
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

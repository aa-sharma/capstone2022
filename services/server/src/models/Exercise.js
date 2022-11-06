const mongoose = require("mongoose");
const logger = require("../utils/logger");

const { ExerciseLevel } = require("./ExerciseLevel");

const ExerciseSchema = mongoose.Schema({
  flexResistor1: {
    type: Number,
    required: [true, "`flexResistor1` is required"],
  },
  flexResistor2: {
    type: Number,
    required: [true, "`flexResistor2` is required"],
  },
  flexResistor3: {
    type: Number,
    required: [true, "`flexResistor3` is required"],
  },
  flexResistor4: {
    type: Number,
    required: [true, "`flexResistor4` is required"],
  },
  flexResistor5: {
    type: Number,
    required: [true, "`flexResistor5` is required"],
  },
  gyroscope: {
    type: Number,
    required: [true, "`gyroscope` is required"],
  },
});

async function preDelete() {
  const doc = await Exercise.findOne(this.getFilter());
  if (doc) {
    await ExerciseLevel.deleteMany({ exercise: doc._id });
  }
}

ExerciseSchema.pre("deleteOne", preDelete);
ExerciseSchema.pre("deleteMany", preDelete);

const Exercise = mongoose.model("Exercise", ExerciseSchema);

module.exports = { Exercise, ExerciseSchema };

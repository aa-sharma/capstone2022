const mongoose = require("mongoose");
const logger = require("../utils/logger");
const { ExerciseLevel } = require("./ExerciseLevel");

const LevelSchema = mongoose.Schema({
  levelNumber: {
    type: Number,
    unique: true,
    required: [true, "`levelNumber` is required"],
  },
});

LevelSchema.path("levelNumber").validate(async (value) => {
  const levelNumberCount = await mongoose.models.Level.countDocuments({
    levelNumber: value,
  });
  return !levelNumberCount;
}, "Level Already Exists");

async function preDelete() {
  const doc = await Level.findOne(this.getFilter());
  if (doc) {
    await ExerciseLevel.deleteMany({ level: doc._id });
  }
}

LevelSchema.pre("deleteOne", preDelete);
LevelSchema.pre("deleteMany", preDelete);

const Level = mongoose.model("Level", LevelSchema);

module.exports = { Level, LevelSchema };

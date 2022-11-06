const mongoose = require("mongoose");
const config = require("config");
const { Level } = require("../models/Level");
const logger = require("../utils/logger");
const { Exercise } = require("../models/Exercise");
const { ExerciseLevel } = require("../models/ExerciseLevel");
const readJson = require("../utils/readJson");

const connectDB = async () => {
  try {
    await mongoose.connect(
      `mongodb://${process.env.MONGO_INITDB_ROOT_USERNAME}:${process.env.MONGO_INITDB_ROOT_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.MONGO_INITDB_DATABASE}`,
      {
        useNewUrlParser: true,
      }
    );

    logger.info("MongoDB Connected...");
  } catch (err) {
    logger.error(err.message);
    process.exit(1);
  }
};

const initLevels = async () => {
  const levels = await readJson(
    "./src/config/initilize-data/initilize-levels.json"
  );
  try {
    await Level.deleteMany();

    for (idx in levels) {
      let level = new Level({
        levelNumber: levels[idx].levelNumber,
      });
      await level.save();
    }
  } catch (err) {
    logger.error(err);
  }
};

const initExercises = async () => {
  const exercises = await readJson(
    "./src/config/initilize-data/initilize-exercises.json"
  );
  try {
    await Exercise.deleteMany();

    for (idx in exercises) {
      const exercise = new Exercise({
        flexResistor1: exercises[idx].flexResistor1,
        flexResistor2: exercises[idx].flexResistor2,
        flexResistor3: exercises[idx].flexResistor3,
        flexResistor4: exercises[idx].flexResistor4,
        flexResistor5: exercises[idx].flexResistor5,
        gyroscope: exercises[idx].gyroscope,
      });

      await exercise.save();
    }
  } catch (err) {
    logger.error(err);
  }
};

const initExerciseLevels = async () => {
  const exerciseLevels = await readJson(
    "./src/config/initilize-data/initilize-exerciseLevels.json"
  );
  const exercises = await readJson(
    "./src/config/initilize-data/initilize-exercises.json"
  );

  try {
    await ExerciseLevel.deleteMany();

    for (idx in exerciseLevels) {
      let level = await Level.findOne({
        levelNumber: exerciseLevels[idx].levelNumber,
      });

      let exercise = await Exercise.findOne({
        flexResistor1:
          exercises[exerciseLevels[idx].exerciseIndex].flexResistor1,
        flexResistor2:
          exercises[exerciseLevels[idx].exerciseIndex].flexResistor2,
        flexResistor3:
          exercises[exerciseLevels[idx].exerciseIndex].flexResistor3,
        flexResistor4:
          exercises[exerciseLevels[idx].exerciseIndex].flexResistor4,
        flexResistor5:
          exercises[exerciseLevels[idx].exerciseIndex].flexResistor5,
        gyroscope: exercises[exerciseLevels[idx].exerciseIndex].gyroscope,
      });

      let exerciseLevel = new ExerciseLevel({
        level: level._id,
        exercise: exercise._id,
        dexterityDifficulty: exerciseLevels[idx].dexterityDifficulty,
        agilityDifficulty: exerciseLevels[idx].agilityDifficulty,
      });
      await exerciseLevel.save();
    }
  } catch (err) {
    logger.error(err);
  }
};

const initData = async () => {
  await initLevels();
  await initExercises();
  await initExerciseLevels();
};

module.exports = { connectDB, initData };

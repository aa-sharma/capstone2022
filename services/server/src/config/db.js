const mongoose = require("mongoose");
const config = require("config");
const logger = require("../utils/logger");
const { Exercise } = require("../models/Exercise");
const { readJson } = require("../utils/helpers");

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

const initExercises = async () => {
  const exercises = await readJson(
    "./src/config/initilize-data/initilize-exercises.json"
  );
  const positions = await readJson(
    "./src/config/initilize-data/initilize-positions.json"
  );

  const startingPosition = {
    flexResistor1: 0,
    flexResistor2: 0,
    flexResistor3: 0,
    flexResistor4: 0,
    flexResistor5: 0,
    gyroscope: 0,
  };

  try {
    await Exercise.deleteMany();

    for (idx in exercises) {
      const finalPosition = {
        flexResistor1: positions[exercises[idx].positionIndex].flexResistor1,
        flexResistor2: positions[exercises[idx].positionIndex].flexResistor2,
        flexResistor3: positions[exercises[idx].positionIndex].flexResistor3,
        flexResistor4: positions[exercises[idx].positionIndex].flexResistor4,
        flexResistor5: positions[exercises[idx].positionIndex].flexResistor5,
        gyroscope: positions[exercises[idx].positionIndex].gyroscope,
      };

      let exercise = new Exercise({
        level: exercises[idx].level,
        position: [startingPosition, finalPosition],
        dexterityDifficulty: exercises[idx].dexterityDifficulty,
        agilityDifficulty: exercises[idx].agilityDifficulty,
      });
      await exercise.save();
    }
  } catch (err) {
    logger.error(err);
  }
};

module.exports = { connectDB, initExercises };

const express = require("../config/express-p");
const router = express.Router();
const { Exercise } = require("../models/Exercise");
const { readJson } = require("../utils/helpers");
const authAdmin = require("../middleware/authAdmin");
const logger = require("../utils/logger");

// @route   POST api/initilize/
// @desc    remove all exercises and replaces with the ones specified in initilize-server-data directory
// @access  onlyAdmin
router.postP("/", authAdmin, async (req, res) => {
  try {
    const exercises = await readJson(
      "./initilize-server-data/initilize-exercises.json"
    );
    const positions = await readJson(
      "./initilize-server-data/initilize-positions.json"
    );

    await Exercise.deleteMany();

    for (const exerciseData of exercises) {
      let exercise = new Exercise({
        level: exerciseData.level,
        exerciseNumber: exerciseData.exerciseNumber,
        description: exerciseData.description,
        position: [
          positions[exerciseData.position[0]],
          positions[exerciseData.position[1]],
        ],
        image: `${exerciseData.position[1]}.png`,
      });
      await exercise.save();
    }

    return res.json({ msg: "successfully initilized data" });
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/initilize/
// @desc    remove all exercises
// @access  onlyAdmin
router.deleteP("/", authAdmin, async (req, res) => {
  try {
    exercise = await Exercise.deleteMany();

    return res.json(exercise);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

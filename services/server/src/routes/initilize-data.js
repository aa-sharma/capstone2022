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

    const startingPosition = {
      pinkyAngle: 0,
      ringAngle: 0,
      middleAngle: 0,
      indexAngle: 0,
      thumbAngle: 0,
      roll: 0,
      pitch: 0,
      yaw: 0,
    };

    await Exercise.deleteMany();

    for (idx in exercises) {
      const finalPosition = {
        pinkyAngle: positions[exercises[idx].positionIndex].pinkyAngle,
        ringAngle: positions[exercises[idx].positionIndex].ringAngle,
        middleAngle: positions[exercises[idx].positionIndex].middleAngle,
        indexAngle: positions[exercises[idx].positionIndex].indexAngle,
        thumbAngle: positions[exercises[idx].positionIndex].thumbAngle,
        roll: positions[exercises[idx].positionIndex].roll,
        pitch: positions[exercises[idx].positionIndex].pitch,
        yaw: positions[exercises[idx].positionIndex].yaw,
      };

      let exercise = new Exercise({
        level: exercises[idx].level,
        exerciseNumber: exercises[idx].exerciseNumber,
        description: exercises[idx].description,
        position: [startingPosition, finalPosition],
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

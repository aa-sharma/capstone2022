const express = require("../config/express-p");
const router = express.Router();
const { check, validationResult } = require("express-validator");
const logger = require("../utils/logger");
const auth = require("../middleware/auth");
const { ExerciseLevel } = require("../models/ExerciseLevel");

// @route   GET api/exerciseLevels/
// @desc    get all exerciseLevels
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    let exerciseLevels = await ExerciseLevel.find()
      .select("-__v")
      .populate("exercise", "-__v -_id")
      .populate("level", "-__v -_id");
    return res.json(exerciseLevels);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

const express = require("../config/express-p");
const router = express.Router();
const { check, validationResult } = require("express-validator");
const logger = require("../utils/logger");
const { Exercise } = require("../models/Exercise");
const auth = require("../middleware/auth");
const authAdmin = require("../middleware/authAdmin");
const mongoose = require("mongoose");
const { singleErrorMsg } = require("../utils/handleErrors");

// @route   GET api/exercise/
// @desc    get all exercises
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    let exercises = await Exercise.find().select("-__v");
    return res.json(exercises);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/exercise/:id
// @desc    delete exercise by id
// @access  onlyAdmin
router.deleteP("/:id", authAdmin, async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res
        .status(400)
        .json(singleErrorMsg("invalid value for exercise id"));
    }

    let exercise = await Exercise.deleteOne({ _id: req.params.id });
    if (!exercise.deletedCount) {
      return res.status(400).json(singleErrorMsg("exercise does not exist"));
    }
    return res.json(exercise);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

const express = require("../config/express-p");
const router = express.Router();
const { check, validationResult } = require("express-validator");
const logger = require("../utils/logger");
const auth = require("../middleware/auth");
const { Exercise } = require("../models/Exercise");
const {
  singleErrorMsg,
  handleMongooseErrors,
} = require("../utils/handleErrors");
const authAdmin = require("../middleware/authAdmin");
const { paginationResponse, isValidObjectId } = require("../utils/helpers");

// @route   POST api/exercise
// @desc    create new exercise
// @access  onlyAdmin
router.postP("/", auth, async (req, res) => {
  const { position, level, description } = req.body;

  try {
    let exercise = new Exercise({
      position,
      level,
      description,
    });

    try {
      await exercise.save();
    } catch (err) {
      return res.status(400).json(handleMongooseErrors(err));
    }

    exercise = await Exercise.findOne({ _id: exercise._id }).select("-__v");

    return res.json(exercise);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/exercise/:id
// @desc    get a particular exercise by id
// @access  Private
router.getP("/:id", auth, async (req, res) => {
  try {
    if (!isValidObjectId(req.params.id)) {
      return res.status(400).json(singleErrorMsg("not a valid mongodb id"));
    }

    let exercise = await Exercise.findOne({
      _id: req.params.id,
    }).select("-__v");

    if (!exercise) {
      return res.status(400).json(singleErrorMsg("exercise does not exist"));
    }

    return res.json(exercise);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/exercise/
// @desc    get all exercises
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    let exercise = await Exercise.find().select("-__v").sort({ level: "asc" });

    return res.json(
      paginationResponse(exercise, req.query.page, req.query.pageSize)
    );
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/exercise/level/:levelNumber
// @desc    Gets level progress for a user by for a given level
// @access  Private
router.getP("/level/:levelNumber", auth, async (req, res) => {
  try {
    if (!Number(req.params.levelNumber)) {
      return res
        .status(400)
        .json(singleErrorMsg("level is not a valid number"));
    }

    let exercise = await Exercise.find({
      user: req.user._id,
      level: req.params.levelNumber,
    }).select("-__v");

    return res.json(
      paginationResponse(exercise, req.query.page, req.query.pageSize)
    );
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
    if (!isValidObjectId(req.params.id)) {
      return res.status(400).json(singleErrorMsg("not a valid mongodb id"));
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

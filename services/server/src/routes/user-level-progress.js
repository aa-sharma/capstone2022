const express = require("../config/express-p");
const router = express.Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const config = require("config");
const auth = require("../middleware/auth");
const { check, validationResult } = require("express-validator");
const { _ } = require("lodash");
const logger = require("../utils/logger");
const { UserLevelProgress } = require("../models/UserLevelProgress");
const {
  isValidObjectId,
  paginationResponse,
  structuredClone,
} = require("../utils/helpers");
const {
  handleMongooseErrors,
  singleErrorMsg,
} = require("../utils/handleErrors");

// @route   POST api/user-level-progress/
// @desc    Updates level progress for a user
// @access  Private
router.postP("/", auth, async (req, res) => {
  const { exercise, dexterityScore, agilityScore } = req.body;

  try {
    let userLevelProgress = new UserLevelProgress({
      user: req.user._id,
      exercise,
      dexterityScore: Math.round(dexterityScore * 100) / 100,
      agilityScore: Math.round(agilityScore * 100) / 100,
      overallScore:
        Math.round(((3 / 4) * dexterityScore + (1 / 4) * agilityScore) * 100) /
        100,
    });

    try {
      await userLevelProgress.save();
    } catch (err) {
      return res.status(400).json(handleMongooseErrors(err));
    }

    userLevelProgress = await UserLevelProgress.findOne({
      _id: userLevelProgress._id,
    }).select("-__v -user");

    return res.json(userLevelProgress);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/user-level-progress/
// @desc    Gets all user level progress reports for a user
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    let userLevelProgresses = await UserLevelProgress.find({
      user: req.user._id,
    })
      .select("-__v -user")
      .sort({ date: "desc" });

    return res.json(
      paginationResponse(
        userLevelProgresses,
        req.query.page,
        req.query.pageSize
      )
    );
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/user-level-progress/:id
// @desc    Gets level progress for a user by userLevelProgress ID
// @access  Private
router.getP("/:id", auth, async (req, res) => {
  try {
    if (!isValidObjectId(req.params.id)) {
      return res.status(400).json(singleErrorMsg("not a valid mongodb id"));
    }

    let userLevelProgress = await UserLevelProgress.findOne({
      _id: req.params.id,
      user: req.user._id,
    }).select("-__v -user");
    if (!userLevelProgress) {
      return res
        .status(400)
        .json(singleErrorMsg("userLevelProgress report does not exist"));
    }

    return res.json(userLevelProgress);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/user-level-progress/level/:levelNumber
// @desc    Gets level progress for a user by for a given level
// @access  Private
router.getP("/level/:levelNumber", auth, async (req, res) => {
  try {
    if (!Number(req.params.levelNumber)) {
      return res
        .status(400)
        .json(singleErrorMsg("level is not a valid number"));
    }

    let userLevelProgresses = await UserLevelProgress.find({
      user: req.user._id,
      "exercise.level": req.params.levelNumber,
    }).select("-__v -user");

    return res.json(
      paginationResponse(
        userLevelProgresses,
        req.query.page,
        req.query.pageSize
      )
    );
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/user-level-progress/:id
// @desc    delete userLevelProgress report by id
// @access  Private
router.deleteP("/:id", auth, async (req, res) => {
  try {
    if (!isValidObjectId(req.params.id)) {
      return res.status(400).json(singleErrorMsg("not a valid mongodb id"));
    }

    let userLevelProgress = await UserLevelProgress.deleteOne({
      _id: req.params.id,
      user: req.user._id,
    });

    if (!userLevelProgress.deletedCount) {
      return res
        .status(400)
        .json(singleErrorMsg("userLevelProgress report does not exist"));
    }

    return res.json(userLevelProgress);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/user-level-progress/:id
// @desc    delete all userLevelProgress reports
// @access  Private
router.deleteP("/", auth, async (req, res) => {
  try {
    let userLevelProgress = await UserLevelProgress.deleteMany({
      user: req.user._id,
    });

    if (!userLevelProgress.deletedCount) {
      return res
        .status(400)
        .json(singleErrorMsg("userLevelProgress reports did not exist"));
    }

    return res.json(userLevelProgress);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});
module.exports = router;

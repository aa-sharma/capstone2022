const express = require("../config/express-p");
const router = express.Router();
const { check, validationResult } = require("express-validator");
const logger = require("../utils/logger");
const { singleErrorMsg } = require("../utils/handleErrors");
const { Level } = require("../models/Level");
const auth = require("../middleware/auth");
const authAdmin = require("../middleware/authAdmin");
const mongoose = require("mongoose");

// @route   GET api/level/
// @desc    get all levels
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    let levels = await Level.find().select("-__v");
    return res.json(levels);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/level/:levelNumber
// @desc    delete level by levelNumber
// @access  onlyAdmin
router.deleteP("/:levelNumber", authAdmin, async (req, res) => {
  try {
    if (!Number(req.params.levelNumber)) {
      return res
        .status(400)
        .json(singleErrorMsg("invalid value for levelNumber"));
    }
    let level = await Level.deleteOne({ levelNumber: req.params.levelNumber });
    if (!level.deletedCount) {
      return res.status(400).json(singleErrorMsg("level does not exist"));
    }
    return res.json(level);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

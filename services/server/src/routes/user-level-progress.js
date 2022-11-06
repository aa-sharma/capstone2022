const express = require("../config/express-p");
const router = express.Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const config = require("config");
const auth = require("../middleware/auth");
const { check, validationResult } = require("express-validator");

// @route   POST api/user-level-progress/
// @desc    Updates level progress for a user
// @access  Private

// @route   GET api/user-level-progress/
// @desc    Gets level progress for a user
// @access  Private

module.exports = router;

const express = require("express");
const router = express.Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const config = require("config");
const { check, validationResult } = require("express-validator/check");

// @route   POST api/user-hand-position-initialization
// @desc    Updates HandMap model to initialize a hand mapping for a given user
// @access  Private

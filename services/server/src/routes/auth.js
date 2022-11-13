const express = require("../config/express-p");
const router = express.Router();
const bcrypt = require("bcryptjs");
const auth = require("../middleware/auth");
const logger = require("../utils/logger");
const { check, validationResult } = require("express-validator");
const { User } = require("../models/User");
const { singleErrorMsg, handleExpressValidatorError } = require("../utils/handleErrors");
const { signJWT } = require("../utils/helpers");

// @route   POST api/auth
// @desc    Auth user & get token
// @access  Public
router.postP(
  "/",
  [
    check("email", "Please include a valid email").isEmail(),
    check("password", "Password is required").exists(),
  ],
  async (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json(handleExpressValidatorError(errors));
    }

    const { email, password } = req.body;
    try {
      const user = await User.findOne({ email });
      if (!user) {
        return res.status(400).json(singleErrorMsg("Invalid Credentials"));
      }
      const isMatch = await bcrypt.compare(password, user.password);

      if (!isMatch) {
        return res.status(400).json(singleErrorMsg("Invalid Credentials"));
      }

      const token = await signJWT(user);
      return res.json({ token });
    } catch (err) {
      logger.error(err.message);
      res.status(500).send("Server Error");
    }
  }
);

// @route   POST api/auth/device
// @desc    Auth user & get token
// @access  Public
router.postP(
  "/device",
  [
    check("productCode", "Please include a valid product code").isLength({
      min: 6,
      max: 20,
    }),
  ],
  async (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json(handleExpressValidatorError(errors));
    }

    const { productCode } = req.body;
    try {
      const user = await User.findOne({ productCode });
      if (!user) {
        return res
          .status(400)
          .json(singleErrorMsg("user product code does not exist"));
      }

      const token = await signJWT(user);
      return res.json({ token });
    } catch (err) {
      logger.error(err.message);
      res.status(500).send("Server Error");
    }
  }
);

// @route   GET api/auth
// @desc    Get logged in user
// @access  Private
router.getP("/", auth, async (req, res) => {
  try {
    return res.json(req.user);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

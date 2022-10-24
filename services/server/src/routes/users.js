const express = require("express");
const router = express.Router();
const bcrypt = require("bcryptjs");
const config = require("config");
const { check, validationResult } = require("express-validator");
const User = require("../models/User");
const logger = require("../utils/logger");
const auth = require("../middleware/auth");
const signJWT = require("../utils/sign-jwt");

// @route   POST api/users
// @desc    Register a user
// @access  Public
router.post(
  "/",
  [
    check("name", "Name is required").not().isEmpty(),
    check("email", "Please include a valid email").isEmail(),
    check(
      "password",
      "Please enter a password with 6 or more character"
    ).isLength({ min: 6 }),
  ],
  async (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { name, email, password } = req.body;

    try {
      let user = await User.findOne({ email });

      if (user) {
        return res.status(400).json({ msg: "User already exists" });
      }

      user = new User({
        name,
        email,
        password,
      });

      const salt = await bcrypt.genSalt(10);
      user.password = await bcrypt.hash(password, salt);

      await user.save();

      const token = await signJWT(user);
      return res.json({ token });
    } catch (err) {
      logger.error(err.message);
      res.status(500).send("Server Error");
    }
  }
);

// @route   POST api/users/register-product-code
// @desc    Register Product Code
// @access  Private
router.post(
  "/register-product-code",
  auth,
  [
    check("productCode", "Please include a valid product code")
      .exists()
      .isLength({ min: 6, max: 20 }),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);

      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { productCode } = req.body;
      const user = await User.findById(req.user.id)
        .select("-password")
        .select("-__v");

      user.productCode = productCode;
      await user.save();

      return res.json(user);
    } catch (err) {
      logger.error(err.message);
      return res.status(500).send("Server Error");
    }
  }
);

module.exports = router;

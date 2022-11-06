const express = require("../config/express-p");
const router = express.Router();
const bcrypt = require("bcryptjs");
const config = require("config");
const { check, validationResult } = require("express-validator");
const { User } = require("../models/User");
const logger = require("../utils/logger");
const auth = require("../middleware/auth");
const signJWT = require("../utils/sign-jwt");
const authAdmin = require("../middleware/authAdmin");

// @route   POST api/users
// @desc    Register a user
// @access  Public
router.postP(
  "/",
  [
    check("name", "Please include a name").exists(),
    check("email", "Please include a valid email").isEmail(),
    check("password", "Password must be greater than or equal to 6 characters")
      .exists()
      .isLength({ min: 6 }),
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
        return res.status(400).json({
          errors: [{ msg: "Email already exists" }],
        });
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
router.postP(
  "/register-product-code",
  auth,
  [
    check(
      "productCode",
      "Please include a valid product code between 6 and 20 characters"
    )
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
      const user = req.user;
      user.productCode = productCode;

      await user.save();

      return res.json(user);
    } catch (err) {
      logger.error(err.message);
      return res.status(500).send("Server Error");
    }
  }
);

// @route   GET api/users
// @desc    Get all users
// @access  onlyAdmin
router.getP("/", authAdmin, async (req, res) => {
  try {
    const users = await User.find().select("-password").select("-__v");

    return res.json(users);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

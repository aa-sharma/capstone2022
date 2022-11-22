const express = require("../config/express-p");
const router = express.Router();
const bcrypt = require("bcryptjs");
const { check, validationResult } = require("express-validator");
const { User } = require("../models/User");
const logger = require("../utils/logger");
const auth = require("../middleware/auth");
const authAdmin = require("../middleware/authAdmin");
const {
  signJWT,
  paginationResponse,
  isValidObjectId,
} = require("../utils/helpers");
const {
  singleErrorMsg,
  handleExpressValidatorError,
  handleMongooseErrors,
} = require("../utils/handleErrors");

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
      return res.status(400).json(handleExpressValidatorError(errors));
    }
    const { name, email, password } = req.body;

    try {
      let user = await User.findOne({ email });

      if (user) {
        return res.status(400).json(singleErrorMsg("Email already exists"));
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

// @route   PUT api/users/
// @desc    Update your user details including product code
// @access  Private
router.putP("/", auth, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json(handleExpressValidatorError(errors));
    }

    const { productCode, name, password } = req.body;
    let user = await User.findOne({ _id: req.user.id });
    user.productCode = productCode || user.productCode;
    user.name = name || user.name;
    user.password = password || user.password;

    try {
      await user.save();
    } catch (err) {
      return res.status(400).json(handleMongooseErrors(err));
    }

    if (password) {
      const salt = await bcrypt.genSalt(10);
      user.password = await bcrypt.hash(password, salt);
    }

    await user.save();

    user = await User.findOne({ _id: user.id })
      .select("-password")
      .select("-__v");

    return res.json(user);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   GET api/users
// @desc    Get all users
// @access  onlyAdmin
router.getP("/", authAdmin, async (req, res) => {
  try {
    const users = await User.find()
      .select("-password")
      .select("-__v")
      .sort({ admin: "desc", date: "desc" });

    return res.json(
      paginationResponse(users, req.query.page, req.query.pageSize)
    );
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/users/:id
// @desc    delete all users
// @access  onlyAdmin
router.deleteP("/:id", authAdmin, async (req, res) => {
  try {
    if (!isValidObjectId(req.params.id)) {
      return res.status(400).json(singleErrorMsg("not a valid mongodb id"));
    }

    let user = await User.deleteOne({
      _id: req.params.id,
      admin: !true,
    });

    if (!user.deletedCount) {
      return res.status(400).json(singleErrorMsg("User does not exist"));
    }

    return res.json(user);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

// @route   DELETE api/users
// @desc    delete all users
// @access  onlyAdmin
router.deleteP("/", authAdmin, async (req, res) => {
  try {
    const users = await User.deleteMany({ admin: !true });

    if (!users.deletedCount) {
      return res.status(400).json(singleErrorMsg("No users to delete"));
    }

    return res.json(users);
  } catch (err) {
    logger.error(err.message);
    return res.status(500).send("Server Error");
  }
});

module.exports = router;

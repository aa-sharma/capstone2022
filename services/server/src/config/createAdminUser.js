const bcrypt = require("bcryptjs");
const { User } = require("../models/User");
const logger = require("../utils/logger");

const createAdminUser = async () => {
  try {
    let user = await User.findOne({ admin: true });

    if (user) {
      return;
    }

    const salt = await bcrypt.genSalt(10);
    const password = await bcrypt.hash(process.env.SERVER_ADMIN_PASSWORD, salt);

    user = new User({
      name: "admin",
      email: process.env.SERVER_ADMIN_EMAIL,
      password: password,
      admin: true,
    });

    await user.save();
  } catch (err) {
    logger.error(err.message);
  }
};

module.exports = createAdminUser;

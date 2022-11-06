const jwt = require("jsonwebtoken");
const config = require("config");
const logger = require("../utils/logger");
const { User } = require("../models/User");

module.exports = async (req, res, next) => {
  //  Get token from header
  const token = req.header("x-auth-token");

  // Check if token does not exist in header
  if (!token) {
    return res
      .status(401)
      .json(singleErrorMsg("No token, authorization denied"));
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.user.id)
      .select("-password")
      .select("-__v");

    if (!user.admin) {
      return res
        .status(401)
        .json(singleErrorMsg("User is not admin user, authorization denied"));
    }
    req.user = decoded.user;
    next();
  } catch (err) {
    return res.status(401).json(singleErrorMsg("Token is not valid"));
  }
};

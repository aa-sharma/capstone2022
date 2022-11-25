const { User } = require("../models/User");
const logger = require("../utils/logger");
const jwt = require("jsonwebtoken");

module.exports = async (socket, next) => {
  const token = socket.handshake.auth["x-auth-token"];
  if (!token) {
    next(new Error("No token, authorization denied"));
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.user = await User.findById(decoded.user.id)
      .select("-password")
      .select("-__v");
    if (!socket.user) {
      next(new Error("Token is not valid"));
    }
    next();
  } catch (err) {
    logger.error(err);
    next(new Error("Token is not valid"));
  }
};

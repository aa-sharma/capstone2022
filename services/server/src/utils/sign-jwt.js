const jwt = require("jsonwebtoken");
const logger = require("./logger");

const signJWT = async (user) => {
  const payload = {
    user: {
      id: user.id,
    },
  };

  return new Promise(function (resolve, reject) {
    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      {
        expiresIn: 360000,
      },
      (err, token) => {
        if (err) reject(err);
        resolve(token);
      }
    );
  });
};

module.exports = signJWT;

const jwt = require("jsonwebtoken");
const logger = require("./logger");

const handleMongooseErrors = (err) => {
  output = { errors: [] };

  for (error in err.errors) {
    output.errors.push({
      error: err.errors[error].name,
      msg: err.errors[error].message,
    });
  }
  return output;
};

const singleErrorMsg = (msg) => ({ errors: [{ msg }] });

const handleExpressValidatorError = (err) => ({ errors: err.array() });

module.exports = {
  handleMongooseErrors,
  singleErrorMsg,
  handleExpressValidatorError,
};

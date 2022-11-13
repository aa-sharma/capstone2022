const mongoose = require("mongoose");
const logger = require("../utils/logger");

const PositionSchema = mongoose.Schema(
  {
    flexResistor1: {
      type: Number,
      required: [true, "`position.flexResistor1` is required"],
    },
    flexResistor2: {
      type: Number,
      required: [true, "`position.flexResistor2` is required"],
    },
    flexResistor3: {
      type: Number,
      required: [true, "`position.flexResistor3` is required"],
    },
    flexResistor4: {
      type: Number,
      required: [true, "`position.flexResistor4` is required"],
    },
    flexResistor5: {
      type: Number,
      required: [true, "`position.flexResistor5` is required"],
    },
    gyroscope: {
      type: Number,
      required: [true, "`position.gyroscope` is required"],
    },
  },
  {
    toJSON: {
      transform: function (doc, ret) {
        delete ret._id;
      },
    },
  }
);

module.exports = { PositionSchema };

const mongoose = require("mongoose");
const logger = require("../utils/logger");

const PositionSchema = mongoose.Schema(
  {
    pinkyAngle: {
      type: Number,
      required: [true, "`position.pinkyAngle` is required"],
    },
    ringAngle: {
      type: Number,
      required: [true, "`position.ringAngle` is required"],
    },
    middleAngle: {
      type: Number,
      required: [true, "`position.middleAngle` is required"],
    },
    indexAngle: {
      type: Number,
      required: [true, "`position.indexAngle` is required"],
    },
    thumbAngle: {
      type: Number,
      required: [true, "`position.thumbAngle` is required"],
    },
    roll: {
      type: Number,
      required: [true, "`position.roll` is required"],
    },
    pitch: {
      type: Number,
      required: [true, "`position.pitch` is required"],
    },
    yaw: {
      type: Number,
      required: [true, "`position.yaw` is required"],
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

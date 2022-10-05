const mongoose = require("mongoose");

const HandMap = mongoose.Schema({
  _id: {
    type: Number,
    required: true,
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
  },
  // handPositions: {
  //   // an array of hand positions ranging from closed fist to open palm
  //   type: [
  //     {
  //       type: mongoose.Schema.Types.ObjectId,
  //       ref: "HandPosition",
  //     },
  //   ],
  //   required: true,
  // },
  handPosition1: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "HandPosition",
  },
  handPosition2: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "HandPosition",
  },
  handPosition3: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "HandPosition",
  },
  handPosition4: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "HandPosition",
  },
  handPosition5: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "HandPosition",
  },
});

module.exports = mongoose.model("HandMap", HandMap);

const mongoose = require("mongoose");

const Level = mongoose.Schema({
  _id: {
    type: Number,
    required: true,
  },
  exercise: {
    type: [{ type: String, required: true }], // ["handPosition1", "handPosition3", "handPosition5"]
  },
});

module.exports = mongoose.model("Level", Level);

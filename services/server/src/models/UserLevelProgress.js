const mongoose = require("mongoose");

const UserLevelProgress = mongoose.Schema({
  _id: {
    type: Number,
    required: true,
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
  },
  level: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Level",
  },
  exercisesCompleted: [
    {
      exercise: {
        type: String, // "handPosition1"
        required: true,
      },
      time: {
        type: Number, // completed in 5 seconds
        required: true,
      },
    },
  ],
});

module.exports = mongoose.model("UserLevelProgress", UserLevelProgress);

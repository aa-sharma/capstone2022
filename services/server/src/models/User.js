const mongoose = require("mongoose");

const UserSchema = mongoose.Schema({
  name: {
    type: String,
    required: [true, "`name` is required"],
  },
  email: {
    type: String,
    required: [true, "`email` is required"],
    unique: [true, "`email` must be unique"],
  },
  password: {
    type: String,
    required: [true, "`password` is required"],
    validate: {
      validator: (v) => v.length >= 6,
      message: () => "`password` must be greater than 6 characters",
    },
  },
  productCode: {
    type: String,
    required: false,
    validate: {
      validator: (v) => v.length >= 6 && v.length <= 20,
      message: () => "`productCode` must be between 6 and 20 characters",
    },
  },
  admin: {
    type: Boolean,
    default: false,
  },
  date: {
    type: Date,
    default: Date.now,
  },
});

const User = mongoose.model("User", UserSchema);

module.exports = { User, UserSchema };

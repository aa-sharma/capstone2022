const mongoose = require("mongoose");
const { UserLevelProgress } = require("./UserLevelProgress");

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
      message: () => "`password` must be greater than 5 characters",
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

// `this` is not accessible unless the function is NON-ES6 syntax for some weird reason...
// delete userLevelProgress if user is deleted.
async function preDelete() {
  const doc = await User.findOne(this.getFilter());
  if (doc) {
    await UserLevelProgress.deleteMany({ user: doc._id });
  }
}

UserSchema.pre("deleteOne", preDelete);
UserSchema.pre("deleteMany", preDelete);

const User = mongoose.model("User", UserSchema);

module.exports = { User, UserSchema };

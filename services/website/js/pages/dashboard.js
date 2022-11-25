import API from "../modules/api.js";

const token = localStorage["token"];

let myVariable = document.getElementsByClassName("my-class");
console.log(myVariable[0]);

const api = new API({ url: "/api/exercise", token });
const { json } = await api.call();

console.log(json);

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js";
import {
  getAuth,
  onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/9.4.0/firebase-auth.js";
import { getDatabase } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-database.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-analytics.js";


const firebaseConfig = {
    apiKey: "AIzaSyDPYvTnU3I0P_IdKOSnmrmGwldvhUZjJoI",
    authDomain: "capstone2022-4f612.firebaseapp.com",
    projectId: "capstone2022-4f612",
    storageBucket: "capstone2022-4f612.appspot.com",
    messagingSenderId: "904570161227",
    appId: "1:904570161227:web:506cd785ef1c8c6efee5ce",
    measurementId: "G-WV599N592B"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const analytics = getAnalytics(app);


document.getElementById('signup-btn').addEventListener('click', signup);


const auth = getAuth(app);
// onAuthStateChanged(auth, (user) => {
//   if (user) {
//     // User is signed in, see docs for a list of available properties
//     // https://firebase.google.com/docs/reference/js/firebase.User
//     const uid = user.uid;

//     // document.getElementById("user_div").style.display = "initial";
//     // document.getElementById("login_div").style.display = "none";

//   } else {
//     // User is signed out
//     // document.getElementById("user_div").style.display = "none";
//     // document.getElementById("login_div").style.display = "initial";
// }
// });

function signup() {
    console.log("[INFO] Attempting to register user...")
    var userEmail = document.getElementById("email_field").value;
    var userPassword = document.getElementById("password_field").value;
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;

    const auth = getAuth(app);
    createUserWithEmailAndPassword(auth, userEmail, userPassword)
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        window.alert("user created for :" + firstName + lastName)
        // ...
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;

        window.alert("Error: " + errorMessage);
    });

}

function login() {
    console.log("[INFO] Attempting to login user...")
    var userEmail = document.getElementById("email_field").value;
    var userPassword = document.getElementById("password_field").value;

    const auth = getAuth();
    signInWithEmailAndPassword(auth, userEmail, userPassword)
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        // ...
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;

        window.alert("Error: " + errorMessage);
    });

}

function logout() {
    const auth = getAuth();
    signOut(auth).then(() => {
      // Sign-out successful.
    }).catch((error) => {
      // An error happened.
    });
}
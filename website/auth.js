    // Import the functions you need from the SDKs you need
    import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
    import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js";
    import { getDatabase, set, ref } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";

    // import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
    // TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries
  
    // Your web app's Firebase configuration
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    const firebaseConfig = {
      apiKey: "AIzaSyDPYvTnU3I0P_IdKOSnmrmGwldvhUZjJoI",
      authDomain: "capstone2022-4f612.firebaseapp.com",
      databaseURL: "https://capstone2022-4f612-default-rtdb.firebaseio.com",
      projectId: "capstone2022-4f612",
      storageBucket: "capstone2022-4f612.appspot.com",
      messagingSenderId: "904570161227",
      appId: "1:904570161227:web:506cd785ef1c8c6efee5ce",
      measurementId: "G-WV599N592B"
    };
  
    // Initialize Firebase
    const app = initializeApp(firebaseConfig);
    // const analytics = getAnalytics(app);
    const auth = getAuth(app);
    const database = getDatabase(app);

    signUp.addEventListener('click',(e) => {
        var email = document.getElementById('email_field').value;
        var password = document.getElementById('password_field').value;
        var first_name = document.getElementById('first_name').value;
        var last_name = document.getElementById('last_name').value;
        createUserWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;
            set(ref(database, 'users/' + user.uid), {
                email: email,
                first_name: first_name,
                last_name: last_name
            })
                .then( () => {
                    alert('User created succesfully');
                })
                .catch((error) => {
                    alert(error);
                });
            
            // ...
            })
            .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(errorMessage);
            // ..
            });
    });


    login.addEventListener('click', (e) => {
        var email = document.getElementById('email_field').value;
        var password = document.getElementById('password_field').value;
        signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
        })
            .then( () => {
                alert('Login successful');
            })
            .catch((error) => {
                alert(error);
            }); 

    });


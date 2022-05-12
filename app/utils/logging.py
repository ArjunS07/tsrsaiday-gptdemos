import pyrebase
config = {
    "apiKey": "AIzaSyDu1ZmLgrsfLFrU_9KqI_pqB_QDK9EJCx0",
    "authDomain": "aiday-3d73b.firebaseapp.com",
    "projectId": "aiday-3d73b",
    "storageBucket": "aiday-3d73b.appspot.com",
    "appId": "1:740559734267:web:836a41cd16f32bb216f75e",
    "serviceAccount": "app/utils/aiday-3d73b-firebase-adminsdk-a8c5j-5f20c99697.json",
    "databaseURL": "https://aiday-3d73b-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()


def log_to_firebase(data, type):
    if type == "story":
        """
        Data in the format:
        word1: "", 
        word2: "",
        word3: "",
        word4: "",
        story: "",
        timestamp: ""
        """
        database.child("stories").push(data)
    elif type == "completion":
        """
        Data in the format:
        sent1: "", 
        sent2: "",
        para: "",
        timestamp: ""
        """
        database.child("completions").push(data)

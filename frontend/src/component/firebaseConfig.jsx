import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
const firebaseConfig = {
  apiKey: "AIzaSyBuYEHYtdvfTSzKA-enibx9bm1rtRNHGKA",
  authDomain: "resume-analyzer-a310d.firebaseapp.com",
  projectId: "resume-analyzer-a310d",
  storageBucket: "resume-analyzer-a310d.firebasestorage.app",
  messagingSenderId: "118707069232",
  appId: "1:118707069232:web:ea03ed27284464f8d728f5"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);


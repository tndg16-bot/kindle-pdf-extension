import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// import { getAnalytics } from "firebase/analytics"; // Analytics is optional and client-side only

const firebaseConfig = {
    apiKey: "FIREBASE_API_KEY_PLACEHOLDER",
    authDomain: "gamified-mandala.firebaseapp.com",
    projectId: "gamified-mandala",
    storageBucket: "gamified-mandala.firebasestorage.app",
    messagingSenderId: "108564617362",
    appId: "1:108564617362:web:5d586bf07a3a3628eeae4b",
    measurementId: "G-LC2EDGSF83"
};

// Initialize Firebase (Singleton pattern to avoid errors in dev HMR)
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
export const auth = getAuth(app);
export const db = getFirestore(app);

// Analytics can be initialized purely on client side if needed, skipping for MVP logic

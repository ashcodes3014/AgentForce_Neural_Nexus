import { createContext, useContext, useEffect, useState } from 'react';
import { auth, db} from './firebaseConfig';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, query, where, getDocs } from "firebase/firestore";
import { useDispatch } from 'react-redux';
import {setUserId}  from './slicer'
const AuthContext = createContext(); 

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const dispatch = useDispatch();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, user => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  useEffect(()=>{
    async function get() {
      if (currentUser) {
      const q = query(
        collection(db, "users"),
        where("email", "==", currentUser.email)
      );

    const querySnapshot = await getDocs(q);
    querySnapshot.forEach((doc) => {
      dispatch(setUserId(doc.id))
    });
  }
    }

  get();
  },[currentUser]);

  const value = {
    currentUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}




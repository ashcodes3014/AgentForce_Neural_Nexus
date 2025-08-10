import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './component/authContext';
import AuthForm from './component/auth';
import Home from './component/home';
import PrivateRoute from './component/privateRoute';
import {Provider }  from 'react-redux'
import store from './component/store'

function App() {
  return (
    <Provider store={store}>    
      <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<AuthForm />} />
          <Route path="/signup" element={<AuthForm />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </Router>
    </Provider>
  );
}

export default App;
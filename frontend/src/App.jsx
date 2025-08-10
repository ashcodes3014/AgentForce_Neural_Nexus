import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './component/authContext';
import AuthForm from './component/auth';
import Home from './component/home';
import PrivateRoute from './component/privateRoute';

function App() {
  return (
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
  );
}

export default App;
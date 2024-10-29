// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/common/Navbar';
import Dashboard from './pages/Dashboard';
import Market from './pages/Market';
import Portfolio from './pages/Portfolio';
import Trade from './pages/Trade';
import Login from './pages/Login';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { useEffect } from 'react';
import dogecoinGif from './assets/dogecoin.gif';

// Loading component
const LoadingScreen = () => (
  <div className="min-h-screen bg-gray-900 flex items-center justify-center">
    <div className="bg-gray-900/50 backdrop-blur-sm p-8 rounded-lg shadow-lg text-center">
      <img 
        src={dogecoinGif} 
        alt="Loading..."
        className="w-24 h-24 mx-auto mb-4" // Adjust size as needed
      />
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
      <div className="text-xl font-semibold text-gray-100">Loading...</div>
    </div>
  </div>
);

// Separate component for the app content to use hooks
const AppContent = () => {
  const { user, loading } = useAuth();
  
  useEffect(() => {
    console.log('Auth state changed - User:', user, 'Loading:', loading);
  }, [user, loading]);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    // Dark theme with gradient
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Navbar />
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto">
          <Routes>
            <Route 
              path="/login" 
              element={user ? <Navigate to="/dashboard" replace /> : <Login />} 
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <div className="space-y-6">
                    <Dashboard />
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/market"
              element={
                <ProtectedRoute>
                  <div className="space-y-6">
                    <Market />
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/portfolio"
              element={
                <ProtectedRoute>
                  <div className="space-y-6">
                    <Portfolio />
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/trade"
              element={
                <ProtectedRoute>
                  <div className="space-y-6">
                    <Trade />
                  </div>
                </ProtectedRoute>
              }
            />
            <Route 
              path="/" 
              element={<Navigate to={user ? "/dashboard" : "/login"} replace />} 
            />
            {/* 404 Route */}
            <Route
              path="*"
              element={
                <div className="min-h-[60vh] flex items-center justify-center">
                  <div className="bg-gray-900/50 backdrop-blur-sm p-8 rounded-lg shadow-lg text-center">
                    <h2 className="text-2xl font-bold text-gray-100 mb-2">Page Not Found</h2>
                    <p className="text-gray-300 mb-4">The page you're looking for doesn't exist.</p>
                    <button
                      onClick={() => window.history.back()}
                      className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors duration-200 font-medium"
                    >
                      Go Back
                    </button>
                  </div>
                </div>
              }
            />
          </Routes>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="mt-auto py-6 px-4 border-t border-gray-800">
        <div className="max-w-7xl mx-auto text-center text-gray-400 text-sm">
          © {new Date().getFullYear()} Crypto Mock. All rights reserved.   Site created by Darragh Larkin.
        </div>
      </footer>
    </div>
  );
};

// Main App component
const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default App;
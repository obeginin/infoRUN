import { Routes, Route } from "react-router-dom";
import { Auth } from "../Pages/Auth/Auth.tsx";
import { Profile } from "../Pages/Profile/Profile.tsx";
import { Home } from "../Pages/Home/Home.tsx";
import { ProtectedRoute } from "../Processes/ProtectedRoute/ProtectedRoute.tsx";
function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />s
        <Route path="/auth" element={<Auth />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;

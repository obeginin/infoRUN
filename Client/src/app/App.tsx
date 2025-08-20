import { Routes, Route } from "react-router-dom";
import { Auth } from "../Pages/Auth/Auth.tsx";
import { Profile } from "../Pages/Profile/Profile.tsx";
import { Home } from "../Pages/Home/Home.tsx";
import { ProtectedRoute } from "../Processes/ProtectedRoute/ProtectedRoute.tsx";
import { ProfileAllTasks } from "../Pages/Profile/ProfileAllTasks/ProfileAllTasks.tsx";
import { Politics } from "../Pages/Politics/Politics.tsx";
import { Admin } from "../Pages/Admin/Admin.tsx";
import { Registration } from "../Pages/Registration/Registration.tsx";
import { RegistrationMailSend } from "../Widgets/Registration/RegistratiionMailSend.tsx";
import { SuccessRegistration } from "../Widgets/Registration/SuccessRegistration/SuccessRegistration.tsx";
import { ProfileTask } from "../Pages/Profile/ProfileTask/ProfileTask.tsx";
import { ForgotPassword } from "../Pages/ForgotPassword/ForgotPassword.tsx";
import { ResetPassword } from "../Pages/ForgotPassword/ResetPassword/ResetPassword.tsx";
function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/politics" element={<Politics />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/registration" element={<Registration />} />
        <Route
          path="/registration/mail-send"
          element={<RegistrationMailSend />}
        />
        <Route path="/auth/confirm-email" element={<SuccessRegistration />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/auth/reset-password" element={<ResetPassword />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile/all-tasks"
          element={
            <ProtectedRoute>
              <ProfileAllTasks />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile/task/:id"
          element={
            <ProtectedRoute>
              <ProfileTask />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <Admin />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;

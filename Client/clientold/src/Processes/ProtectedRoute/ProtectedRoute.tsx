import { Navigate } from "react-router-dom";
import { useUserStore } from "../../store/userStore";
export const ProtectedRoute = ({ children }: { children: React.ReactElement }) => {
  const user = useUserStore((state) => state.user);
  if (!user) {
    return <Navigate to="/auth" replace />;
  }
  return children;
};
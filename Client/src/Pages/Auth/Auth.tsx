import { Header } from "../../Widgets/Header/Header";
import { AuthForm } from "../../Widgets/AuthForm/AuthForm";

export const Auth = () => {
  return (
    <div style={{ height: "100vh" }}>
      <Header />
      <AuthForm />
    </div>
  );
};

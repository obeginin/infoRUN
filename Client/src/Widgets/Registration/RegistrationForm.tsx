import { useNavigate } from "react-router-dom";
import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../ui/buttonDeafault/Button";
import { Input } from "../../ui/input/Input";
import { Paragraph } from "../../ui/p/Paragraph";
import styles from "./RegistrationForm.module.scss";
import { useEffect, useState } from "react";
import AuthAPI from "../../API/registration";
export const RegistrationForm = () => {
  const [Login, setLogin] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const nav = useNavigate();

  const handleClick = () => {
    if (Login.length <= 3) {
      setLoginError(true);
      return;
    }
    if (email.length <= 3 || !email.includes("@")) {
      setEmailError(true);
      return;
    }
    if (password.length <= 3) {
      setPasswordError(true);
      return;
    }

    AuthAPI.registration(email, Login, password);
    nav("/registration/mail-send", {
      state: { email: email, login: Login, password: password },
    });
  };

  useEffect(() => {
    setLoginError(false);
    setEmailError(false);
    setPasswordError(false);
  }, [Login, email, password]);
  return (
    <div className="app">
      <div className={styles.container}>
        <ProfileContentContainer>
          <div className={styles.form}>
            <Paragraph>Регистрация</Paragraph>
            <Input
              error_text={
                loginError ? "Логин должен состоять минимум из 4 символов" : ""
              }
              required
              radius="16px"
              type="text"
              label="Логин"
              value={Login}
              onChange={(e) => setLogin(e.target.value)}
            />
            <Input
              error_text={
                emailError ? "Email должен состоять минимум из 4 символов" : ""
              }
              required
              radius="16px"
              type="text"
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              error_text={
                passwordError
                  ? "Пароль должен состоять минимум из 4 символов"
                  : ""
              }
              required
              radius="16px"
              type="password"
              label="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
              onClick={() => handleClick()}
              style={{
                border: "none",
                background: "none",
                color: "var(--primary)",
              }}
            >
              Далее
            </Button>
          </div>
        </ProfileContentContainer>
      </div>
    </div>
  );
};

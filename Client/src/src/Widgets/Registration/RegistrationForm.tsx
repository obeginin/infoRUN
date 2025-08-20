"use client";

import { useRouter } from "next/navigation";
import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../ui/buttonDeafault/Button";
import { Input } from "../../ui/input/Input";
import { Paragraph } from "../../ui/p/Paragraph";
import styles from "./RegistrationForm.module.scss";
import { useEffect, useState } from "react";
import AuthAPI from "../../API/registration";
export const RegistrationForm = () => {
  const [login, setLogin] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [tel, setTel] = useState("");
  const [loginError, setLoginError] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  // const [telError, setTelError] = useState(false);
  const router = useRouter();

  const handleClick = () => {
    if (login.length <= 3) {
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

    AuthAPI.registration(email, login, password, tel);
    sessionStorage.setItem(
      "registrationData",
      JSON.stringify({
        email,
        login,
        password,
        tel,
      })
    );
    router.push("/registration/confirm-email");
  };

  useEffect(() => {
    setLoginError(false);
    setEmailError(false);
    setPasswordError(false);
  }, [login, email, password]);
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
              value={login}
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
            <Input
              radius="16px"
              required
              type="number"
              label="Телефон"
              value={tel}
              onChange={(e) => setTel(e.target.value)}
            />

            <Button
              type="submit"
              onClick={() => handleClick()}
              filled
              width="full"
              color="white"
            >
              Далее
            </Button>
            <Button outlined width="full" onClick={() => router.push("/auth")}>
              Уже есть аккаунт
            </Button>
          </div>
        </ProfileContentContainer>
      </div>
    </div>
  );
};

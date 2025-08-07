import { useNavigate } from "react-router-dom";
import { useUserStore } from "../../store/userStore";
import { Link } from "../../ui/Link/Link";
import { Button } from "../../ui/buttonDeafault/Button";
import { Input } from "../../ui/input/Input";
import styles from "./AuthForm.module.scss";
import { useEffect, useState } from "react";
import { Paragraph } from "../../ui/p/Paragraph";
import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";

export const AuthForm = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const userLogin = useUserStore((state) => state.login);
  const useUser = useUserStore((state) => state.user);
  const error = useUserStore((state) => state.error);
  const [loginError, setLoginError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const clearError = useUserStore((state) => state.clearError);
  const navigate = useNavigate();

  const handleClick = () => {
    userLogin(login, password);

    if (error?.error === "LoginNotFoud") {
      setLogin("");
    }

    if (error?.error === "PasswordFailed") {
      setPassword("");
    }
  };

  useEffect(() => {
    if (useUser) navigate("/profile");
  }, [useUser, navigate, userLogin]);

  useEffect(() => {
    setLoginError(false);
    setPasswordError(false);
    clearError();
  }, [login, password, clearError]);

  useEffect(() => {
    if (!error) return;
    if (error.error === "LoginNotFound") {
      setLoginError(true);
    }
    if (error.error === "PasswordFailed") {
      setPasswordError(true);
    }
  }, [error]);

  return (
    <div className={styles["auth-form-outer"]}>
      <div className={styles.container}>
        <ProfileContentContainer>
          <div className={styles.form}>
            <Paragraph>Авторизация</Paragraph>
            <Input
              type="text"
              label="Логин"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              radius="16px"
              error_text={loginError ? "Логин не найден" : ""}
            />
            <Input
              type="password"
              label="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              radius="16px"
              error_text={passwordError ? error?.message : ""}
            />
            <Button
              onClick={() => handleClick()}
              filled
              color="white"
              width="full"
              radius="16px"
            >
              Вход
            </Button>
            <Link href="/forgot-password">Забыли пароль?</Link>
            <Link href="/registration">Зарегистрироваться</Link>
          </div>
        </ProfileContentContainer>
      </div>
    </div>
  );
};

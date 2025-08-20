"use client";

import { useUserStore } from "@/src/store/userStore";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Input } from "@/src/ui/input/Input";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./AuthForm.module.scss";
import { useEffect, useState } from "react";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { AnimationLink } from "@/src/ui/AnimationLink/AnimationLink";
import { useRouter } from "next/navigation";
export const AuthForm = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const userLogin = useUserStore((state) => state.login);
  const useUser = useUserStore((state) => state.user);
  const loading = useUserStore((state) => state.loading);
  const error = useUserStore((state) => state.error);
  const [loginError, setLoginError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const clearError = useUserStore((state) => state.clearError);
  const router = useRouter();

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
    if (useUser) router.push("/profile");
  }, [useUser, router, userLogin]);

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
              loading={loading}
            >
              Вход
            </Button>
            <ul>
              <AnimationLink href="/forgot-password" size="small">
                Забыли пароль?
              </AnimationLink>
              <AnimationLink href="/registration" size="small">
                Регистрация
              </AnimationLink>
            </ul>
          </div>
        </ProfileContentContainer>
      </div>
    </div>
  );
};

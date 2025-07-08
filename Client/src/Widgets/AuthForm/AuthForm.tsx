import { useNavigate } from "react-router-dom";
import { useUserStore } from "../../store/userStore";
import { Link } from "../../ui/Link/Link";
import { Button } from "../../ui/buttonDeafault/Button";
import { Input } from "../../ui/input/Input";
import { SelectButton } from "../../ui/selectButton/SelectButton";
import styles from "./AuthForm.module.scss";
import { useEffect, useState } from "react";

export const AuthForm = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [activeButton, setActiveButton] = useState("Вход");
  const userLogin = useUserStore((state) => state.login);
  const useUser = useUserStore((state) => state.user);
  const navigate = useNavigate();

  const handleClick = () => {
    if (activeButton === "Вход") userLogin(login, password);
  };
  useEffect(() => {
    if (useUser) navigate("/profile");
  }, [useUser, navigate, userLogin]);

  return (
    <div className={styles.auth__form}>
      <div className={styles.auth__form__content}>
        <SelectButton
          first_value="Вход"
          second_value="Регистрация"
          activeButton={activeButton}
          setActiveButton={setActiveButton}
        />
        <Input
          type="text"
          label="Логин"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <Input
          type="password"
          label="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Link href="">Забыли пароль?</Link>
        <Button onClick={() => handleClick()}>Вход</Button>
      </div>
    </div>
  );
};

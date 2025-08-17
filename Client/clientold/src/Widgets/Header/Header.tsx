import burger from "../../assets/burger-menu.svg";
import { Button } from "../../ui/buttonDeafault/Button";
import styles from "./Header.module.scss";
import { useUserStore } from "../../store/userStore";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
export const Header = () => {
  const nav = useNavigate();
  const useUserLogout = useUserStore((state) => state.logout);
  const user = useUserStore((state) => state.user);
  const theme = localStorage.getItem("theme");
  const [isDark, setIsDart] = useState(theme === "dark" ? true : false);

  const handleClick = () => {
    setIsDart(!isDark);
    localStorage.setItem("theme", isDark ? "light" : "dark");
  };

  useEffect(() => {
    const theme = localStorage.getItem("theme");
    document.documentElement.setAttribute("data-theme", theme as string);
  }, [isDark]);

  return (
    <header className={styles.header}>
      <div className={styles.content__right}>
        <img src={burger} alt="" className={styles.burger} />
        {user?.RoleName === "Админ" && (
          <Button color="white" filled onClick={() => nav("/admin")}>
            admin
          </Button>
        )}
        <ul className={styles.list}>
          <li>
            <a href="/profile/all-tasks">Мои задачи</a>
          </li>
          <li>
            <a href="/">Категории заданий</a>
          </li>
        </ul>
        <div
          className={
            styles.theme_switcher + " " + (isDark ? styles.dark : styles.light)
          }
        >
          <i onClick={() => handleClick()} className={`pi pi-sun`}></i>
        </div>
        {!user ? (
          <Button filled onClick={() => nav("/auth")}>
            Войти
          </Button>
        ) : (
          <Button outlined onClick={useUserLogout}>
            Выйти
          </Button>
        )}
      </div>
    </header>
  );
};

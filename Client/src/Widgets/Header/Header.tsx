import burger from "../../assets/burger-menu.svg";
import { Button } from "../../ui/buttonDeafault/Button";
import styles from "./Header.module.scss";
import { useUserStore } from "../../store/userStore";
import { useNavigate } from "react-router-dom";
export const Header = () => {
  const nav = useNavigate();
  const useUserLogout = useUserStore((state) => state.logout);
  const user = useUserStore((state) => state.user);
  return (
    <header className={styles.header}>
      <div className={styles.content__right}>
        <img src={burger} alt="" className={styles.burger} />
        {user?.RoleName === "Админ" && (
          <Button filled onClick={() => nav("/admin")}>
            Панель администратора
          </Button>
        )}
        <ul className={styles.list}>
          <li>
            <a href="/">Мои задачи</a>
          </li>
          <li>
            <a href="/">Категории заданий</a>
          </li>
        </ul>
        {!user ? (
          <Button filled onClick={() => nav("/auth")}>
            Войти
          </Button>
        ) : (
          <Button
            style={{
              border: "1px solid var(--primary)",
              backgroundColor: "transparent",
            }}
            onClick={useUserLogout}
          >
            Выйти
          </Button>
        )}
      </div>
    </header>
  );
};

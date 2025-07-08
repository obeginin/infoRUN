import burger from "../../assets/burger-menu.svg";
import { ListHeader } from "../../Features/ListHeader/ListHeader";
import { Button } from "../../ui/buttonDeafault/Button";
import styles from "./Header.module.scss";
import { useUserStore } from "../../store/userStore";
export const Header = () => {
    const list = ["Мои задачи", "Категории заданий"];
    const useUserLogout = useUserStore((state) => state.logout);
  return (
    <header className={styles.header}>
      <img src={burger} alt="" style={{ width: "40px", height: "40px" }} />
      <div className={styles.content__right}>
        <ListHeader children={list} />
        <Button onClick={useUserLogout}>Выход</Button>
      </div>
    </header>
  );
};

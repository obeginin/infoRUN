import styles from "./Popup.module.scss";
import { useAdminStore } from "../../../../Pages/Admin/store";

export const Popup = () => {
  const { setVisibleDialogPassword, setVisibleDialogDelete } = useAdminStore();
  return (
    <>
      <div className={styles.popup}>
        <button className={styles.btn} onClick={() => setVisibleDialogDelete()}>
          Удалить
        </button>
        <button
          className={styles.btn_change}
          onClick={() => setVisibleDialogPassword()}
        >
          Изменить пароль
        </button>
      </div>
    </>
  );
};

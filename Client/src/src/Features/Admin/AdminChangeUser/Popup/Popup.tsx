'use client'

import styles from "./Popup.module.scss";
import { useAdminStore } from "@/src/store/adminStore";

export const Popup = () => {
  const {
    setVisibleDialogPassword,
    setVisibleDialogDelete,
    setVisibleDialogEdit,
  } = useAdminStore();
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
        <button className={styles.btn} onClick={() => setVisibleDialogEdit()}>
          Изменить пользователя
        </button>
      </div>
    </>
  );
};

'use client';

import { Button } from "../../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../../ui/p/Paragraph";
import styles from "./DialogDelete.module.scss";
import { useAdminStore } from "@/src/store/adminStore";
import { IDialog } from "../../../../ui/IDialog/IDialog";
export const DialogDelete = () => {
  const token = localStorage.getItem("token") || "";
  const {
    currentUser,
    deleteUser,
    isVisibleDialogDelete,
    setVisibleDialogDelete,
  } = useAdminStore();
  return (
    <>
      <IDialog
        visible={isVisibleDialogDelete}
        setVdisible={setVisibleDialogDelete}
      >
        <div className={styles.dialog}>
          <Paragraph size="medium">Вы уверены?</Paragraph>
          <Paragraph>Логин: {currentUser?.Login}</Paragraph>
          <Paragraph>Имя: {currentUser?.First_Name}</Paragraph>
          <Paragraph>Email: {currentUser?.Email}</Paragraph>
          <div className={styles.dialog__btn}>
            <Button outlined onClick={() => setVisibleDialogDelete()}>
              Отменить
            </Button>
            <Button
              type="submit"
              color="white"
              filled
              onClick={() => deleteUser(token, currentUser?.ID as number)}
            >
              Удалить
            </Button>
          </div>
        </div>
      </IDialog>
    </>
  );
};

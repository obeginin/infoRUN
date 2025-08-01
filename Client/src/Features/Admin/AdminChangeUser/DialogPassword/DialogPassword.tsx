import { Dialog } from "primereact/dialog";
import { Button } from "../../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../../ui/p/Paragraph";
import styles from "../DialogDelete/DialogDelete.module.scss";
import { Input } from "../../../../ui/input/Input";
import { useAdminStore } from "../../../../Pages/Admin/store";
import { useEffect, useState } from "react";
export const DialogPassword = () => {
  const token = localStorage.getItem("token") || "";
  const {
    currentUser,
    changePassword,
    isVisibleDialogPassword,
    setVisibleDialogPassword,
  } = useAdminStore();
  const [passwordError, setPasswordError] = useState(false);
  const [newPassword, setNewPassword] = useState("");

  const handleClick = () => {
    if (newPassword.length < 6) {
      setPasswordError(true);
    } else {
      changePassword(token, currentUser?.ID as number, newPassword);
    }
  };

  useEffect(() => {
    setPasswordError(false);
  }, [newPassword]);
  return (
    <>
      <Dialog
        visible={isVisibleDialogPassword}
        onHide={() => setVisibleDialogPassword()}
        style={{ width: "370px", maxHeight: "500px" }}
      >
        <div className={styles.dialog}>
          <Paragraph size="medium">Изменить пароль пользователю</Paragraph>
          <Paragraph>Логин: {currentUser?.Login}</Paragraph>
          <Paragraph>Имя: {currentUser?.First_Name}</Paragraph>
          <Paragraph>Email: {currentUser?.Email}</Paragraph>
          <Input
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            label="Новый пароль"
            error_text={
              passwordError ? "Пароль должен быть больше 6 символов" : ""
            }
          />
          <div className={styles.dialog__btn}>
            <Button outlined onClick={() => setVisibleDialogPassword()}>
              Отменить
            </Button>
            <Button
              type="submit"
              color="white"
              filled
              onClick={() => handleClick()}
            >
              Сохранить
            </Button>
          </div>
        </div>
      </Dialog>
    </>
  );
};

import { Dialog } from "primereact/dialog";
import { Button } from "../../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../../ui/p/Paragraph";
import styles from "./DialogDelete.module.scss";
import { useAdminStore } from "../../../../Pages/Admin/store";
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
      <Dialog
        visible={isVisibleDialogDelete}
        onHide={() => setVisibleDialogDelete()}
        style={{ width: "370px", maxHeight: "500px" }}
      >
        <div className={styles.dialog}>
          <Paragraph size="medium">Are you sure?</Paragraph>
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
              onClick={() => deleteUser(token, currentUser?.Email || "")}
            >
              Удалить
            </Button>
          </div>
        </div>
      </Dialog>
    </>
  );
};

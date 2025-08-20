import { Dialog } from "primereact/dialog";
import styles from "./IDialog.module.scss";
interface IDialogProps {
  children: React.ReactNode;
  visible: boolean;
  setVdisible: React.Dispatch<React.SetStateAction<boolean>>;
  closeIcon?: boolean;
}

export const IDialog = ({ children, visible, setVdisible, closeIcon=false }: IDialogProps) => {
  return (
    <Dialog
      className={styles.dialog}
      visible={visible}
      onHide={() => setVdisible(false)}
      closeIcon={closeIcon}
    >
      {children}
    </Dialog>
  );
};

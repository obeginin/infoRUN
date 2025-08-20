import { Dialog } from "primereact/dialog";
import styles from "./IDialog.module.scss";
interface IDialogProps {
  children: React.ReactNode;
  visible: boolean;
  setVdisible: React.Dispatch<React.SetStateAction<boolean>>;
}

export const IDialog = ({ children, visible, setVdisible }: IDialogProps) => {
  return (
    <Dialog className={styles.dialog} visible={visible} onHide={() => setVdisible(false)}>
      {children}
    </Dialog>
  );
};

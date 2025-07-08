import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import edit from "../../assets/edit.svg";
import { useUserStore } from "../../store/userStore";
import { Button } from "../../ui/buttonDeafault/Button";
import { Paragraph } from "../../ui/p/Paragraph";
import { ChangePassword } from "../ChangePassword/ChangePassword";
import { useState } from "react";
import { Dialog } from "primereact/dialog";

import styles from "./ProfileGreatings.module.scss";
export const ProfileGreatings = () => {
  const useUser = useUserStore((state) => state.user);
  const [open, setOpen] = useState(false);
  return (
    <>
      <ProfileContentContainer>
        <div className={styles.greatings}>
          <div className={styles.greatings__left}>
            <Paragraph size="large">Привет, {useUser?.first_name}!</Paragraph>
            <Paragraph>ЕГЭ, которое ты сдаешь: Информатика</Paragraph>
          </div>

          <div className={styles.greatings__right}>
            <div className={styles.edit__email}>
              <Paragraph>{useUser?.email}</Paragraph>
              <img src={edit} alt="" />
            </div>
            <Button onClick={() => setOpen(!open)}>Сменить пароль</Button>
          </div>
        </div>
      </ProfileContentContainer>

      {open && (
        <Dialog visible={open} onHide={() => setOpen(false)} >
          <ChangePassword />
        </Dialog>
      )}
    </>
  );
};

import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import edit from "../../../assets/edit_white.svg";
import { useUserStore } from "../../../store/userStore";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import { ChangePassword } from "../../ChangePassword/ChangePassword";
import { useState } from "react";
import { Dialog } from "primereact/dialog";

import styles from "./ProfileGreatings.module.scss";
export const ProfileGreatings = () => {
  const useUser = useUserStore((state) => state.user);
  const [open, setOpen] = useState(false);
  return (
    <>
      <ProfileContentContainer color="primary">
        <div className={styles.greatings}>
          <div className={styles.greatings__left}>
            <Paragraph size="large" color="white">
              Привет, {useUser?.First_Name ? useUser.First_Name : "новый пользователь"}!
            </Paragraph>
            <Paragraph color="white">
              ЕГЭ, которое ты сдаешь: Информатика
            </Paragraph>
          </div>

          <div className={styles.greatings__right}>
            <div className={styles.edit__email}>
              <Paragraph color="white">{useUser?.Email}</Paragraph>
              <img src={edit} alt="" style={{ cursor: "pointer" }} />
            </div>
            <Button
              style={{
                backgroundColor: "var(--primary)",
                color: "var(--bg)",
                border: "1px solid var(--bg)",
              }}
              onClick={() => setOpen(!open)}
            >
              Сменить пароль
            </Button>
          </div>
        </div>
      </ProfileContentContainer>

      {open && (
        <Dialog visible={open} onHide={() => setOpen(false)}>
          <ChangePassword />
        </Dialog>
      )}
    </>
  );
};

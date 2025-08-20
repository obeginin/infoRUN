"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import edit from "@public/assets/edit_white.svg";
import { useUserStore } from "@/src/store/userStore";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { ChangePassword } from "../../ChangePassword/ChangePassword";
import { useState } from "react";
import { IDialog } from "@/src/ui/IDialog/IDialog";
import Image from "next/image";

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
              Привет,{" "}
              {useUser?.First_Name ? useUser.First_Name : "новый пользователь"}!
            </Paragraph>
            <Paragraph color="white">
              ЕГЭ, которое ты сдаешь: Информатика
            </Paragraph>
          </div>

          <div className={styles.greatings__right}>
            <div className={styles.edit__email}>
              <Paragraph color="white">{useUser?.Email}</Paragraph>
              <Image src={edit} alt="" style={{ cursor: "pointer" }} />
            </div>
            <Button
              border='white' color="white" outlined
              onClick={() => setOpen(!open)}
            >
              Сменить пароль
            </Button>
          </div>
        </div>
      </ProfileContentContainer>

      {open && (
        <IDialog visible={open} setVdisible={setOpen}>
          <ChangePassword />
        </IDialog>
      )}
    </>
  );
};

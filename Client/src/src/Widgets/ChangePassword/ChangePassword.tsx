'use client'

import { useState } from "react";
import { Input } from "@/src/ui/input/Input";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./ChangePassword.module.scss";
import { Button } from "@/src/ui/buttonDeafault/Button";
import UserPassword from "@/src/API/password";
export const ChangePassword = () => {
  const [oldPass, setOldPass] = useState("");
  const [newPass, setNewPass] = useState("");
  const [repeat_new_password, setRepeat_new_password] = useState("");
  const token = localStorage.getItem("token");
  const handleClick = () => {
    try {
      UserPassword.changePassword(oldPass, newPass, repeat_new_password, token ? token : "");
      console.log("ok change password");
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div className={styles.change__password__container}>
      <div className={styles.change__password}>
        <Paragraph size="medium">Сменить пароль</Paragraph>
        <Input
          value={oldPass}
          onChange={(e) => setOldPass(e.target.value)}
          type="text"
          label="Старый пароль"
        />
        <Input
          value={newPass}
          onChange={(e) => setNewPass(e.target.value)}
          type="text"
          label="Новый пароль"
        />
        <Input
          value={repeat_new_password}
          onChange={(e) => setRepeat_new_password(e.target.value)}
          type="text"
          label="Повторите пароль"
        />
        <Button onClick={handleClick}>Сохранить</Button>
      </div>
    </div>
  );
};

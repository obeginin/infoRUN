"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Input } from "@/src/ui/input/Input";
import { Header } from "@/src/Widgets/Header/Header";
import Image from "next/image";
import styles from "../forgotPassword.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import group from "@public/alphabet/group.svg";
import group_black from "@public/alphabet/group_black.svg";
import male from "@public/subjects/male1.svg";
import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useResetPasswordStore } from "@/src/store/resetPasswordStore";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
export default function Success() {
  const items = [
    { id: 1, label: "Восстановление пароля", link: "/forgot-password" },
    { id: 2, label: "Сброс пароля", link: "/forgot-password/success" },
  ];
  return (
    <>
      <Header />
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <BreadCrumb items={items} />
        <Suspense fallback={<div>Loading...</div>}>
          <FormContent />
        </Suspense>
      </div>
      <Footer />
    </>
  );
}

function FormContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [new_password, setNewPassword] = useState("");
  const [repeat_new_password, setRepeatNewPassword] = useState("");
  const { loading, success, error } = useResetPasswordStore();
  const resetPasswordWithToken = useResetPasswordStore(
    (state) => state.resetPasswordWithToken
  );
  const handleClick = () => {
    resetPasswordWithToken(token!, new_password, repeat_new_password);
  };

  return (
    <>
      <div className={styles.container}>
        <Image src={group} alt="" className={styles.group} />
        <div className={styles.form}>
          <ProfileContentContainer>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "10px" }}
            >
              <Paragraph>Восстановление пароля</Paragraph>
              <Input
                radius="16px"
                label="Новый пароль"
                value={new_password}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                error_text={error ? error : ""}
              />
              <Input
                radius="16px"
                label="Повторите пароль"
                value={repeat_new_password}
                onChange={(e) => setRepeatNewPassword(e.target.value)}
                required
                error_text={error ? error : ""}
              />
              {success && <p className={styles.success}>{success}</p>}
              <Button
                radius="16px"
                onClick={() => handleClick()}
                loading={loading}
                filled
                color="white"
                width="full"
              >
                Восстановить
              </Button>
            </div>
          </ProfileContentContainer>
        </div>
        <div className={styles.right}>
          <Image src={group_black} alt="" className={styles.group__black} />
          <Image src={male} alt="" className={styles.male} />
        </div>
      </div>
    </>
  );
}

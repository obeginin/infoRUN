"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Input } from "@/src/ui/input/Input";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import Image from "next/image";
import styles from "./forgotPassword.module.scss";
import group from "@public/alphabet/group.svg";
import group_black from "@public/alphabet/group_black.svg";
import male from "@public/subjects/male1.svg";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useResetPasswordStore } from "@/src/store/resetPasswordStore";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";

export default function ForgotPassword() {
  const items = [
    { id: 1, label: "Восстановление пароля", link: "/forgot-password" },
  ];
  const [email, setEmail] = useState("");
  const router = useRouter();
  const { resetPassword, loading, error, success } = useResetPasswordStore();
  return (
    <>
      <Header />
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
      <BreadCrumb items={items} />
        <div className={styles.container}>
          <Image src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <ProfileContentContainer>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >
                <Paragraph>Восстановление пароля</Paragraph>
                <Input
                  radius="16px"
                  label="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  error_text={error ? error : ""}
                />
                <Button
                  radius="16px"
                  onClick={() => resetPassword(email)}
                  loading={loading}
                  filled
                  color="white"
                  width="full"
                >
                  Восстановить
                </Button>
                <Button
                  radius="16px"
                  width="full"
                  outlined
                  onClick={() => router.push("/auth")}
                >
                  Назад
                </Button>
              </div>
            </ProfileContentContainer>
          </div>
          <div className={styles.right}>
            <Image src={group_black} alt="" className={styles.group__black} />
            <Image src={male} alt="" className={styles.male} />
          </div>
        </div>
      </div>
      <Footer />

      {success && (
        <div className={styles.success}>
          <p>{success}</p>
        </div>
      )}
    </>
  );
}

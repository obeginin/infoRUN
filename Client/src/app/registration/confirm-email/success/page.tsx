"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./success.module.scss";
import { useRouter } from "next/navigation";
import { Suspense, useEffect } from "react";
import AuthAPI from "@/src/API/registration";
import { useSearchParams } from "next/navigation";

export default function Success() {
  return (
    <>
      <div className="app">
        <Header />
        <div className={styles.container}>
          <ProfileContentContainer>
            <Suspense fallback={<div>Loading...</div>}>
              <Form />
            </Suspense>
          </ProfileContentContainer>
        </div>
      </div>
      <Footer />
    </>
  );
}

function Form() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  useEffect(() => {
    if (token) {
      AuthAPI.confirmToken(token);
    }
  });

  return (
    <div className={styles.content}>
      <Paragraph size="large" f_weight="extra_bold">
        Поздравляем! Ваш аккаунт зарегистрирован
      </Paragraph>
      <Button color="white" filled onClick={() => router.push("/auth")}>
        Войти
      </Button>
    </div>
  );
}

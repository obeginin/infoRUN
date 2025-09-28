"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./confirm-email.module.scss";
import { useEffect, useState } from "react";
import AuthAPI from "@/src/API/registration";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";

export default function ConfirmEmail() {
  const items = [
    { id: 1, label: "Регистрация", link: "/registration" },
    { id: 2, label: "Подтверждение", link: "/registration/confirm-email" },
  ];
  const [data, setData] = useState({
    email: "",
    login: "",
    password: "",
    tel: "",
  });
  const [timer, setTimer] = useState(300);

  useEffect(() => {
    const storedData = sessionStorage.getItem("registrationData");
    if (storedData) {
      setData(JSON.parse(storedData));
    }
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleClick = () => {
    const { email, login, password, tel } = data;
    AuthAPI.registration(email, login, password, tel);
    window.location.reload();
  };

  return (
    <>
      <div className="app">
        <Header />
        <BreadCrumb items={items} />
        <div className={styles.container}>
          <ProfileContentContainer>
            <div className={styles.content}>
              <Paragraph size="large" f_weight="extra_bold">
                Проверьте вашу почту {data.email}
              </Paragraph>

              <Paragraph>
                Мы отправили письмо с подтверждением на ваш email
              </Paragraph>

              <div style={{ maxWidth: "500px" }}>
                <Paragraph size="small">
                  Если письмо не пришло в течение 5 минут, проверьте папку Спам
                  или{" "}
                  {timer === 0 ? (
                    <Button onClick={() => handleClick()}>
                      отправьте письмо повторно
                    </Button>
                  ) : (
                    <span>
                      повторите отправку через {Math.floor(timer / 60)}:
                      {String(timer % 60).padStart(2, "0")}
                    </span>
                  )}
                </Paragraph>
              </div>
            </div>
          </ProfileContentContainer>
        </div>
      </div>
      <Footer />
    </>
  );
}

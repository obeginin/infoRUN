import { useEffect, useState } from "react";
import { Header } from "../Header/Header";
import { Footer } from "../Footer/Footer";
// import { useLocation } from "react-router-dom";
import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "../../ui/p/Paragraph";
import styles from "./RegistrationMailSend.module.scss";
import { Button } from "../../ui/buttonDeafault/Button";
// import AuthAPI from "../../API/registration";
export const RegistrationMailSend = () => {
  // const locate = useLocation();
  const [timer, setTimer] = useState(300);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // const handleClick = () => {
  //   const { email, login, password, tel } = locate.state;
  //   AuthAPI.registration(email, login, password, tel);
  //   window.location.reload();
  // };

  return (
    <>
      <div className="app">
        <Header />
        <div className={styles.container}>
          <ProfileContentContainer>
            <div className={styles.content}>
              <Paragraph size="large" f_weight="extra_bold">
                Проверьте вашу почту 
                {/* {locate.state.email} */}
              </Paragraph>

              <Paragraph>
                Мы отправили письмо с подтверждением на ваш email
              </Paragraph>

              <div style={{ maxWidth: "500px" }}>
                <Paragraph size="small">
                  Если письмо не пришло в течение 5 минут, проверьте папку спам или{" "}
                  {timer === 0 ? (
                    <Button>
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
};

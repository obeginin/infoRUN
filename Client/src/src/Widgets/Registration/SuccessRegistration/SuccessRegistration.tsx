import styles from "./SuccessRegistration.module.scss";
import { Paragraph } from "../../../ui/p/Paragraph";
import { Header } from "../../../Widgets/Header/Header";
import { Footer } from "../../../Widgets/Footer/Footer";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../../ui/buttonDeafault/Button";
// import { useNavigate } from "react-router-dom";
// import { useSearchParams } from "react-router-dom";
// import { useEffect } from "react";
// import AuthAPI from "../../../API/registration";
import { useRouter } from "next/navigation";
export const SuccessRegistration = () => {
  const router = useRouter();
  // const nav = useNavigate();
  // const [searchParams] = useSearchParams();
  // const token = searchParams.get("token");

  // useEffect(() => {
  //   if (token) {
  //     AuthAPI.confirmToken(token);
  //   }
  // });
  return (
    <>
      <div className="app">
        <Header />
        <div className={styles.container}>
          <ProfileContentContainer>
            <div className={styles.content}>
              <Paragraph size="large" f_weight="extra_bold">
                Поздравляем! Ваш аккаунт зарегистрирован
              </Paragraph>
              <Button filled onClick={() => router.push("/auth")}>
                Войти
              </Button>
            </div>
          </ProfileContentContainer>
        </div>
      </div>
      <Footer />
    </>
  );
};

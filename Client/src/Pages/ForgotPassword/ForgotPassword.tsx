import { Header } from "../../Widgets/Header/Header";
import styles from "./ForgotPassword.module.scss";
import { Footer } from "../../Widgets/Footer/Footer";
import group from "../../assets/alphabet/group.svg";
import group_black from "../../assets/alphabet/group_black.svg";
import male from "../../assets/subjects/male1.png";
import wave from "../../assets/wave.svg";
import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Input } from "../../ui/input/Input";
import { useState } from "react";
import { Button } from "../../ui/buttonDeafault/Button";
import { Paragraph } from "../../ui/p/Paragraph";
import { useNavigate } from "react-router-dom";
import { useResetPasswordStore } from "./store/store";
export const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const nav = useNavigate();
  const { resetPassword, loading, error, success } = useResetPasswordStore();
  return (
    <>
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <Header />
        <div className={styles.container}>
          <img src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <ProfileContentContainer>
              <Paragraph>Восстановление пароля</Paragraph>
              <Input
                label="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                error_text={error ? error : ""}
              />
              <Button
                onClick={() => resetPassword(email)}
                loading={loading}
                filled
                color="white"
                width="full"
              >
                Восстановить
              </Button>
              <Button onClick={() => nav("/auth")}>Назад</Button>
            </ProfileContentContainer>
          </div>
          <div className={styles.right}>
            <img src={group_black} alt="" className={styles.group__black} />
            <img src={male} alt="" className={styles.male} />
          </div>
        </div>
        <img src={wave} alt="" className={styles.wave} />
      </div>
      <Footer />

      {success && (
        <div className={styles.success}>
          <p>{success}</p>
        </div>
      )}
    </>
  );
};


import { Header } from "../../../Widgets/Header/Header";
import styles from "./ResetPassword.module.scss";
import { Footer } from "../../../Widgets/Footer/Footer";
import group from "../../../assets/alphabet/group.svg";
import wave from "../../../assets/wave.svg";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "../../../ui/p/Paragraph";
export const ResetPassword = () => {
  return (
    <>
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <Header />
        <div className={styles.container}>
          <img src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <ProfileContentContainer>
              <Paragraph>Восстановление пароля</Paragraph>
            </ProfileContentContainer>
          </div>
        </div>
        <img src={wave} alt="" className={styles.wave} />
      </div>
      <Footer />
    </>
  );
};

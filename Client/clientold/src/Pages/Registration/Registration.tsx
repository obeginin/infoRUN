import styles from "./Registration.module.scss";
import { RegistrationForm } from "../../Widgets/Registration/RegistrationForm";
import { Header } from "../../Widgets/Header/Header";
import group from "../../assets/alphabet/group.svg";
import group_black from "../../assets/alphabet/group_black.svg";
import male from "../../assets/subjects/male1.png";
import wave from "../../assets/wave.svg";
import { Footer } from "../../Widgets/Footer/Footer";
export const Registration = () => {
  return (
    <>
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <Header />
        <div className={styles.container}>
          <img src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <RegistrationForm />
          </div>
          <div className={styles.right}>
            <img src={group_black} alt="" className={styles.group__black} />
            <img src={male} alt="" className={styles.male} />
          </div>
        </div>
        <img src={wave} alt="" className={styles.wave} />
      </div>
      <Footer />
    </>
  );
};

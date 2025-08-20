import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { RegistrationForm } from "@/src/Widgets/Registration/RegistrationForm";
import Image from "next/image";
import styles from "./registration.module.scss"
import group from "@public/alphabet/group.svg";
import group_black from "@public/alphabet/group_black.svg";
import male from "@public/subjects/male1.svg";
import wave from "@public/assets/wave.svg";

export default function Registration() {
  return (
    <>
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <Header />
        <div className={styles.container}>
          <Image src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <RegistrationForm />
          </div>
          <div className={styles.right}>
            <Image src={group_black} alt="" className={styles.group__black} />
            <Image src={male} alt="male" className={styles.male} />
          </div>
        </div>
        <Image src={wave} alt="" className={styles.wave} />
      </div>
      <Footer />
    </>
  );
}

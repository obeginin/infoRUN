import { Header } from "@/src/Widgets/Header/Header";
import { AuthForm } from "@/src/Widgets/Auth/AuthForm";
import styles from "./auth.module.scss";
import { Footer } from "@/src/Widgets/Footer/Footer";
import group from "@public/alphabet/group.svg";
import group_black from "@public/alphabet/group_black.svg";
import male from "@public/subjects/male1.svg";
import wave from "@public/assets/wave.svg";
import Image from "next/image";

export default function Auth() {
  return (
    <div>
      <div className="app" style={{ position: "relative", overflow: "hidden" }}>
        <Header />
        <div className={styles.container}>
          <Image src={group} alt="" className={styles.group} />
          <div className={styles.form}>
            <AuthForm />
          </div>
          <div className={styles.right}>
            <Image src={group_black} alt="" className={styles.group__black} />
            <Image src={male} alt="" className={styles.male} />
          </div>
        </div>
        <Image src={wave} alt="" className={styles.wave} />
      </div>
      <Footer />
    </div>
  );
}

import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { Main } from "@/src/Widgets/Home/Main/Main";
import { Admin } from "@/src//Widgets/Home/Admin/Admin";
import { HomeCarousel } from "@/src//Widgets/Home/Carousel/HomeCarousel";
import { ForTeacher } from "@/src/Widgets/Home/ForTeacher/ForTeacher";
import { Subjects } from "@/src/Widgets/Home/Subjects/Subjects";
import { Examples } from "@/src/Widgets/Home/Examples/Examples";
import { News } from "@/src/Widgets/Home/News/News";
import group from "@public/alphabet/group.svg";
import styles from "./Home.module.scss";
import Image from "next/image";

export default function Home() {
  return (
    <div style={{ position: "relative" }}>
      <Image src={group} alt="" className={styles.group + " " + styles.first} />
      <Image
        src={group}
        alt=""
        className={styles.group + " " + styles.second}
      />
      <Image src={group} alt="" className={styles.group + " " + styles.third} />
      <Image
        src={group}
        alt=""
        className={styles.group + " " + styles.fourth}
      />
      <Header />
      <div className="app">
        <Main />
        <HomeCarousel />
        <ForTeacher />
        <Admin />
        <Subjects />
        <Examples />
        <News />
      </div>
      <Footer />
    </div>
  );
}

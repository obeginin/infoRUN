import { Footer } from "../../Widgets/Footer/Footer";
import { Header } from "../../Widgets/Header/Header";
import { Admin } from "../../Widgets/Home/Admin/Admin";
import { HomeCarousel } from "../../Widgets/Home/Carousel/HomeCarousel";
import { Examples } from "../../Widgets/Home/Examples/Examples";
import { ForTeacher } from "../../Widgets/Home/ForTeacher/ForTeacher";
import { Main } from "../../Widgets/Home/Main/Main";
import { News } from "../../Widgets/Home/News/News";
import { Subjects } from "../../Widgets/Home/Subjects/Subjects";
import group from "../../assets/alphabet/group.svg";
import styles from "./Home.module.scss"
export const Home = () => {
  return (
    <div style={{ position: "relative" }}>
      <img src={group} alt="" className={styles.group + " " + styles.first} />
      <img src={group} alt="" className={styles.group + " " + styles.second} />
      <img src={group} alt="" className={styles.group + " " + styles.third} />
      <img src={group} alt="" className={styles.group + " " + styles.fourth} />

      <div
        style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
      >
        {/* Основной контент с ограничением ширины */}
        <div
          className="app"
          style={{
            width: "100%",
            maxWidth: "1400px",
            margin: "0 auto",
            flex: "1 0 auto", // Растягивает контент, оставляя футер внизу
            padding: "0 20px", // Добавляем отступы по бокам
          }}
        >
          <Header />
          <Main />
          <HomeCarousel />
          <ForTeacher />
          <Admin />
          <Subjects />
          <Examples />
          <News />
        </div>

        {/* Футер на всю ширину */}
        <div style={{ width: "100%" }}>
          <Footer />
        </div>
      </div>
    </div>
  );
};

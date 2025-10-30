import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import { Main } from "@/Widgets/Home/Main/Main";
import { Admin } from "@//Widgets/Home/Admin/Admin";
import { HomeCarousel } from "@//Widgets/Home/Carousel/HomeCarousel";
import { ForTeacher } from "@/Widgets/Home/ForTeacher/ForTeacher";
import { Subjects } from "@/Widgets/Home/Subjects/Subjects";
import { Examples } from "@/Widgets/Home/Examples/Examples";
import { News } from "@/Widgets/Home/News/News";
import { BackgroundDefault } from "@/ui/backgroundPaper/backgeoundDefault";

export default function Home() {
  return (
    <div style={{ position: "relative" }}>
      <BackgroundDefault count={4} />
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

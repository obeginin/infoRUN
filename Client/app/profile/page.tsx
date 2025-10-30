import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import { ProfileCounterExam } from "@/Widgets/Profile/ProfileCounterExam/ProfileCounterExam";
import { ProfileGreatings } from "@/Widgets/Profile/ProfileGreatings/ProfileGreatings";
import { ProfileMotivation } from "@/Widgets/Profile/ProfileMotivation/ProfileMotivation";
import { ProfileProgress } from "@/Widgets/Profile/ProfileProgress/ProfileProgress";
import styles from "./profile.module.scss";
import { ProfileHistory } from "@/Widgets/Profile/ProfileHistory/ProfileHistory";
import { ProfileCreateTask } from "@/Widgets/Profile/ProfileCreateTask/ProfileCreateTask";
import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import { BackgroundDefault } from "@/ui/backgroundPaper/backgeoundDefault";
export default function Profile() {
  const items = [{ id: 1, label: "Личный кабинет", link: "/profile" }];
  return (
    <div style={{}}>
      <Header />
      <div className={"app"}>
        <BreadCrumb items={items} />
        <section>
          <div className={styles.profile__dashboard}>
            <BackgroundDefault count={1} />
            <ProfileGreatings />
            <div className={styles.profile__dashboard__content}>
              <ProfileCounterExam />
              <ProfileMotivation />
            </div>
            <ProfileCreateTask />
            <ProfileProgress />
            <ProfileHistory />
          </div>
        </section>
      </div>
      <Footer />
    </div>
  );
}

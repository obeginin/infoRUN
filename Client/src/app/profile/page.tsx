import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { ProfileCounterExam } from "@/src/Widgets/Profile/ProfileCounterExam/ProfileCounterExam";
import { ProfileGreatings } from "@/src/Widgets/Profile/ProfileGreatings/ProfileGreatings";
import { ProfileMotivation } from "@/src/Widgets/Profile/ProfileMotivation/ProfileMotivation";
import { ProfileProgress } from "@/src/Widgets/Profile/ProfileProgress/ProfileProgress";
import styles from "./profile.module.scss";
import group from "@public/alphabet/group.svg";
import { ProfileHistory } from "@/src/Widgets/Profile/ProfileHistory/ProfileHistory";
import Image from "next/image";
import { ProfileCreateTask } from "@/src/Widgets/Profile/ProfileCreateTask/ProfileCreateTask";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
export default function Profile() {
  const items = [{ id: 1, label: "Личный кабинет", link: "/profile" }];
  return (
    <div style={{}}>
      <Header />
      <div className={"app"}>
        <BreadCrumb items={items} />
        <section>
          <div className={styles.profile__dashboard}>
            <Image src={group} alt="" className={styles.group} />
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

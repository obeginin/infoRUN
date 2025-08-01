import { BreadCrumb } from "../../Features/BreadCrumb/BreadCrumb";
import { Footer } from "../../Widgets/Footer/Footer";
import { Header } from "../../Widgets/Header/Header";
import { ProfileCounterExam } from "../../Widgets/Profile/ProfileCounterExam/ProfileCounterExam";
import { ProfileGreatings } from "../../Widgets/Profile/ProfileGreatings/ProfileGreatings";
import { ProfileMotivation } from "../../Widgets/Profile/ProfileMotivation/ProfileMotivation";
import { ProfileProgress } from "../../Widgets/Profile/ProfileProgress/ProfileProgress";
import styles from "./Profile.module.scss";
import group from "../../assets/alphabet/group.svg"
import { ProfileHistory } from "../../Widgets/Profile/ProfileHistory/ProfileHistory";
export const Profile = () => {
  return (
    <>
      <div className={"app"}>
        <Header />
        <BreadCrumb currentPage="Личный кабинет" />
        <section>
          <div className={styles.profile__dashboard}>
            <img src={group} alt="" className={styles.group} />
            <ProfileGreatings />
            <div className={styles.profile__dashboard__content}>
              <ProfileCounterExam />
              <ProfileMotivation />
            </div>
            <ProfileProgress />
            <ProfileHistory />
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
};

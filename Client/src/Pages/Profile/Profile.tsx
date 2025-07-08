import { Header } from "../../Widgets/Header/Header";
import { ProfileCounterExam } from "../../Widgets/ProfileCounterExam/ProfileCounterExam";
import { ProfileGreatings } from "../../Widgets/ProfileGreatings/ProfileGreatings";
import { ProfileMotivation } from "../../Widgets/ProfileMotivation/ProfileMotivation";
import styles from "./Profile.module.scss";
export const Profile = () => {
  return (
    <div className={"app"}>
      <Header />
      <div className={styles.profile__dashboard}>
        <ProfileGreatings />
        <div className={styles.profile__dashboard__content}>
          <ProfileCounterExam />
          <ProfileMotivation />
        </div>
      </div>
    </div>
  );
};

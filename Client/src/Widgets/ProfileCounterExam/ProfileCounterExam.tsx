import { ProfileContentContainer } from "../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../ui/buttonDeafault/Button";
import { Paragraph } from "../../ui/p/Paragraph";
import styles from "./ProfileCounterExam.module.scss";
export const ProfileCounterExam = () => {
  return (
    <>
      <ProfileContentContainer>
        <div className={styles.counter__exam}>
          <Button>Расписание</Button>
          <Paragraph>Информатика через 365 дней</Paragraph>
        </div>
      </ProfileContentContainer>
    </>
  );
};

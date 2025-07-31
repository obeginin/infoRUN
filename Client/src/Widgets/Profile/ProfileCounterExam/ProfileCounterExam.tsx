import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./ProfileCounterExam.module.scss";
export const ProfileCounterExam = () => {
  return (
    <>
      <ProfileContentContainer color="secondary">
        <div className={styles.counter__exam}>
          <Button style={{
            backgroundColor: "var(--secondary)",
            color: "var(--bg)",
            border: "1px solid var(--bg)"
          }}>
            Расписание
          </Button>
          <Paragraph color="white">Информатика через 365 дней</Paragraph>
        </div>
      </ProfileContentContainer>
    </>
  );
};

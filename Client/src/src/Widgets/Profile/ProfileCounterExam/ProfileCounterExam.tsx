import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./ProfileCounterExam.module.scss";
export const ProfileCounterExam = () => {
  return (
    <>
      <ProfileContentContainer borderColor="secondary" color="secondary">
        <div className={styles.counter__exam}>
          <Button border="white" color="white" outlined>
            Расписание
          </Button>
          <Paragraph color="white">Информатика через 365 дней</Paragraph>
        </div>
      </ProfileContentContainer>
    </>
  );
};

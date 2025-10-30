import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "@/ui/p/Paragraph";
import styles from "./ProfileCounterExam.module.scss";
import { TextContainer } from "@/ui/textContainer/TextContainer";
export const ProfileCounterExam = () => {
  return (
    <>
      <ProfileContentContainer borderColor="secondary" color="secondary">
        <div className={styles.counter__exam}>
          <TextContainer borderColor="bg" color="white">
            Расписание
          </TextContainer>
          <Paragraph color="white">Информатика через 365 дней</Paragraph>
        </div>
      </ProfileContentContainer>
    </>
  );
};

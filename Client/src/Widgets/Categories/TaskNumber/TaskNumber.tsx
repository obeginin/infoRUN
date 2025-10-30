import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./TaskNumber.module.scss";
import { Paragraph } from "@/ui/p/Paragraph";
interface TaskNumberProps {
  task: string[];
}

export const TaskNumber = ({ task }: TaskNumberProps) => {
  return (
    <div>
      <ProfileContentContainer>
        <div className={styles.content}>
          {task.map((item) => (
            <div key={item} className={styles.card}>
              <Paragraph>{item}</Paragraph>
            </div>
          ))}
        </div>
      </ProfileContentContainer>
    </div>
  );
};

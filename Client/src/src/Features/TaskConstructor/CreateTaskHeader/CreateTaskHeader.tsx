import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./CreateTaskHeader.module.scss";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { ProfileContentContainer } from "../../ProfileContentContainer/ProfileContentContainer";

interface CreateTaskHeaderProps {
  onAddElement: (type: "text" | "image") => void;
  subject: string;
  task: string;
}

export const CreateTaskHeader = ({
  onAddElement,
  subject,
  task,
}: CreateTaskHeaderProps) => {
  return (
    <ProfileContentContainer>
      <div className={styles.header}>
        <Paragraph>
          {subject}: {task}
        </Paragraph>

        <div className={styles.buttons}>
          <Paragraph>Добавить:</Paragraph>

          <Button filled color="white" onClick={() => onAddElement("text")}>
            Текст
          </Button>
          <Button filled color="white" onClick={() => onAddElement("image")}>
            Изображение
          </Button>
        </div>
      </div>
    </ProfileContentContainer>
  );
};

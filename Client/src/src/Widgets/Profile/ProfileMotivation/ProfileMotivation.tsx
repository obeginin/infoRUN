import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./ProfileMotivation.module.scss";
import blackboard from "@public/assets/blackboard.svg";
import { Button } from "@/src/ui/buttonDeafault/Button";
import Image from "next/image";
export const ProfileMotivation = () => {
  return (
    <>
      <ProfileContentContainer borderColor="purple" color="purple">
        <div className={styles.motivation__exam}>
          <Button border="white" color="white" outlined>
            Цитата дня
          </Button>
          <Image
            src={blackboard}
            alt=""
            className={styles.motivation__exam__img}
          />
          <Paragraph color="white">
            Это всегда выглядит невозможным, пока не сделаешь.
          </Paragraph>
        </div>
      </ProfileContentContainer>
    </>
  );
};

"use client";

import { useUserStore } from "@/src/store/userStore";
import styles from "./ProfileCreateTask.module.scss";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import Link from "next/link";
import { TextContainer } from "@/src/ui/textContainer/TextContainer";

export const ProfileCreateTask = () => {
  const user = useUserStore((state) => state.user);
  return (
    <>
      {user?.RoleName !== "Ученик" && (
        <ProfileContentContainer>
          <div className={styles.container}>
            <TextContainer >Создать задачу</TextContainer>
            <Paragraph size="base">
              Создавайте задачи для своих учеников в нашем конструкторе заданий!
            </Paragraph>
            <Link href="/profile/create-task">
              <Button width="auto" color="white" border="white" filled>
                Перейти в конструктор
              </Button>
            </Link>
          </div>
        </ProfileContentContainer>
      )}
    </>
  );
};

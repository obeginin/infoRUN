"use client";

import styles from "./ProfileHistory.module.scss";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { useEffect, useState } from "react";
import AdminAPI from "@/src/API/admin";
import { useUserStore } from "@/src/store/userStore";
import type { ILog } from "@/src/interface/logs.interface";
import { Task } from "@/src/ui/taskContainer/Task";
import { format } from "date-fns";
import { ru } from "date-fns/locale";
import { TextContainer } from "@/src/ui/textContainer/TextContainer";

export const ProfileHistory = () => {
  const [data, setData] = useState<ILog[]>([]);
  const token = localStorage.getItem("token");
  const user = useUserStore((state) => state.user);
  useEffect(() => {
    AdminAPI.getStudentLogs(token as string, user?.ID as number)
      .then((res) => setData(res))
      .catch((error) => console.error(error));
  }, [user, token]);

  return (
    <>
      <ProfileContentContainer>
        <div className={styles.container}>
          <TextContainer>
            История действий
          </TextContainer>
          <div className={styles.content}>
            {data.slice(0, 10).map((item) => (
              <div key={item.LogID} className={styles.card}>
                <Task>
                  <Paragraph>
                    #{item.LogID} <span>{item.DescriptionEvent}</span>
                  </Paragraph>
                  <Paragraph size="small">
                    {format(new Date(item.EventTime), "dd.MM.yyyy HH:mm", {
                      locale: ru,
                    })}
                  </Paragraph>
                </Task>
              </div>
            ))}
          </div>
        </div>
      </ProfileContentContainer>
    </>
  );
};

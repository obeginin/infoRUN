import styles from "./ProfileHistory.module.scss";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Paragraph } from "../../../ui/p/Paragraph";
import { useEffect, useState } from "react";
import AdminAPI from "../../../API/admin";
import { useUserStore } from "../../../store/userStore";
import type { ILog } from "../../../interface/logs.interface";
import { Task } from "../../../ui/taskContainer/Task";
import { Button } from "../../../ui/buttonDeafault/Button";
import { format } from "date-fns";
import { ru } from "date-fns/locale";

export const ProfileHistory = () => {
  const [data, setData] = useState<ILog[]>([]);
  const token = localStorage.getItem("token");
  const user = useUserStore((state) => state.user);
  useEffect(() => {
    AdminAPI.getStudentLogs(token as string, user?.ID as number)
      .then((res) => setData(res))
      .catch((error) => console.log(error));
  }, [user, token]);

  return (
    <>
      <ProfileContentContainer>
        <div className={styles.container}>
          <Button disabled filled color="white">
            История действий
          </Button>
          <div className={styles.content}>
            {data.slice(0, 10).map((item) => (
              <div key={item.LogID} className={styles.card}>
                <Task>
                  <Paragraph>#{item.LogID} <span>{item.DescriptionEvent}</span></Paragraph>
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

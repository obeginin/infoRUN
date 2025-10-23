"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./AdminLogsCurrentUser.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { useAdminStore } from "@/src/store/admin/adminStore";
import { TextContainer } from "@/src/ui/textContainer/TextContainer";
import { useEffect, useState } from "react";
import AdminAPI from "@/src/API/admin";
import { ILog } from "@/src/interface/logs.interface";
import { Task } from "@/src/ui/taskContainer/Task";
import { format } from "date-fns";
import { ru } from "date-fns/locale";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";

export const AdminLogsCurrentUser = () => {
  const { currentUser } = useAdminStore();
  const [logsData, setLogsData] = useState<ILog[]>([]);
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("token") || "";
  useEffect(() => {
    if (currentUser) {
      setLoading(true);
      AdminAPI.getUserLogs(token, currentUser.ID)
        .then((response) => {
          setLogsData(response);
          setLoading(false);
        })
        .catch((error) => {
          console.log(error);
          setLoading(false);
        });
    }
  }, [currentUser]);

  return (
    <ProfileContentContainer>
      <div className={styles.container}>
        <TextContainer>
          Логи пользователя
        </TextContainer>
        <div className={styles.content_container}>
          <div className={styles.content}>
            <Paragraph size="tiny">Логи: {currentUser?.Login}</Paragraph>
            <Paragraph size="tiny">Email: {currentUser?.Email}</Paragraph>
          </div>
          <div className={styles.content}>
            <Paragraph size="tiny">Имя: {currentUser?.First_Name}</Paragraph>
            <Paragraph size="tiny">Фамилия: {currentUser?.Last_Name}</Paragraph>
          </div>
          <div className={styles.content}>
            <Paragraph size="tiny">Телефон: {currentUser?.Phone}</Paragraph>
            <Paragraph size="tiny">Пол: {currentUser?.Sex}</Paragraph>
          </div>
          <div className={styles.content}>
            <Paragraph size="tiny">Роль: {currentUser?.RoleName}</Paragraph>
            <Paragraph size="tiny">
              Комментарии: {currentUser?.Comment}
            </Paragraph>
          </div>
          <div className={styles.content}>
            <Paragraph size="tiny">
              Активность: {currentUser?.IsActive}
            </Paragraph>
            <Paragraph size="tiny">Удален: {currentUser?.IsDeleted}</Paragraph>
          </div>
        </div>

        {loading ? (
          <div className={styles.loading}>
            <Spinner />
          </div>
        ) : (
          <div className={styles.card_container}>
            {logsData.length > 0 ? (
              logsData.map((item) => (
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
              ))
            ) : (
              <Paragraph>Нет логов</Paragraph>
            )}
          </div>
        )}
      </div>
    </ProfileContentContainer>
  );
};

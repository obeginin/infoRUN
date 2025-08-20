import TasksAPI from "../../../API/tasks";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./ProfileProgress.module.scss";
import { useState, useEffect } from "react";
import { useUserStore } from "../../../store/userStore";
import type { IProfileProgress } from "./ProfileProgress.interface";
import { CircualProgress } from "../../../Features/CircualProgress/CircualProgress";
import { useNavigate } from "react-router-dom";
import { Task } from "../../../ui/taskContainer/Task";

export const ProfileProgress = () => {
  const user = useUserStore((state) => state.user);
  const [progress, setProgress] = useState<IProfileProgress[]>([]);
  const [complitedTasks, setComplitedTasks] = useState<number>(0);
  const nav = useNavigate();
  const token = localStorage.getItem("token");
  useEffect(() => {
    if (!progress.length) return;
    setComplitedTasks(
      progress.filter((item) => item.CompletionStatus === "Выполнено").length
    );
  }, [progress]);

  useEffect(() => {
    if (!user) return;
    TasksAPI.getAllTasks(user.ID, token ? token : "")
      .then((response) => setProgress(response))
      .catch((error) => console.log(error));
  }, [user, token]);

  return (
    <>
      <ProfileContentContainer>
        <Button
          disabled
          style={{
            border: "1px solid var(--primary)",
            backgroundColor: "transparent",
          }}
        >
          Прогресс
        </Button>
        <div className={styles.progress__item}>
          <CircualProgress completed={complitedTasks} total={progress.length} />
          <Paragraph>Информатика</Paragraph>
          <Paragraph color="primary">
            Выполнено {complitedTasks} из {progress.length} заданий
          </Paragraph>
        </div>

        <div className={styles.progress__item}>
          {progress.length > 0 ? (
            progress.slice(0, 5).map((item) => (
              <Task key={item.StudentTaskID}>
                <Paragraph>
                  Задание {item.SubTaskID}: {item.TaskTitle} {item.VariantName}
                </Paragraph>
              </Task>
            ))
          ) : (
            <Task>
              <Paragraph>Заданий нет</Paragraph>
            </Task>
          )}

          <div
            className={styles.arrow}
            onClick={() =>
              nav("/profile/all-tasks", { state: { tasks: progress } })
            }
          >
            <i className={"pi pi-angle-down"}></i>
          </div>
        </div>
      </ProfileContentContainer>
    </>
  );
};

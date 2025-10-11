"use client";

import { Task } from "@/src/ui/taskContainer/Task";
import styles from "./CurrentMyTask.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { format } from "date-fns";
import { useEffect, useRef, useState } from "react";
import { useMyTaskStore } from "@/src/store/task/myTaskStore";
import { useUserStore } from "@/src/store/user/userStore";
import { Toast } from "primereact/toast";
import "primereact/resources/themes/lara-light-cyan/theme.css";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import Link from "next/link";
export const CurrentMyTask = () => {
  const ref = useRef<Toast>(null);
  const [visibleImage, setVisibleImage] = useState<number[]>([]);
  const { getTask, task, deleteSubtask, error, clearError, setCurrentTask } =
    useMyTaskStore();
  const user = useUserStore((state) => state.user);

  useEffect(() => {
    getTask(user?.Login || "");
  }, []);
  const handleClick = (task_id: number) => {
    deleteSubtask(task_id);
  };

  useEffect(() => {
    if (error) {
      ref.current?.show({
        severity: "error",
        summary: "Error",
        detail: error,
        life: 3000,
      });
      clearError();
    }
  }, [error]);
  return (
    <div className={styles.container}>
      <Toast ref={ref} position="bottom-left" />
      {task ? (
        task
          .sort((a, b) => b.SubTaskID - a.SubTaskID)
          .map((item, index) => (
            <Task key={item.SubTaskID}>
              <div className={styles.task__container}>
                <div className={styles.date__container}>
                  <Paragraph>
                    {item.TaskTitle}: {item.VariantName} {item.SubTaskID}
                  </Paragraph>
                  <i className={styles.date}>
                    {format(new Date(item.UploadDate), "dd.MM.yyyy. HH:mm")}
                  </i>
                </div>
                <div className={styles.icon__container}>
                  <Link
                    href={`/profile/subjects/${item.SubjectName}/${item.SubTaskID}`}
                  >
                    <i
                      onClick={() => setCurrentTask(item)}
                      className="pi pi-pencil"
                    ></i>
                  </Link>
                  <i
                    className="pi pi-trash"
                    onClick={() => handleClick(item.SubTaskID)}
                  ></i>
                  <i
                    onClick={() =>
                      setVisibleImage(
                        visibleImage.includes(index)
                          ? visibleImage.filter((i) => i !== index)
                          : [...visibleImage, index]
                      )
                    }
                    className={`pi pi-angle-down ${styles.arrow}`}
                  ></i>
                </div>
              </div>

              <div
                className={`${styles.collapsible} ${
                  visibleImage.includes(index) ? styles.open : ""
                }`}
              >
                <div className={styles.task__content}>
                  {item.Blocks.map((item, index) => (
                    <div key={index}>
                      {item.type === "image" ? (
                        <img
                          src={process.env.NEXT_PUBLIC_BASE_URL + item.content}
                          alt={item.content}
                        />
                      ) : (
                        <Paragraph>{item.content}</Paragraph>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </Task>
          ))
      ) : (
        <Spinner />
      )}
    </div>
  );
};

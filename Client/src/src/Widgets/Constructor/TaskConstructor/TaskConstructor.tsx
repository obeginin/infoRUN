"use client";

import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { CreateTaskHeader } from "@/src/Features/TaskConstructor/CreateTaskHeader/CreateTaskHeader";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { TaskElement } from "@/src/Features/TaskConstructor/TaskElement/TaskElement";
import styles from "./TaskConstructor.module.scss";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { useConstructorStore } from "@/src/store/useConstructorStore";
import { useEffect, useRef, useState } from "react";
import { Toast, ToastMessage } from "primereact/toast";
import "primereact/resources/themes/lara-light-cyan/theme.css";

export const TaskConstructor = () => {
  const {
    elements,
    addElement,
    updateElement,
    removeElement,
    moveElement,
    handleSave,
    loading,
    success,
    error,
    setError,
  } = useConstructorStore();
  const ref = useRef<Toast>(null);
  const constructorStorage = localStorage.getItem("constructor-storage");
  const [subject, setSubject] = useState("");
  const [task, setTask] = useState("");

  useEffect(() => {
    const constructorStorage = localStorage.getItem("constructor-storage");
    if (!constructorStorage) return;

    const data = JSON.parse(constructorStorage || "");
    if (!data.state.subject || !data.state.task) {
      setError("Заполните все поля");
    } else {
      setSubject(data.state.subject.Name);
      setTask(data.state.task.TaskTitle);
    }
  }, []);

  const showToastMessage = (
    message: string,
    severity: ToastMessage["severity"]
  ) => {
    ref.current?.show({
      severity: severity,
      summary: message,
      life: 3000,
    });
  };

  useEffect(() => {
    if (error) {
      showToastMessage(error, "error");
    }
    if (success) {
      showToastMessage(success, "success");
    }
  }, [error, success]);

  return (
    <div className={styles.taskConstructor}>
      <Toast ref={ref} position="bottom-left" />
      <CreateTaskHeader
        onAddElement={addElement}
        subject={subject}
        task={task}
      />
      <ProfileContentContainer>
        <div className={styles.container}>
          {elements.map((element) => (
            <TaskElement
              key={element.id}
              element={element}
              onUpdate={updateElement}
              onRemove={removeElement}
              onMove={moveElement}
            />
          ))}

          {elements.length > 0 && (
            <Button
              loading={loading}
              color="white"
              filled
              onClick={() => handleSave()}
            >
              Сохранить
            </Button>
          )}

          {elements.length === 0 && (
            <div>
              <Paragraph>Добавьте первый элемент задачи</Paragraph>
            </div>
          )}
        </div>
      </ProfileContentContainer>
    </div>
  );
};

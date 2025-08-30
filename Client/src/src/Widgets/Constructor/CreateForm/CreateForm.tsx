"use client";

import { useConstructorStore } from "@/src/store/useConstructorStore";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import { TextArea } from "@/src/ui/textArea/TextArea";
import { useEffect, useState } from "react";
import styles from "./CreateForm.module.scss";
import { InputImage } from "@/src/ui/InputImage/InputImage";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Button } from "@/src/ui/buttonDeafault/Button";
import Stepper, { Step } from "@/src/shared/Stepper/Stepper";

export const CreateForm = () => {
  const [step1Valid, setStep1Valid] = useState(false);
  const {
    subjects,
    getSubjects,
    setSubject,
    getTaskNumber,
    subject,
    loading,
    tasks,
    task,
    setTask,
    getVarinants,
    variants,
    variant,
    setVariant,
    answer,
    setAnswer,
    setImage,
    initialAnswerFiles,
    initialAnswerFilesAdd,
    initialAnswerFilesRemove,
    initialDescriptionFiles,
    initialDescriptionFilesAdd,
    initialDescriptionFilesRemove,
    updateInitialAnswerFile,
    updateInitialDescriptionFile,
  } = useConstructorStore();

  useEffect(() => {
    getSubjects();
    getVarinants();
  }, []);

  useEffect(() => {
    if (subject) {
      getTaskNumber(subject.ID);
    }
  }, [subject]);

  useEffect(() => {
    if (subject && task && variant) {
      setStep1Valid(true);
    }
  }, [task, variant, subject]);

  return (
    <section>
      {loading &&
      (!subjects || subjects.length === 0) &&
      (!tasks || tasks.length === 0) ? (
        <Spinner />
      ) : (
        <Stepper
          linkEndButton="/profile/create-task/constructor"
          endButtonChildren="Перейти в конструктор"
          initialStep={1}
          disabledNextButton={!step1Valid}
        >
          <Step>
            <form className={styles.form}>
              <div className={styles.select__container}>
                <i className={`pi pi-chevron-down ${styles.icon}`} />
                <select
                  className={styles.select}
                  value={subject?.Name || ""}
                  onChange={(e) => {
                    const selectedSubject = subjects?.find(
                      (s) => s.Name === e.target.value
                    );
                    if (selectedSubject) setSubject(selectedSubject);
                  }}
                >
                  <option value="">Выберите предмет</option>
                  {subjects?.map((subject) => (
                    <option key={subject.ID} value={subject.Name}>
                      {subject.Name}
                    </option>
                  ))}
                </select>
              </div>
              <div className={styles.select__container}>
                <i className={`pi pi-chevron-down ${styles.icon}`} />
                <select
                  className={styles.select}
                  value={task?.TaskTitle || ""}
                  onChange={(e) => {
                    const selectedTask = tasks?.find(
                      (t) => t.TaskTitle === e.target.value
                    );
                    if (selectedTask) setTask(selectedTask);
                  }}
                >
                  <option value="">Выберите категорию</option>
                  {tasks?.map((task) => (
                    <option key={task.TaskID} value={task.TaskTitle}>
                      {task.TaskTitle}
                    </option>
                  ))}
                </select>
              </div>
              <div className={styles.select__container}>
                <i className={`pi pi-chevron-down ${styles.icon}`} />
                <select
                  className={styles.select}
                  value={variant?.VariantName || ""}
                  onChange={(e) => {
                    const selectedVariant = variants?.find(
                      (v) => v.VariantName === e.target.value
                    );
                    if (selectedVariant) setVariant(selectedVariant);
                  }}
                >
                  <option value="">Выберите вариант</option>
                  {variants?.map((variant) => (
                    <option key={variant.VariantID} value={variant.VariantName}>
                      {variant.VariantName}
                    </option>
                  ))}
                </select>
              </div>
              <TextArea
                onChange={(e) => setAnswer(e.target.value)}
                value={answer}
                placeholder="Введите ответ"
              />
            </form>
          </Step>
          <Step>
            <div className={styles.container}>
              <Paragraph size="small">Изображение с решением</Paragraph>
              {initialAnswerFiles.map((file) => (
                <div key={file.id}>
                  <i
                    className="pi pi-trash"
                    onClick={() => initialAnswerFilesRemove(file.id)}
                  />
                  <InputImage
                    key={file.id}
                    file={file.file}
                    onChange={(e) => updateInitialAnswerFile(file.id, e)}
                  />
                </div>
              ))}
              <Button
                onClick={() => initialAnswerFilesAdd()}
                size="small"
                color="white"
                filled
              >
                Добавить изображение
              </Button>
            </div>
          </Step>
          <Step>
            <div className={styles.container}>
              <Paragraph size="small">
                Дополнительная информация к задаче
              </Paragraph>
              {initialDescriptionFiles.map((file) => (
                <div key={file.id}>
                  <i
                    className="pi pi-trash"
                    onClick={() => initialDescriptionFilesRemove(file.id)}
                  />
                  <InputImage
                    key={file.id}
                    file={file.file}
                    onChange={(e) => updateInitialDescriptionFile(file.id, e)}
                  />
                </div>
              ))}
              <Button
                onClick={() => initialDescriptionFilesAdd()}
                size="small"
                color="white"
                filled
              >
                Добавить файл
              </Button>
            </div>
          </Step>
        </Stepper>
      )}
    </section>
  );
};

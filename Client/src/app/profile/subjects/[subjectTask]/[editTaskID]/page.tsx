"use client";

import { useState, useCallback } from "react";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { IBlock } from "@/src/interface/subtask.interface";
import { useMyTaskStore } from "@/src/store/myTaskStore";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./editTaskID.module.scss";
import { TextArea } from "@/src/ui/textArea/TextArea";
import { InputImage } from "@/src/ui/InputImage/InputImage";
import { Button } from "@/src/ui/buttonDeafault/Button";
import type { EditBlock } from "@/src/store/myTaskStore"; // импортируй тип

export default function EditTask() {
  const [filesById, setFilesById] = useState<Record<string, File | null>>({});
  const [textsById, setTextsById] = useState<Record<string, string>>({});

  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Предметы", link: "/profile/subjects" },
  ];

  const { currentTask, handleEditTask, loading, error, success } =
    useMyTaskStore();

  const onSave = useCallback(async () => {
    if (!currentTask) return;

    const blocks: EditBlock[] = currentTask.Blocks.map(
      (b: IBlock, index: number) => {
        const key = String(index);

        if (b.type === "text") {
          return {
            type: "text",
            content: textsById[key] ?? b.content ?? "",
          };
        }

        const f = filesById[key];
        if (f) {
          return {
            type: "image",
            file: f,
            content: f.name || "",
          };
        }
        return {
          type: "image",
          content: b.content || "",
        };
      }
    );
    // console.log(
    //   currentTask.SubTaskID,
    //   currentTask.SubTaskNumber,
    //   currentTask.TaskID,
    //   currentTask.VariantID
    // );
    await handleEditTask({
      subtask_id: currentTask.SubTaskID,
      subtask_number: currentTask.SubTaskNumber,
      task_id: currentTask.TaskID,
      variant_id: currentTask.VariantID,
      answer: null,
      blocks,
    });
  }, [currentTask, filesById, textsById, handleEditTask]);

  return (
    <>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
      </div>

      <ProfileContentContainer>
        <div className={styles.container}>
          {currentTask &&
            currentTask.Blocks.map((item: IBlock, index: number) => {
              const key = String(index);
              return (
                <div key={`${item.type}-${index}`}>
                  {item.type === "image" ? (
                    <ProfileContentContainer>
                      <div className={styles.imageContainer}>
                        <InputImage
                          url={`${process.env.NEXT_PUBLIC_BASE_URL}${item.content}`}
                          file={filesById[key] ?? null}
                          onChange={(f) =>
                            setFilesById((prev) => ({ ...prev, [key]: f }))
                          }
                        />
                      </div>
                    </ProfileContentContainer>
                  ) : (
                    <ProfileContentContainer>
                      <TextArea
                        value={textsById[key] ?? (item.content || "")}
                        onChange={(e) =>
                          setTextsById((prev) => ({
                            ...prev,
                            [key]: e.target.value,
                          }))
                        }
                      />
                    </ProfileContentContainer>
                  )}
                </div>
              );
            })}

          <div className={styles.actions}>
            <Button color="white" filled disabled={loading} onClick={onSave}>
              {loading ? "Сохранение..." : "Сохранить"}
            </Button>
            {error && <div className={styles.error}>{error}</div>}
            {success && <div className={styles.success}>{success}</div>}
          </div>
        </div>
      </ProfileContentContainer>

      <Footer />
    </>
  );
}

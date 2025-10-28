"use client";

import { InputImage } from "@/src/ui/InputImage/InputImage";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { TextArea } from "@/src/ui/textArea/TextArea";
import styles from "./TaskElement.module.scss";

type TaskElementType = "text" | "image";
interface TaskElement {
  id: string;
  type: TaskElementType;
  content?: string;
  file?: File | null;
}
interface PropTaskElement {
  element: TaskElement;
  onUpdate: (id: string, updates: Partial<TaskElement>) => void;
  onRemove: (id: string) => void;
  onMove: (id: string, direction: "up" | "down") => void;
}

export const TaskElement = ({
  element,
  onUpdate,
  onRemove,
  onMove,
}: PropTaskElement) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <span>
          {element.type === "text" ? (
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <i className="pi pi-pen-to-square"></i>
              <Paragraph size="tiny">Текстовое поле</Paragraph>
            </div>
          ) : (
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <i className="pi pi-image"></i>
              <Paragraph size="tiny">Изображение</Paragraph>
            </div>
          )}
        </span>
        <div className={styles.arrows}>
          <i
            className="pi pi-chevron-down"
            onClick={() => onMove(element.id, "down")}
          ></i>
          <i
            className="pi pi-chevron-up"
            onClick={() => onMove(element.id, "up")}
          ></i>
        </div>
        <div onClick={() => onRemove(element.id)} className={styles.delete}>
          <i className="pi pi-trash"></i>
        </div>
      </div>
      {element.type === "text" ? (
        <TextArea
          value={element.content || ""}
          onChange={(e) => onUpdate(element.id, { content: e.target.value })}
        />
      ) : (
        <InputImage
          file={element.file}
          onChange={(file) => onUpdate(element.id, { file })}
        />
      )}
    </div>
  );
};

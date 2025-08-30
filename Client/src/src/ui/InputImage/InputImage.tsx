import { useState, useRef, useCallback } from "react";
import styles from "./InputImage.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";

interface InputImageProps {
  file: File | null | undefined;
  onChange: (file: File | null) => void;
}

export const InputImage = ({ file, onChange }: InputImageProps) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(
    (selectedFile: File) => {
      if (selectedFile) {
        onChange(selectedFile);
        setFileName(selectedFile.name);

        // Создаем превью только для изображений
        if (selectedFile.type.startsWith("image/")) {
          const reader = new FileReader();
          reader.onload = (e) => setPreview(e.target?.result as string);
          reader.readAsDataURL(selectedFile);
        } else {
          setPreview(null); // Сбрасываем превью для не-изображений
        }
      }
    },
    [onChange]
  );

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      handleFile(selectedFile);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFile(droppedFile);
    }
  };

  const handleRemove = () => {
    onChange(null);
    setPreview(null);
    setFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  // Функция для получения иконки файла по расширению
  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    
    switch (extension) {
      case 'pdf':
        return 'pi pi-file-pdf';
      case 'doc':
      case 'docx':
        return 'pi pi-file-word';
      case 'xls':
      case 'xlsx':
        return 'pi pi-file-excel';
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return 'pi pi-image';
      default:
        return 'pi pi-file';
    }
  };

  return (
    <div
      className={`${styles.input__container} ${
        isDragging ? styles.dragging : ""
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      {preview ? (
        <div className={styles.preview}>
          <img src={preview} alt="Preview" className={styles.preview__image} />
          <i className="pi pi-times" onClick={handleRemove}></i>
        </div>
      ) : fileName ? (
        <div className={styles.file__info}>
          <i className={getFileIcon(fileName)}></i>
          <span className={styles.file__name}>{fileName}</span>
          <i 
            className="pi pi-times" 
            onClick={(e) => {
              e.stopPropagation();
              handleRemove();
            }}
          ></i>
        </div>
      ) : (
        <>
          <label className={styles.label}>
            <input
              ref={fileInputRef}
              type="file"
              className={styles.input}
              onChange={handleFileChange}
              accept="pdf,doc,docx,xls,xlsx,jpg,jpeg,png"
            />
            <span>{isDragging ? "Отпустите файл" : "Загрузить файл"}</span>
          </label>
          <Paragraph size="tiny" color="gray">
            PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG до 10MB
          </Paragraph>
          <Paragraph size="tiny" color="gray">
            Или перетащите файл сюда
          </Paragraph>
        </>
      )}
    </div>
  );
};
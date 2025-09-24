"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import styles from "./InputImage.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";

interface InputImageProps {
  file?: File | null;
  url?: string | null; // для режима редактирования
  onChange: (file: File | null) => void;
}

const isImageExt = (ext?: string) =>
  !!ext &&
  ["jpg", "jpeg", "png", "gif", "webp", "avif", "bmp", "svg"].includes(ext);

const getExt = (name?: string) => name?.split(".").pop()?.toLowerCase();

const getFileIcon = (filename: string) => {
  const ext = getExt(filename);
  switch (ext) {
    case "pdf":
      return "pi pi-file-pdf";
    case "doc":
    case "docx":
      return "pi pi-file-word";
    case "xls":
    case "xlsx":
      return "pi pi-file-excel";
    case "jpg":
    case "jpeg":
    case "png":
    case "gif":
    case "webp":
    case "avif":
    case "bmp":
    case "svg":
      return "pi pi-image";
    default:
      return "pi pi-file";
  }
};

export const InputImage = ({ file, url, onChange }: InputImageProps) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // синхронизация пропсов -> локальный стейт
  useEffect(() => {
    // 1) приоритет File
    if (typeof File !== "undefined" && file instanceof File) {
      setFileName(file.name);
      if (file.type?.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => setPreview((e.target?.result as string) || null);
        reader.readAsDataURL(file);
      } else {
        setPreview(null);
      }
      return;
    }
    // 2) URL
    if (url) {
      try {
        const u = new URL(
          url,
          typeof window !== "undefined" ? window.location.origin : undefined
        );
        const name = u.pathname.split("/").pop() || "file";
        setFileName(name);
        const ext = getExt(name);
        setPreview(isImageExt(ext) ? url : null);
      } catch {
        // если это относительный путь без window — просто показать как есть
        const name = url.split("/").pop() || "file";
        setFileName(name);
        const ext = getExt(name);
        setPreview(isImageExt(ext) ? url : null);
      }
      return;
    }
    // 3) сброс
    setPreview(null);
    setFileName(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }, [file, url]);

  const handleFile = useCallback(
    (selectedFile: File) => {
      onChange(selectedFile);
      // оптимистично показываем сразу
      setFileName(selectedFile.name);
      if (selectedFile.type?.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => setPreview((e.target?.result as string) || null);
        reader.readAsDataURL(selectedFile);
      } else {
        setPreview(null);
      }
    },
    [onChange]
  );

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  };

  const handleRemove = () => {
    onChange(null);
    setPreview(null);
    setFileName(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleClick = () => fileInputRef.current?.click();

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
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
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
        <div className={styles.preview} onClick={(e) => e.stopPropagation()}>
          <img src={preview} alt="Preview" className={styles.preview__image} />
          <i
            className="pi pi-times"
            onClick={(e) => {
              e.stopPropagation();
              handleRemove();
            }}
          />
        </div>
      ) : fileName ? (
        <div className={styles.file__info} onClick={(e) => e.stopPropagation()}>
          <i className={getFileIcon(fileName)} />
          <span className={styles.file__name}>{fileName}</span>
          <i
            className="pi pi-times"
            onClick={(e) => {
              e.stopPropagation();
              handleRemove();
            }}
          />
        </div>
      ) : (
        <>
          <label className={styles.label}>
            <input
              ref={fileInputRef}
              type="file"
              className={styles.input}
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif,.webp,.avif,.bmp,.svg"
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

import styles from "./TextArea.module.scss";

interface TextAreaProps {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
}

export const TextArea = ({
  value,
  onChange,
  placeholder = "Введите текст...",
}: TextAreaProps) => {
  return (
    <textarea
      className={styles.textarea}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      rows={4}
    />
  );
};

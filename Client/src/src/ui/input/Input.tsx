import styles from "./Input.module.scss";

interface InputProps {
  type?: string;
  label?: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  radius?: string;
  error_text?: string;
  required?: boolean;
}

export const Input = ({
  type = "text",
  label,
  value,
  onChange,
  radius = "32px",
  error_text,
  required = false,
}: InputProps) => {
  return (
    <div className={styles.input__container}>
      <input
        required={required}
        type={type}
        className={styles.input + `${error_text ? " " + styles.error : ""}`}
        value={value}
        onChange={onChange}
        style={{
          borderRadius: radius,
        }}
      />
      <label className={styles.label}>{label}</label>
      {error_text && (
        <label className={styles.error__label}>{error_text}</label>
      )}
    </div>
  );
};

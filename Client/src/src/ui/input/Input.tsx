import { useState } from "react";
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
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const inputType = type === "password" && showPassword ? "text" : type;

  return (
    <div className={styles.input__container}>
      <input
        required={required}
        type={inputType}
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
      {type === "password" && (
        <button
          type="button"
          className={styles.password__toggle}
          onClick={togglePasswordVisibility}
          aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
        >
          <i className={`pi ${showPassword ? "pi-eye" : "pi-eye-slash"}`}></i>
        </button>
      )}
    </div>
  );
};

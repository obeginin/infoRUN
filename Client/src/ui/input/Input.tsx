import styles from "./Input.module.scss";

interface InputProps {
  type?: string;
  label?: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const Input = ({
  type = "text",
  label,
  value,
  onChange,
}: InputProps) => {
  return (
    <div className={styles.input__container}>
      <input
        type={type}
        className={styles.input}
        value={value}
        onChange={onChange}
      />
      <label>{label}</label>
    </div>
  );
};

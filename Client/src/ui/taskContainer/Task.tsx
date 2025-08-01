import styles from "./Task.module.scss";
export const Task = ({
  children,
  onClick,
  border = "primary",
}: {
  children: React.ReactNode;
  onClick?: () => void;
  border?: "primary" | "success" | "error" | "warning";
}) => {
  return (
    <div
      className={styles.task}
      onClick={onClick}
      style={{
        border: `1px solid var(--${border})`,
      }}
    >
      {children}
    </div>
  );
};

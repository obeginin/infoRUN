import type React from "react";
import styles from "./Task.module.scss";
export const Task = ({
  children,
  onClick,
  border = "primary",
  ref,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  border?: "primary" | "success" | "error" | "warning";
  ref?: React.Ref<HTMLDivElement>;
}) => {
  return (
    <div
      ref={ref}
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

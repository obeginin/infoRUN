import styles from "./ProfileContentContainer.module.scss";

interface ProfileContentContainerProps {
  children: React.ReactNode;
  width?: string;
  color?: "primary" | "secondary" | "purple";
  borderColor?:
    | "primary"
    | "secondary"
    | "purple"
    | "warning"
    | "error"
    | "success";
}

export const ProfileContentContainer = ({
  children,
  width,
  color,
  borderColor,
}: ProfileContentContainerProps) => {
  return (
    <div className={styles.outside__content} style={{ maxWidth: width }}>
      <div
        className={styles.content}
        style={{
          backgroundColor: color ? `var(--${color})` : "",
          border: borderColor ? `5px solid var(--${color})` : "",
          transition: "all 0.2s ease-in-out",
        }}
      >
        {children}
      </div>
    </div>
  );
};

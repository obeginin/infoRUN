import styles from "./ProfileContentContainer.module.scss";

interface ProfileContentContainerProps {
  children: React.ReactNode;
  width?: string;
  color?: "primary" | "secondary" | "purple";
}

export const ProfileContentContainer = ({
  children,
  width,
  color,
}: ProfileContentContainerProps) => {
  return (
    <div className={styles.outside__content} style={{ maxWidth: width }}>
      <div
        className={styles.content}
        style={{
          backgroundColor: color ? `var(--${color})` : "",
          border: color ? `1px solid var(--${color})` : "",
        }}
        >
        {children}
      </div>
    </div>
  );
};

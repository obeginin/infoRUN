import styles from "./ProfileContentContainer.module.scss";

interface ProfileContentContainerProps {
  children: React.ReactNode;
}

export const ProfileContentContainer = ({
  children,
}: ProfileContentContainerProps) => {
  return (
      <div className={styles.outside__content}>
        <div className={styles.content}>{children}</div>
    </div>
  );
};

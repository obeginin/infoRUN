import styles from "./BackroundGrid.module.scss";

interface BackgroundGridProps {
  children: React.ReactNode;
}

export const BackgroundGrid = ({ children }: BackgroundGridProps) => {
  return (
    <div className={styles.grid__background}>
      <div
        className={styles.grid__background__item}
        style={{
          backgroundSize: "40px 40px",
          backgroundImage: `
            linear-gradient(to right, #639aff 1px, transparent 1px),
            linear-gradient(to bottom, #639aff 1px, transparent 1px)
          `,
        }}
      >
        {children}
      </div>
    </div>
  );
};

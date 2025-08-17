import styles from "./BackroundGrid.module.scss";

export const BackgroundGrid = () => {
  return (
    <>
      <div className={styles.grid__background__blue}></div>
      <div className={styles.grid__background__container}>
        <div className={styles.grid__background__second}>
          <div className={styles.grid__background__item__third}></div>
        </div>
      </div>
    </>
  );
};

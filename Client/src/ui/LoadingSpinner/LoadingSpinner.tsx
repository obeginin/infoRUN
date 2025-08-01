import styles from "./LoadingSpinner.module.scss";
export const Spinner = () => {
  return (
    <div className={styles.spinner}>
      <span className={styles.loader}></span>
    </div>
  );
};

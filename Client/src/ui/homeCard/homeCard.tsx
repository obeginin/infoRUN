import styles from "./homeCard.module.scss";

interface HomeCardProps {
  children: React.ReactNode;
  color: string;
  rotate?: string;
  img: string;
}

export const HomeCard = ({ children, color, rotate, img }: HomeCardProps) => {
  return (
    <div
      className={
        styles.card__container + `${rotate ? " " + styles.rotate : ""}`
      }
      style={{}}
    >
      <div
        className={styles.card__content}
        style={{ background: color, position: "relative" }}
      >
        <div className={styles.card}>{children}</div>
        <img
          src={img}
          alt=""
          style={{ width: "100%", position: "absolute", bottom: -100 }}
        />
      </div>
    </div>
  );
};

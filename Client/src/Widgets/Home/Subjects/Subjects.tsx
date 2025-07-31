import styles from "./Subjects.module.scss";
import { Paragraph } from "../../../ui/p/Paragraph";
import male1 from "../../../assets/subjects/male1.png";
import male2 from "../../../assets/subjects/male2.png";
import { Button } from "../../../ui/buttonDeafault/Button";

export const Subjects = () => {
  return (
    <div className="app">
      <div className={styles.container}>
        <Paragraph size="medium" f_weight="bold">
          Предметы
        </Paragraph>
        <div className={styles.content}>
          <div className={styles.card}>
            <Button filled>Информатика</Button>
            <img src={male1} alt="" />
          </div>
          <div className={styles.card}>
            <div
              style={{
                display: "flex",
                gap: "10px",
                justifyContent: "space-between",
              }}
            >
              <Button filled>Другие предметы</Button>
              <Button>Скоро</Button>
            </div>
            <img src={male2} alt="" />
          </div>
        </div>
      </div>
    </div>
  );
};

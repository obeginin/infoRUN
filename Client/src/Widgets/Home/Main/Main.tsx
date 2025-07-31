import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./Main.module.scss";
import rocket from "../../../assets/rocket-icon.svg";
import pencil from "../../../assets/pencil-icon.svg";
import male1 from "../../../assets/male1.svg";
import male2 from "../../../assets/male2.svg";
import male3 from "../../../assets/male3.svg";
import male4 from "../../../assets/male4.svg";

export const Main = () => {
  return (
    <>
      <section>
        <div className="app">
          <div className={styles.container} style={{ position: "relative" }}>
            <div className={styles.main}>
              <div className={styles.main__content}>
                <h1>
                  Онлайн-платформа для подготовки к
                  <span className={styles.ege}> ЕГЭ</span> — твой личный
                  репетитор 24/7!
                </h1>
                <Paragraph>
                  Добро пожаловать на уникальный образовательный сервис,
                  созданный специально для эффективной и комфортной подготовки к
                  ЕГЭ!
                </Paragraph>
              </div>
              <img src={pencil} alt="" className={styles.pencil} />
              <img src={rocket} alt="" className={styles.rocket} />
            </div>
            <div className={styles.cards__container}>
              <img src={male1} alt="" />
              <img src={male2} alt="" />
              <img src={male3} alt="" />
              <img src={male4} alt="" />
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

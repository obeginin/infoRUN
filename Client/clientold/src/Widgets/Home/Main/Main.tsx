import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./Main.module.scss";
import rocket from "../../../assets/rocket-icon.svg";
import pencil from "../../../assets/pencil-icon.svg";
import male1 from "../../../assets/subjects/male3.png";
import male2 from "../../../assets/subjects/male4.png";
import male3 from "../../../assets/subjects/male5.png";
import male4 from "../../../assets/subjects/male6.png";

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
              {data.map((item) => (
                <div className={styles.outline}>
                  <div
                    key={item.id}
                    className={styles.card + " " + styles[item.color]}
                    style={{ backgroundColor: `var(--${item.color})` }}
                  >
                    <img src={item.img} alt="" />
                    <span>{item.description}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

const data = [
  {
    id: 1,
    img: male1,
    description: "Личный кабинет",
    color: "primary",
  },
  {
    id: 2,
    img: male2,
    description: "Вариант № ",
    color: "secondary",
  },
  {
    id: 3,
    img: male3,
    description: "Каталог заданий",
    color: "purple",
  },
  {
    id: 4,
    img: male4,
    description: "Мои задачи",
    color: "peach",
  },
];

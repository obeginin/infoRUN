import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./Main.module.scss";
import rocket from "@public/assets/rocket-icon.svg";
import pencil from "@public/assets/pencil-icon.svg";
import male1 from "@public/subjects/male3.svg";
import male2 from "@public/subjects/male4.svg";
import male3 from "@public/subjects/male5.svg";
import male4 from "@public/subjects/male6.svg";
import Image from "next/image";
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
              <Image src={pencil} alt="" className={styles.pencil} />
              <Image src={rocket} alt="" className={styles.rocket} />
            </div>
            <div className={styles.cards__container}>
              {data.map((item) => (
                <div className={styles.outline} key={item.id}>
                  <div
                    key={item.id}
                    className={styles.card + " " + styles[item.color]}
                    style={{ backgroundColor: `var(--${item.color})` }}
                  >
                    <Image src={item.img} alt="" />
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

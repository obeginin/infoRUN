import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./Admin.module.scss";
import Image from "next/image";
import card1 from "@public/home-admin/card1.svg";
import card2 from "@public/home-admin/card2.svg";
import card3 from "@public/home-admin/card3.svg";
import card4 from "@public/home-admin/card4.svg";

export const Admin = () => {
  return (
    <section>
      <div className="app">
        <div className={styles.container}>
          <Paragraph size="medium" f_weight="extra_bold">
            Панель администрирования{" "}
          </Paragraph>

          <div className={styles.content}>
            {data.map((item) => (
              <div key={item.id} className={styles.card}>
                {item.id % 2 === 0 ? (
                  <div className={styles.card__reverse}>
                    <Paragraph>{item.title}</Paragraph>
                    <Image src={item.img} alt="" />
                  </div>
                ) : (
                  <>
                    <Image src={item.img} alt="" />
                    <Paragraph>{item.title}</Paragraph>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

const data = [
  {
    id: 1,
    img: card1,
    title: "Полный контроль над системой",
  },
  {
    id: 2,
    img: card2,
    title: "Доступ ко всем данным и пользователям",
  },
  {
    id: 3,
    img: card3,
    title: "Назначение ролей и разрешений",
  },
  {
    id: 4,
    img: card4,
    title: "Импорт и экспорт заданий, история действий",
  },
];

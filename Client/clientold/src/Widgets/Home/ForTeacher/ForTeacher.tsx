import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./ForTeacher.module.scss";

export const ForTeacher = () => {
  return (
    <section>
      <div className="app">
        <div className={styles.container}>
          <Paragraph size="medium" f_weight="extra_bold">
            Для преподавателей и школ
          </Paragraph>

          <div className={styles.content}>
            {data.map((item) => (
              <div key={item.id} className={styles.card}>
                <Paragraph>{item.title}</Paragraph>
                <Paragraph size="small">{item.description}</Paragraph>
              </div>
            ))}
          </div>

          <div style={{ textAlign: "center" }}>
            <Button color="white" filled>Зарегистрироваться</Button>
          </div>
        </div>
      </div>
    </section>
  );
};

const data = [
  {
    id: 1,
    title: "Управление учениками и их прогрессом",
    description:
      "Удобное отображение прогресса в личном кабинете для отслеживания ваших результатов",
  },
  {
    id: 2,
    title: "Гибкая система статистики и контроля",
    description:
      "Удобное отображение прогресса в личном кабинете для отслеживания ваших результатов",
  },
  {
    id: 3,
    title: "Создание и выдача собственных заданий",
    description:
      "Удобное отображение прогресса в личном кабинете для отслеживания ваших результатов",
  },
  {
    id: 4,
    title: "Удобная фильтрация и поиск",
    description:
      "Удобное отображение прогресса в личном кабинете для отслеживания ваших результатов",
  },
];

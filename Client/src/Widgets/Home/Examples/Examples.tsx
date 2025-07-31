import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./Examples.module.scss";
import task from "../../../assets/task_ex.png";
import { Button } from "../../../ui/buttonDeafault/Button";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
export const Examples = () => {
  return (
    <section>
      <div className="app">
        <div className={styles.container}>
          <Paragraph size="medium" f_weight="extra_bold">
            Примеры заданий
          </Paragraph>

          <ProfileContentContainer>
            <div className={styles.content}>
              <div className={styles.counter__exam}>
                <Button filled>Информатика</Button>
                <Button>смотреть все</Button>
              </div>
              <img src={task} alt="" />
            </div>
          </ProfileContentContainer>

          <div style={{ textAlign: "center" }}>
            <Button filled>Перейти в каталог</Button>
          </div>
        </div>
      </div>
    </section>
  );
};

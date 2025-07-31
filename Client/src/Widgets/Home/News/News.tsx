import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./News.module.scss";
import laptop from "../../../assets/laptop.svg";

export const News = () => {
  return (
    <section>
      <div className="app">
        <div className={styles.conteiner}>
          <Paragraph size="medium" f_weight="bold">
            Новости
          </Paragraph>
          <div className={styles.content}>
            <ProfileContentContainer>
              <div className={styles.card}>
                <div className={styles.buttons}>
                  <Button disabled style={{
                      border: `1px solid ${"var(--primary)"}`,
                  }}>
                    Скоро 1 сентября — начни подготовку уже сейчас!
                  </Button>
                  <Button filled>смотреть все</Button>
                </div>
                <div className={styles.text}>
                  <Paragraph>
                    Новый учебный год не за горами! <br />
                    Хочешь встретить 1 сентября уверенно? Начни готовиться к ЕГЭ
                    уже сегодня — решай задания, проходи варианты и следи за
                    своей статистикой.
                    <br /> Лучший результат начинается с раннего старта.
                  </Paragraph>
                </div>
                <img src={laptop} alt="" className={styles.laptop} />
              </div>
            </ProfileContentContainer>
          </div>
        </div>
      </div>
    </section>
  );
};

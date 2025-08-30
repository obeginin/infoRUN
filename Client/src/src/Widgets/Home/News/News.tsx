import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./News.module.scss";
import laptop from "@public/assets/laptop.svg";
import Image from "next/image";
import { TextContainer } from "@/src/ui/textContainer/TextContainer";
export const News = () => {
  return (
    <section>
      <div className="app">
        <div className={styles.conteiner}>
          <Paragraph size="medium" f_weight="extra_bold">
            Новости
          </Paragraph>
          <div className={styles.content}>
            <ProfileContentContainer>
              <div className={styles.card}>
                <div className={styles.buttons}>
                  <TextContainer>
                    Скоро 1 сентября — начни подготовку уже сейчас!
                  </TextContainer>
                  <Button color="white" filled>смотреть все</Button>
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
                <Image src={laptop} alt="" className={styles.laptop} />
              </div>
            </ProfileContentContainer>
          </div>
        </div>
      </div>
    </section>
  );
};

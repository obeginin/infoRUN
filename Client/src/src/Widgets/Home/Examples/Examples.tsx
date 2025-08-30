import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./Examples.module.scss";
import task from "@public/assets/task_ex.svg";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import Image from "next/image";
import { TextContainer } from "@/src/ui/textContainer/TextContainer";
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
                <TextContainer color="white" filled>Информатика</TextContainer>
                <Button outlined>смотреть все</Button>
              </div>
              <Image src={task} alt="" />
            </div>
          </ProfileContentContainer>

          <div style={{ textAlign: "center" }}>
            <Button color="white" filled>Перейти в каталог</Button>
          </div>
        </div>
      </div>
    </section>
  );
};

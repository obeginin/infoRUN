import styles from "./Subjects.module.scss";
import { Paragraph } from "@/src/ui/p/Paragraph";
import male1 from "@public/subjects/male1.svg";
import male2 from "@public/subjects/male2.svg";
import { Button } from "@/src/ui/buttonDeafault/Button";
import Image from "next/image";

export const Subjects = () => {
  return (
    <div className="app">
      <div className={styles.container}>
        <Paragraph size="medium" f_weight="extra_bold">
          Предметы
        </Paragraph>
        <div className={styles.content}>
          <div className={styles.card}>
            <div style={{display: "flex", gap: "10px", justifyContent: "space-between"}}>
            <Button color="white" filled>Информатика</Button>
            </div>
            <Image src={male1} alt="" />
          </div>
          <div className={styles.card}>
            <div
              style={{
                display: "flex",
                gap: "10px",
                justifyContent: "space-between",
              }}
            >
              <Button color="white" filled>Другие предметы</Button>
              <Button outlined>Скоро</Button>
            </div>
            <Image src={male2} alt="" />
          </div>
        </div>
      </div>
    </div>
  );
};

"use client";

import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./Main.module.scss";
import rocket from "@public/assets/rocket-icon.svg";
import pencil from "@public/assets/pencil-icon.svg";
import male1 from "@public/subjects/male1.webp";
import male2 from "@public/subjects/male2.webp";
import male3 from "@public/subjects/male3.webp";
import male4 from "@public/subjects/male4.webp";
import Image from "next/image";
import { useState, useEffect } from "react";
// import { motion, useScroll, useTransform } from "framer-motion";

export const Main = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  // const { scrollYProgress } = useScroll();
  // const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);
  // const scale = useTransform(scrollYProgress, [0, 1], [1, 1.5]);

  useEffect(() => {
    // Запускаем анимацию после монтирования компонента
    const timer = setTimeout(() => {
      setIsLoaded(true);
    }, 300);

    return () => clearTimeout(timer);
  }, []);

  return (
    // <motion.div style={{ opacity, scale }}>
    <section>
      <div className="app">
        <div className={styles.container} style={{ position: "relative" }}>
          <div className={styles.main}>
            <div className={styles.main__content}>
              <h1>
                Онлайн-платформа для подготовки к
                <span className={styles.ege}> ЕГЭ</span> — твой личный репетитор
                24/7!
              </h1>
              <Paragraph>
                Добро пожаловать на уникальный образовательный сервис, созданный
                специально для эффективной и комфортной подготовки к ЕГЭ!
              </Paragraph>
            </div>
            <Image
              src={pencil}
              alt=""
              className={`${styles.pencil} ${isLoaded ? styles.loaded : ""}`}
            />
            <Image
              src={rocket}
              alt=""
              className={`${styles.rocket} ${isLoaded ? styles.loaded : ""}`}
            />
          </div>
          <div className={styles.cards__container}>
            {data.map((item, index) => (
              <div
                className={`${styles.outline} ${isLoaded ? styles.loaded : ""}`}
                key={item.id}
                style={
                  {
                    "--animation-delay": `${index * 0.3}s`,
                  } as React.CSSProperties
                }
              >
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
    // </motion.div>
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

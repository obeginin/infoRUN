import styles from "./Footer.module.scss";
import { AnimationLink } from "@/src/ui/AnimationLink/AnimationLink";
export const Footer = () => {
  return (
    // <div className={styles["footer-sticky"]}>
    <footer style={{ }}>
      <div className={styles.line}></div>
      <div style={{ maxWidth: "1400px", margin: "0 auto" }}>
        <div className={styles.container}>
          <ul>
            <AnimationLink href="/">О сервисе</AnimationLink>
            <AnimationLink href="/">Личный кабинет</AnimationLink>
            <AnimationLink href="/">Демоверсии</AnimationLink>
          </ul>

          <ul>
            <AnimationLink href="/">Поддержка</AnimationLink>
            <AnimationLink href="/">Каталог заданий</AnimationLink>
            <AnimationLink href="">Спецификации</AnimationLink>
          </ul>

          <ul>
            <AnimationLink href="/politics">
              Политика конфиденциальности
            </AnimationLink>
            <AnimationLink href="/">Мои задачи</AnimationLink>
            <AnimationLink href="/">Кодификаторы</AnimationLink>
          </ul>
        </div>
      </div>
      <div className={styles.line}></div>
      <div style={{ maxWidth: "1400px", margin: "0 auto" }}>
        <ul className={styles.bottom}>
          <AnimationLink href="https://t.me/obeginin">
            backend: @obeginin
          </AnimationLink>
          <div className={styles.vertical__line}></div>
          <AnimationLink href="https://t.me/kvantoose">
            frontend: @kvantoose
          </AnimationLink>
          <div className={styles.vertical__line}></div>
          <AnimationLink href="https://t.me/savorovskaya_v">
            ux/ui-design: @savorovskaya_v
          </AnimationLink>
        </ul>

        <div className={styles.mobile}>
          <div className={styles.content}>
            <ul>
              <AnimationLink href="/">О сервисе</AnimationLink>
              <AnimationLink href="/">Личный кабинет</AnimationLink>
              <AnimationLink href="/">Демоверсии</AnimationLink>
            </ul>
            <ul>
              <AnimationLink href="/">Поддержка</AnimationLink>
              <AnimationLink href="/">Каталог заданий</AnimationLink>
              <AnimationLink href="">Спецификации</AnimationLink>
            </ul>
          </div>
          <div className={styles.line}></div>
          <ul>
            <AnimationLink href="/politics">
              Политика конфиденциальности
            </AnimationLink>
            <AnimationLink href="/">Мои задачи</AnimationLink>
            <AnimationLink href="/">Кодификаторы</AnimationLink>
          </ul>
          <div className={styles.line}></div>

          <div>
            <ul>
              <AnimationLink href="https://t.me/obeginin">
                backend: @obeginin
              </AnimationLink>
              <AnimationLink href="https://t.me/kvantoose">
                frontend: @kvantoose
              </AnimationLink>
              <AnimationLink href="https://t.me/savorovskaya_v">
                ux/ui-design: @savorovskaya_v
              </AnimationLink>
            </ul>
          </div>
        </div>
      </div>
    </footer>
    // </div>
  );
};

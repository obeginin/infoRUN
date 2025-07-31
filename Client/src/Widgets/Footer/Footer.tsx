import styles from "./Footer.module.scss";
export const Footer = () => {
  return (
    <div className={styles["footer-sticky"]}>
      <footer>
        <div className={styles.line}></div>
        <div className="app">
          <div className={styles.container}>
            <ul>
              <li>
                <a href="/">О сервисе</a>
              </li>
              <li>
                <a href="/">Личный кабинет</a>
              </li>
              <li>
                <a href="/">Демоверсии</a>
              </li>
            </ul>

            <ul>
              <li>
                <a href="/">Поддержка</a>
              </li>
              <li>
                <a href="/">Каталог заданий</a>
              </li>
              <li>
                <a href="/">Спецификации</a>
              </li>
            </ul>

            <ul>
              <li>
                <a href="/politics">Политика конфиденциальности</a>
              </li>
              <li>
                <a href="/">Мои задачи</a>
              </li>
              <li>
                <a href="/">Кодификаторы</a>
              </li>
            </ul>
          </div>
          <div className={styles.line}></div>
          <ul className={styles.bottom}>
            <li>
              backend: <a href="">@oleg_beginin</a>
            </li>
            <div className={styles.vertical__line}></div>
            <li>
              frontend: <a href="">@kvantoose</a>
            </li>
            <div className={styles.vertical__line}></div>
            <li>
              ux/ui-design:: <a href="">@savorovskaya_v</a>
            </li>
          </ul>

          <div className={styles.mobile}>
            <div className={styles.content}>
              <ul>
                <li>
                  <a href="/">О сервисе</a>
                </li>
                <li>
                  <a href="/">Личный кабинет</a>
                </li>
                <li>
                  <a href="/">Демоверсии</a>
                </li>
              </ul>
              <ul>
                <li>
                  <a href="/">Поддержка</a>
                </li>
                <li>
                  <a href="/">Каталог заданий</a>
                </li>
                <li>
                  <a href="/">Спецификации</a>
                </li>
              </ul>
            </div>

            <div className={styles.line}></div>

            <ul>
              <li>
                <a href="/politics">Политика конфиденциальности</a>
              </li>
              <li>
                <a href="/">Мои задачи</a>
              </li>
              <li>
                <a href="/">Кодификаторы</a>
              </li>
            </ul>
            <div className={styles.line}></div>

            <div>
              <ul>
                <li>
                  backend: <a href="">@oleg_beginin</a>
                </li>
                <li>
                  frontend: <a href="">@kvantoose</a>
                </li>
                <li>
                  ux/ui-design:: <a href="">@savorovskaya_v</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

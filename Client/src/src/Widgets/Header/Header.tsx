"use client";

import burger from "@public/assets/burger-menu.svg";
import { Button } from "@/src/ui/buttonDeafault/Button";
import styles from "./Header.module.scss";
import { useUserStore } from "../../store/userStore";
// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { AnimationLink } from "@/src/ui/AnimationLink/AnimationLink";

export const Header = () => {
  // const nav = useNavigate();
  const useUserLogout = useUserStore((state) => state.logout);
  const user = useUserStore((state) => state.user);
  // const theme = localStorage.getItem("theme");
  // const [isDark, setIsDart] = useState(theme === "dark" ? true : false);

  // const handleClick = () => {
  //   setIsDart(!isDark);
  //   localStorage.setItem("theme", isDark ? "light" : "dark");
  // };

  // useEffect(() => {
  //   const theme = localStorage.getItem("theme");
  //   document.documentElement.setAttribute("data-theme", theme as string);
  // }, [isDark]);

  return (
    <header className={styles.header}>
      <div className={styles.content__right}>
        <Image src={burger} alt="" className={styles.burger} />
        {user?.RoleName === "Админ" && (
          <Button color="white" filled>
            admin
          </Button>
        )}
        <ul className={styles.list}>
          <AnimationLink href="/profile" size="base">
            Профиль
          </AnimationLink>
          <AnimationLink href="/profile/all-tasks" size="base">
            Мои задачи
          </AnimationLink>
          <AnimationLink href="/" size="base">
            Категории заданий
          </AnimationLink>
        </ul>
        {/* <div
          className={
            styles.theme_switcher + " " + (isDark ? styles.dark : styles.light)
          }
        >
          <i onClick={() => handleClick()} className={`pi pi-sun`}></i>
        </div> */}
        {!user ? (
          <Link href="/auth">
            <Button color="white" filled>
              Войти
            </Button>
          </Link>
        ) : (
          <Button outlined onClick={useUserLogout}>
            Выйти
          </Button>
        )}
      </div>
    </header>
  );
};

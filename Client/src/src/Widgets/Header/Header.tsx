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
import { useEffect, useState } from "react";

export const Header = () => {
  // const nav = useNavigate();
  const useUserLogout = useUserStore((state) => state.logout);
  const user = useUserStore((state) => state.user);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollThreshold = 100;

      if (window.scrollY > scrollThreshold) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

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
    <header>
      <div className={`${styles.header} ${isScrolled ? styles.scrolled : ""}`}>
        {/* <div
          style={{
            width: "100%",
            borderRadius: "32px",
            padding: "10px 10px",
            backgroundColor: "var(--bg)",
          }}
        > */}
          <div className={styles.content__right}>
            <Image src={burger} alt="" className={styles.burger} />
            {user?.RoleName === "Админ" && (
              <Link href="/admin">
                <Button color="white" filled>
                  admin
                </Button>
              </Link>
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
        </div>
      {/* </div> */}
    </header>
  );
};

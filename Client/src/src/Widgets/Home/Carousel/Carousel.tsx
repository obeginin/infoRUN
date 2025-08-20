'use client'

import styles from "./Carousel.module.scss";
import slide1 from "@public/carousel/slide1.svg";
import slide2 from "@public/carousel/slide2.svg";
import slide3 from "@public/carousel/slide3.svg";
import slide4 from "@public/carousel/slide4.svg";
import { useState, useEffect, useRef, useLayoutEffect } from "react";
import { Paragraph } from "../../../ui/p/Paragraph";
import { gsap } from "gsap";
import Image from "next/image";
export const Carousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const trackRef = useRef<HTMLDivElement | null>(null);
  const slideRefs = useRef<(HTMLDivElement | null)[]>([]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev === slides.length - 1 ? 0 : prev + 1));
  };

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  const disableTrackCssTransition = () => {
    if (trackRef.current) {
      trackRef.current.style.transition = "none";
    }
  };

  useLayoutEffect(() => {
    if (!trackRef.current) return;
    disableTrackCssTransition();
    gsap.set(trackRef.current, { xPercent: 0, force3D: true });
    const first = slideRefs.current[0];
    if (first) {
      const items = first.querySelectorAll("p, img");
      gsap.fromTo(
        items,
        { opacity: 0, y: 16, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out", stagger: 0.08 }
      );
    }
  }, []);

  useLayoutEffect(() => {
    if (!trackRef.current) return;
    disableTrackCssTransition();
    gsap.killTweensOf(trackRef.current);
    gsap.to(trackRef.current, {
      xPercent: -100 * currentSlide,
      duration: 0.9,
      ease: "power4.inOut",
      force3D: true,
      overwrite: "auto",
    });

    const active = slideRefs.current[currentSlide];
    if (active) {
      const items = active.querySelectorAll("p, img");
      gsap.fromTo(
        items,
        { opacity: 0, y: 16, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out", stagger: 0.08, overwrite: "auto" }
      );
    }
  }, [currentSlide]);

  useEffect(() => {
    const interval = setInterval(nextSlide, 5000);
    return () => clearInterval(interval);
  }, [currentSlide]);

  return (
    <div className="app">
      <div className={styles.carousel}>
        <div
          className={styles.carouselInner}
          ref={trackRef}
        >
          {slides.map((slide, index) => (
            <div
              key={slide.id}
              className={styles.carouselSlide}
              ref={(el) => {
                slideRefs.current[index] = el;
              }}
            >
              <Paragraph>{slide.description}</Paragraph>
              <Image src={slide.image} alt={`Slide ${slide.id}`} />
            </div>
          ))}
        </div>

        <div className={styles.carouselIndicators}>
          {slides.map((_, index) => (
            <button
              key={index}
              className={`${styles.indicator} ${
                index === currentSlide ? styles.active : ""
              }`}
              onClick={() => goToSlide(index)}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};



  const slides = [
    {
      id: 1,
      image: slide1,
      description: "Режим тренировки и тестирования — учись, как тебе удобно",
    },
    {
      id: 2,
      image: slide2,
      description:
        "Варианты экзаменов с реальным таймером  и автоматической проверкой",
    },
    {
      id: 3,
      image: slide3,
      description: "Личный кабинет с полной статистикой и историей прогресса",
    },
    {
      id: 4,
      image: slide4,
      description:
        "Интерактивные задания по всем категориям Единого государственного экзамена",
    },
  ];
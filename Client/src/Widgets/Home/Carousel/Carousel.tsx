import styles from "./Carousel.module.scss";
import slide1 from "../../../assets/carousel/slide1.svg";
import slide2 from "../../../assets/carousel/slide2.svg";
import slide3 from "../../../assets/carousel/slide3.svg";
import slide4 from "../../../assets/carousel/slide4.svg";
import { useState, useEffect } from "react";
import { Paragraph } from "../../../ui/p/Paragraph";

export const Carousel = () => {
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

  const [currentSlide, setCurrentSlide] = useState(0);
  const nextSlide = () => {
    setCurrentSlide((prev) => (prev === slides.length - 1 ? 0 : prev + 1));
  };

//   const prevSlide = () => {
//     setCurrentSlide((prev) => (prev === 0 ? slides.length - 1 : prev - 1));
//   };

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  useEffect(() => {
    const interval = setInterval(nextSlide, 2000);
    return () => clearInterval(interval);
  }, [currentSlide]);

  return (
    <div className="app">
      <div className={styles.carousel}>
        <div
          className={styles.carouselInner}
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {slides.map((slide) => (
            <div key={slide.id} className={styles.carouselSlide}>
              <Paragraph>{slide.description}</Paragraph>
              <img src={slide.image} alt={`Slide ${slide.id}`} />
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

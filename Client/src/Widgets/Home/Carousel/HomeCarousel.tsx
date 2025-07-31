import { Paragraph } from "../../../ui/p/Paragraph";
import { Carousel } from "./Carousel";
import styles from "./HomeCarousel.module.scss"
export const HomeCarousel = () => {
  return (
    <div className="app">
      <div className={styles.container}>
        <Paragraph size="medium" f_weight="extra_bold">
          Что мы предлагаем?
        </Paragraph>
        <Carousel />
      </div>
    </div>
  );
};

import group from "@public/alphabet/group.svg";
import Image from "next/image";
import styles from "./backgroundPaper.module.scss";

interface BackgroundDefaultProps {
  count?: number;
  className?: string;
}

export const BackgroundDefault = ({
  count = 1,
  className,
}: BackgroundDefaultProps) => {
  const images = Array.from({ length: count }, (_, index) => (
    <Image
      key={index}
      src={group}
      alt=""
      className={`${styles.group} ${styles[`group`]} ${className}`}
    />
  ));
  return <>{images.map((image) => image)}</>;
};

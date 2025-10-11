import styles from "./BreadCrumb.module.scss";
import { AnimationLink } from "../AnimationLink/AnimationLink";

interface BreadCrumbProps {
  items: IItem[];
}

interface IItem {
  id: number;
  label: string;
  link: string;
}

export const BreadCrumb = ({ items }: BreadCrumbProps) => {
  return (
    <div className={styles.breadCrumb}>
      <AnimationLink href="/">Главная</AnimationLink>
      
      {items.map((item) => (
        <div key={item.id} className={styles.breadCrumbItem}>
          <span className={styles.separator}> / </span>
          <AnimationLink href={item.link}>{item.label}</AnimationLink>
        </div>
      ))}
    </div>
  );
};
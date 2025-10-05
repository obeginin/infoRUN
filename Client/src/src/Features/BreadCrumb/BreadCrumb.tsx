import { ALink } from "@/src/ui/a/ALink";
import { Li, Ul } from "@/src/ui/ul-li/UlLi";
import styles from "./BreadCrumb.module.scss";
interface BreadCrumbProps {
  prevPage?: string;
  currentPage: string;
}

export const BreadCrumb = ({ prevPage, currentPage }: BreadCrumbProps) => {
  return (
    <div className={styles.breadCrumb}>
      <Ul direcrion="row" justifyContent="flex-start" alignItems="flex-start">
        <Li>
          <ALink href="/">Главная</ALink>
        </Li>
        {prevPage && (
          <>
            <span className={styles.span}> / </span>
            <Li>
              <ALink href="/">{prevPage}</ALink>
            </Li>
          </>
        )}
        <span className={styles.span}> / </span>
        <Li>
          <ALink href="/">{currentPage}</ALink>
        </Li>
      </Ul>
    </div>
  );
};

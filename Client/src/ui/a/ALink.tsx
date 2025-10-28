import styles from "./ALink.module.scss";

interface ALinkProps {
  children: React.ReactNode;
  href: string;
}

export const ALink = ({ children, href, ...props }: ALinkProps) => {
  return (
    <>
      <a href={href} {...props} className={styles.link}>
        {children}
      </a>
    </>
  );
};

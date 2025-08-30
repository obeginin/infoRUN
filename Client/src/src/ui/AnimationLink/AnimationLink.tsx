import styles from "./AnimationLink.module.scss";
import Link from "next/link";
type LinkProps = {
  children: React.ReactNode;
  href: string;
  size?: "large" | "medium" | "base" | "small" | "tiny";
};

export const AnimationLink = ({
  children,
  href,
  size='base',
  ...props
}: LinkProps) => {
  return (
    <span className={styles.container}>
      <li {...props} className={styles.link} style={{ fontSize: `var(--${size})` }}>
        <Link href={href ? href : "/"}>{children}</Link>
      </li>
    </span>
  );
};

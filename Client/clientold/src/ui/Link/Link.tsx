import styles from "./Link.module.scss"

type LinkProps = {
    children: React.ReactNode;
    href: string;
}

export const Link = ({ children, ...props }: LinkProps) => {
    return (
        <a {...props} className={styles.link}>
            {children}
        </a>
    );
};
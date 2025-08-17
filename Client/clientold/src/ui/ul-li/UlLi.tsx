import styles from "./UlLi.module.scss";

interface UlLiProps {
  children: React.ReactNode;
  direcrion?: "row" | "column";
  justifyContent?: "flex-start" | "flex-end" | "center" | "space-between" | "space-around" | "space-evenly";
  alignItems?: "flex-start" | "flex-end" | "center";
}

export const Ul = ({ direcrion = "row", justifyContent = "space-between", alignItems = "center", children, ...props }: UlLiProps) => {
  return (
    <>
      <ul
        style={{
          listStyle: "none",
          display: "flex",
          flexDirection: direcrion,
          justifyContent: justifyContent,
          alignItems: alignItems,
          gap: "20px",
        }}
        {...props}
        className={styles.ul}
      >
        {children}
      </ul>
    </>
  );
};

export const Li = ({ children, ...props }: UlLiProps) => {
  return <li {...props} className={styles.list} style={{
    fontFamily: "Lato",
  }}>{children}</li>;
};
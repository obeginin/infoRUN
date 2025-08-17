interface ParagraphProps {
  children: React.ReactNode;
  size?: "large" | "medium" | "base" | "small" | "tiny";
  f_weight?: "light" | "bold" | "extra_bold";
  color?: "text" | "primary" | "white" | "gray";
}

export const Paragraph = ({
  children,
  size = "base",
  f_weight = "light",
  color,
}: ParagraphProps) => {
  return (
    <p
      style={{
        fontSize: `var(--${size})`,
        fontWeight: `var(--fw_${f_weight})`,
        fontFamily: "Lato",
        color: `var(--${color})`
      }}
    >
      {children}
    </p>
  );
};

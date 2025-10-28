interface ParagraphProps {
  children: React.ReactNode;
  size?: "large" | "medium" | "base" | "small" | "tiny";
  f_weight?: "light" | "bold" | "extra_bold";
  color?: "text" | "primary" | "white" | "gray";
  italic?: boolean;
}

export const Paragraph = ({
  children,
  size = "base",
  f_weight = "light",
  color,
  italic = false,
}: ParagraphProps) => {
  return (
    <p
      style={{
        fontSize: `var(--${size})`,
        fontWeight: `var(--fw_${f_weight})`,
        color: `var(--${color})`,
        fontStyle: italic ? "italic" : "normal",
      }}
    >
      {children}
    </p>
  );
};

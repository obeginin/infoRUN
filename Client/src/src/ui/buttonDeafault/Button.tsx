import styles from "./Button.module.scss";

interface ButtonProps {
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: () => void;
  radius?: string;
  filled?: boolean;
  outlined?: boolean;
  border?: "primary" | "white";
  color?: "primary" | "secondary" | "white" | "text" | "error";
  style?: React.CSSProperties;
  type?: "button" | "submit" | "reset";
  width?: "full" | "auto";
  size?: "small" | "base";
  fontSize?: "tiny" | "small" | "base" | "medium" | "large";
  loading?: boolean;
}

export const Button = ({
  children,
  disabled = false,
  onClick,
  radius = "32px",
  filled = false,
  border,
  outlined = false,
  color = "text",
  style,
  type,
  width = "auto",
  loading = false,
  size = "base",
  fontSize = "base",
}: ButtonProps) => {
  const baseStyles = {
    zIndex: 10,
    width: width === "full" ? "100%" : "auto",
    fontSize: `var(--${fontSize})`,
    borderRadius: radius,
    padding: size === "base" ? "10px 25px" : "5px 10px",
    backgroundColor: filled ? "var(--primary)" : "transparent",
    color: color ? `var(--${color})` : filled ? "var(--bg)" : "var(--text)",
    border: border
      ? `1px solid var(--${border})`
      : outlined
      ? "1px solid var(--primary)"
      : "none",
  };

  const finalStyles = style ? style : baseStyles;

  if (loading) {
    disabled = true;
  }

  return (
    <button
      type={type}
      style={finalStyles}
      className={`${styles.button} ${
        disabled ? styles.disabled : styles.active
      } ${outlined ? styles.outlined : ""}`}
      disabled={disabled}
      onClick={onClick}
    >
      {loading ? (
        <span
          style={{ fontSize: "1.2rem" }}
          className={`${styles.spinner} `}
        ></span>
      ) : (
        children
      )}
    </button>
  );
};

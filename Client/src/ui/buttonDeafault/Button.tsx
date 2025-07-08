import styles from "./Button.module.scss";

interface ButtonProps {
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: () => void;
}

export const Button = ({
  children,
  disabled = false,
  onClick,
}: ButtonProps) => {
  return (
    <>
      <button 
        className={styles.button + " " + (disabled ? styles.disabled : "")} 
        disabled={disabled} 
        onClick={onClick}
        >
        {children}
      </button>
    </>
  );
};

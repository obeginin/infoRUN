import styles from "./SelectButton.module.scss";

interface SelectButtonProps {
  first_value: string;
  second_value: string;
  activeButton: string;
  setActiveButton: React.Dispatch<React.SetStateAction<string>>;
}
export const SelectButton = ({
  first_value,
  second_value,
  activeButton,
  setActiveButton,
}: SelectButtonProps) => {
  return (
    <div className={styles.select__container}>
      <button
        onClick={() => setActiveButton(second_value)}
        className={styles.select__button + " " + (activeButton === second_value ? styles.active : "")}
      >
        {second_value}
      </button>
      <button
        onClick={() => setActiveButton(first_value)}
        className={styles.select__button + " " + (activeButton === first_value ? styles.active : "")}
      >
        {first_value}
      </button>
    </div>
  );
};

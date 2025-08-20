import styles from "./selectOption.module.scss";

interface SelectOptionProps {
  name: string;
  data: string[];
}
export const SelectOption = ({ name, data }: SelectOptionProps) => {
  return (
    <>
      <select value={name} defaultValue={name} className={styles.select}>
        <option disabled selected>{name}</option>
        <hr />
        {data.map((item, index) => (
          <option className={styles.option} key={index} value={item}>
            {item}
          </option>
        ))}
      </select>
    </>
  );
};

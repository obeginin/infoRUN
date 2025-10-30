import { MyCalendar } from "@/ui/calendar/Calendar";
import { Input } from "@/ui/input/Input";
import { Button } from "@/ui/buttonDeafault/Button";
import { Nullable } from "primereact/ts-helpers";

interface IFiltersForm {
  handleApplyFilters: () => void;
  creator: string;
  setCreator: (value: string) => void;
  date: Nullable<Date>;
  setDate: (value: Date) => void;
  id: Nullable<number>;
  setId: (value: number) => void;
}

export const FiltersForm = ({
  handleApplyFilters,
  creator,
  setCreator,
  date,
  setDate,
  id,
  setId,
}: IFiltersForm) => {
  return (
    <form
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "20px",
      }}
      // className={styles.filters}
      onSubmit={(e) => {
        e.preventDefault();
        handleApplyFilters();
      }}
    >
      <Input
        value={creator}
        onChange={(e) => setCreator(e.target.value)}
        label="Поиск по автору"
      />
      <Input
        value={String(id)}
        onChange={(e) => setId(Number(e.target.value))}
        label="Поиск по ID"
        type="number"
      />
      <MyCalendar
        value={date}
        onChange={(e: { value: Date }) => setDate(e.value)}
        showIcon
        dateFormat="dd.mm.yy"
      />

      <Button
        onClick={() => handleApplyFilters()}
        filled
        color="white"
        type="submit"
      >
        Применить фильтры
      </Button>
    </form>
  );
};

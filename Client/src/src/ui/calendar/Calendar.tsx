import { Calendar } from "primereact/calendar";
import { Nullable } from "primereact/ts-helpers";
import "./Calendar.scss";
import { addLocale } from 'primereact/api';

interface IMyCalendar {
  value: Nullable<Date>;
  onChange: (event: any) => void;
  showIcon?: boolean;
  dateFormat?: string;
}

export const MyCalendar = ({
  value,
  onChange,
  showIcon,
  dateFormat,
}: IMyCalendar) => {
  addLocale("ru", {
    firstDayOfWeek: 1,
    dayNames: [
      "Воскресенье",
      "Понедельник",
      "Вторник",
      "Среда",
      "Четверг",
      "Пятница",
      "Суббота",
    ],
    dayNamesShort: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    dayNamesMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    monthNames: [
      "Январь",
      "Февраль",
      "Март",
      "Апрель",
      "Май",
      "Июнь",
      "Июль",
      "Август",
      "Сентябрь",
      "Октябрь",
      "Ноябрь",
      "Декабрь",
    ],
    monthNamesShort: [
      "Янв",
      "Фев",
      "Мар",
      "Апр",
      "Май",
      "Июн",
      "Июл",
      "Авг",
      "Сен",
      "Окт",
      "Ноя",
      "Дек",
    ],
  });

  return (
    <Calendar
      value={value}
      onChange={onChange}
      showIcon={showIcon}
      dateFormat={dateFormat}
      locale="ru"
    />
  );
};

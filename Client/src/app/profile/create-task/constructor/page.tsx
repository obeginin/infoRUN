import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./create-task.module.scss";
import { TaskConstructor } from "@/src/Widgets/Constructor/TaskConstructor/TaskConstructor";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
export default function CreateTask() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Создание задачи", link: "/profile/create-task" },
    {
      id: 3,
      label: "Конструктор заданий",
      link: "/profile/create-task/constructor",
    },
  ];
  return (
    <div style={{ position: "relative", minHeight: "100vh" }}>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
        <div className={styles.container}>
          <section>
            <TaskConstructor />
          </section>
        </div>
      </div>
      <Footer />
    </div>
  );
}

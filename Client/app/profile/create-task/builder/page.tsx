import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import styles from "./create-task.module.scss";
import { TaskConstructor } from "@/Widgets/Constructor/TaskConstructor/TaskConstructor";
import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import { EndDialog } from "@/Widgets/Constructor/EndDialog/EndDialog";
export default function ConstructorTask () {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Создание задачи", link: "/profile/create-task" },
    {
      id: 3,
      label: "Конструктор заданий",
      link: "/profile/create-task/builder",
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
      <EndDialog />
      <Footer />
    </div>
  );
}

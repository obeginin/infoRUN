import { Header } from "@/src/Widgets/Header/Header";
import styles from "./createTask.module.scss";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { CreateForm } from "@/src/Widgets/Constructor/CreateForm/CreateForm";
import group from "@public/alphabet/group.svg";
import Image from "next/image";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
export default function CreateTask() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Создание задачи", link: "/profile/create-task" },
  ]
  return (
    <>
      <div style={{ position: "relative", minHeight: "100vh" }}>
        <Image
          src={group}
          alt=""
          className={styles.group + " " + styles.first}
        />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            // minHeight: "100vh",
          }}
        >
          <Header />
          <div
            className="app"
            style={{
              width: "100%",
              maxWidth: "1400px",
              margin: "0 auto",
              flex: "1 0 auto",
              padding: "0 20px",
              marginTop: "100px",
            }}
          >
            <BreadCrumb items={items} />
            <CreateForm />
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}

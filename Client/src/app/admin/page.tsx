import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { AdminChangeUser } from "@/src/Widgets/Admin/AdminChangeUser/AdminChangeUser";
import { AdminNewUser } from "@/src/Widgets/Admin/AdminNewUser/AdminNewUser";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./admin.module.scss"

export default function Admin() {
  const items = [
    { id: 1, label: "Панель администратора", link: "/admin" },
  ]
  return (
    <>
        <Header />
      <div className="app">

        <BreadCrumb items={items} />
        <section>
          <div className={styles.admin__container}>
            <AdminNewUser />
            <AdminChangeUser />
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
}
